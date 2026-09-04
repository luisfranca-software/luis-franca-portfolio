"""IA Jujuju orchestration application service.

Governing documents: ADR-007 §6, §18; SPEC-005 §4, §14, §48.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import transaction

from apps.assistant.integrations.openai_provider import OpenAILLMProvider
from apps.assistant.models import (
    Conversation,
    ConversationMessage,
    ConversationStatus,
    MessageRole,
    SourceEvidence,
)
from apps.assistant.services.context_builder import ContextBuilder, ControlledContext
from apps.assistant.services.llm_provider import (
    GenerationInput,
    LLMNonRetryableError,
    LLMProvider,
    LLMProviderError,
)
from apps.assistant.services.prompt_builder import PromptBuilder
from apps.knowledge.integrations.openai_embedding_provider import OpenAIEmbeddingProvider
from apps.knowledge.services.retrieval import RetrievalResult, RetrievalService

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = logging.getLogger(__name__)


class AssistantError(Exception):
    """Base class for IA Jujuju orchestration failures."""


class ValidationError(AssistantError):
    """User input or request validation failed."""


class AbuseError(AssistantError):
    """Request was rejected by abuse protection before provider invocation."""


class RetrievalError(AssistantError):
    """Technical retrieval failure."""


class ProviderError(AssistantError):
    """Provider failure surfaced to the orchestration layer."""


@dataclass(frozen=True)
class AskResult:
    """Result of a single IA Jujuju question/answer exchange."""

    success: bool
    assistant_message: ConversationMessage | None
    error_code: str
    error_message: str
    conversation_id: int | None


class AbuseProtection:
    """Session-based proportional abuse protection.

    Governing documents: SPEC-005 §47.
    """

    _DEFAULT_WINDOW_SECONDS = 60
    _DEFAULT_MAX_REQUESTS = 10

    def __init__(
        self,
        window_seconds: int | None = None,
        max_requests: int | None = None,
    ) -> None:
        self.window_seconds = (
            window_seconds
            if window_seconds is not None
            else int(
                getattr(
                    settings,
                    "ASSISTANT_ABUSE_WINDOW_SECONDS",
                    self._DEFAULT_WINDOW_SECONDS,
                )
            )
        )
        self.max_requests = (
            max_requests
            if max_requests is not None
            else int(
                getattr(
                    settings,
                    "ASSISTANT_ABUSE_MAX_REQUESTS",
                    self._DEFAULT_MAX_REQUESTS,
                )
            )
        )

    def check(self, request: HttpRequest) -> None:
        """Raise AbuseError if the session exceeds the configured threshold."""
        session = request.session
        if session is None:
            return

        key = "assistant_request_log"
        import time

        now = time.time()
        log = session.get(key, [])
        cutoff = now - self.window_seconds
        log = [timestamp for timestamp in log if timestamp > cutoff]

        if len(log) >= self.max_requests:
            raise AbuseError("Too many requests. Please wait a moment and try again.")

        log.append(now)
        session[key] = log


class QuestionValidator:
    """Server-side validation for visitor questions (SPEC-005 §13)."""

    _DEFAULT_MAX_LENGTH = 500

    def __init__(self, max_length: int | None = None) -> None:
        self.max_length = (
            max_length
            if max_length is not None
            else int(getattr(settings, "ASSISTANT_MAX_QUESTION_LENGTH", self._DEFAULT_MAX_LENGTH))
        )
        if self.max_length < 1:
            raise ValueError("max_length must be at least 1")

    def validate(self, question: str | None) -> str:
        """Return a normalized question or raise ValidationError."""
        if question is None:
            raise ValidationError("Question is required.")
        normalized = " ".join(question.split())
        if not normalized:
            raise ValidationError("Question cannot be empty.")
        if len(normalized) > self.max_length:
            raise ValidationError(
                f"Question exceeds maximum length of {self.max_length} characters."
            )
        return normalized


class AssistantService:
    """Coordinates the IA Jujuju question/answer flow."""

    _DEFAULT_TOP_K = 5
    _DEFAULT_CONTEXT_CHARS = 4000
    _DEFAULT_HISTORY_MESSAGES = 4

    def __init__(
        self,
        *,
        llm_provider: LLMProvider | None = None,
        retrieval_service: RetrievalService | None = None,
        context_builder: ContextBuilder | None = None,
        prompt_builder: PromptBuilder | None = None,
        question_validator: QuestionValidator | None = None,
        abuse_protection: AbuseProtection | None = None,
        top_k: int | None = None,
        history_messages: int | None = None,
    ) -> None:
        self.llm_provider = llm_provider
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder or ContextBuilder(
            int(getattr(settings, "ASSISTANT_CONTEXT_CHARS", self._DEFAULT_CONTEXT_CHARS))
        )
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.question_validator = question_validator or QuestionValidator()
        self.abuse_protection = abuse_protection or AbuseProtection()
        self.top_k = (
            top_k
            if top_k is not None
            else int(getattr(settings, "ASSISTANT_TOP_K", self._DEFAULT_TOP_K))
        )
        self.history_messages = (
            history_messages
            if history_messages is not None
            else int(
                getattr(
                    settings,
                    "ASSISTANT_HISTORY_MESSAGES",
                    self._DEFAULT_HISTORY_MESSAGES,
                )
            )
        )
        if self.history_messages < 0:
            raise ValueError("history_messages must be non-negative")

    def ask(
        self,
        request: HttpRequest,
        question: str | None,
        language: str,
        conversation_id: int | str | None = None,
    ) -> AskResult:
        """Execute the full IA Jujuju exchange."""
        try:
            normalized_question = self.question_validator.validate(question)
        except ValidationError as exc:
            return AskResult(
                success=False,
                assistant_message=None,
                error_code="invalid_question",
                error_message=str(exc),
                conversation_id=None,
            )

        try:
            self.abuse_protection.check(request)
        except AbuseError as exc:
            return AskResult(
                success=False,
                assistant_message=None,
                error_code="abuse_protection",
                error_message=str(exc),
                conversation_id=None,
            )

        if language not in ("en", "pt-br"):
            return AskResult(
                success=False,
                assistant_message=None,
                error_code="unsupported_language",
                error_message="Unsupported language.",
                conversation_id=None,
            )

        try:
            conversation, user_message = self._prepare_conversation(
                request, normalized_question, language, conversation_id
            )
        except ValidationError as exc:
            return AskResult(
                success=False,
                assistant_message=None,
                error_code="invalid_conversation",
                error_message=str(exc),
                conversation_id=None,
            )

        conversation_history = self._recent_history(
            conversation,
            before_sequence=user_message.sequence,
        )

        try:
            retrieval_query = self.prompt_builder.build_retrieval_query(
                language,
                normalized_question,
                conversation_history=conversation_history,
            )
            results = self._retrieve(retrieval_query, language)
        except RetrievalError as exc:
            self._mark_failed_if_non_recoverable(conversation, exc)
            return AskResult(
                success=False,
                assistant_message=None,
                error_code="retrieval_error",
                error_message=str(exc),
                conversation_id=conversation.pk,
            )

        controlled_context = self.context_builder.build(results)
        system_prompt = self.prompt_builder.build_system_prompt(language)
        user_prompt = self.prompt_builder.build_user_prompt(
            language,
            normalized_question,
            conversation_history=conversation_history,
            has_evidence=controlled_context.has_evidence,
        )

        try:
            provider = self._resolve_provider()
        except ProviderError as exc:
            logger.warning("IA Jujuju provider configuration failure: %s", exc.__class__.__name__)
            self._mark_failed_if_non_recoverable(conversation, exc)
            return AskResult(
                success=False,
                assistant_message=None,
                error_code="provider_error",
                error_message="The assistant is temporarily unavailable. Please try again.",
                conversation_id=conversation.pk,
            )

        try:
            generation_result = provider.generate(
                GenerationInput(
                    system_prompt=system_prompt,
                    user_question=user_prompt,
                    context=controlled_context.text,
                    language=language,
                    max_output_tokens=int(getattr(settings, "ASSISTANT_MAX_OUTPUT_TOKENS", 512)),
                )
            )
        except LLMProviderError as exc:
            logger.warning("IA Jujuju provider failure: %s", exc.__class__.__name__)
            self._mark_failed_if_non_recoverable(conversation, exc)
            return AskResult(
                success=False,
                assistant_message=None,
                error_code="provider_error",
                error_message="The assistant is temporarily unavailable. Please try again.",
                conversation_id=conversation.pk,
            )

        assistant_message = self._persist_success(
            conversation,
            generation_result.content,
            controlled_context,
        )
        return AskResult(
            success=True,
            assistant_message=assistant_message,
            error_code="",
            error_message="",
            conversation_id=conversation.pk,
        )

    def _prepare_conversation(
        self,
        request: HttpRequest,
        normalized_question: str,
        language: str,
        conversation_id: int | str | None,
    ) -> tuple[Conversation, ConversationMessage]:
        """Resolve/create the conversation and persist the USER message, then commit."""
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        assert session_key is not None

        resolved_id: int | None = None
        if conversation_id is not None:
            if isinstance(conversation_id, int):
                resolved_id = conversation_id
            else:
                try:
                    resolved_id = int(conversation_id)
                except (TypeError, ValueError) as exc:
                    raise ValidationError("Conversation identifier is not valid.") from exc

        if resolved_id is not None:
            try:
                conversation = Conversation.objects.get(
                    pk=resolved_id,
                    session_key=session_key,
                )
            except Conversation.DoesNotExist as exc:
                raise ValidationError(
                    "Conversation not found or not owned by this session."
                ) from exc
        else:
            conversation = Conversation.objects.create(
                session_key=session_key,
                language=language,
                status=ConversationStatus.ACTIVE,
            )

        next_sequence = conversation.messages.count()
        user_message = ConversationMessage.objects.create(
            conversation=conversation,
            sequence=next_sequence,
            role=MessageRole.USER,
            content=normalized_question,
        )
        # Ensure the transaction is committed before external provider calls.
        return conversation, user_message

    def _retrieve(self, question: str, language: str) -> list[RetrievalResult]:
        """Call the existing RetrievalService outside a long transaction."""
        service = self.retrieval_service or self._build_retrieval_service()
        try:
            return service.retrieve(question, language=language, top_k=self.top_k)
        except Exception as exc:
            logger.warning("IA Jujuju retrieval failure: %s", exc.__class__.__name__)
            raise RetrievalError("Unable to retrieve portfolio knowledge.") from exc

    def _recent_history(
        self,
        conversation: Conversation,
        *,
        before_sequence: int,
    ) -> list[tuple[str, str]]:
        """Return bounded prior messages from the authorized conversation only."""
        if self.history_messages <= 0:
            return []

        messages = list(
            conversation.messages.filter(sequence__lt=before_sequence).order_by("-sequence")[
                : self.history_messages
            ]
        )
        messages.reverse()
        return [(message.role, message.content) for message in messages]

    def _build_retrieval_service(self) -> RetrievalService:
        """Return the production retrieval service using the configured provider."""
        api_key = getattr(settings, "OPENAI_API_KEY", "")
        if not api_key:
            raise RetrievalError("Embedding provider is not configured.")
        provider = OpenAIEmbeddingProvider(
            api_key=api_key,
            timeout=float(getattr(settings, "KNOWLEDGE_OPENAI_TIMEOUT", 30.0)),
            max_retries=int(getattr(settings, "KNOWLEDGE_OPENAI_MAX_RETRIES", 3)),
        )
        return RetrievalService(provider)

    def _resolve_provider(self) -> LLMProvider:
        """Return the configured LLM provider."""
        if self.llm_provider is not None:
            return self.llm_provider
        api_key = getattr(settings, "OPENAI_API_KEY", "")
        if not api_key:
            raise ProviderError("LLM provider is not configured.")
        try:
            return OpenAILLMProvider(
                api_key=api_key,
                model=str(getattr(settings, "ASSISTANT_MODEL", "gpt-5.6-luna")),
                timeout=float(getattr(settings, "ASSISTANT_OPENAI_TIMEOUT", 30.0)),
                max_retries=int(getattr(settings, "ASSISTANT_OPENAI_MAX_RETRIES", 3)),
                max_output_tokens=int(getattr(settings, "ASSISTANT_MAX_OUTPUT_TOKENS", 512)),
            )
        except LLMNonRetryableError as exc:
            raise ProviderError("LLM provider configuration is invalid.") from exc

    @transaction.atomic
    def _persist_success(
        self,
        conversation: Conversation,
        content: str,
        controlled_context: ControlledContext,
    ) -> ConversationMessage:
        """Atomically persist the ASSISTANT message, source evidence, and state."""
        next_sequence = conversation.messages.count()
        assistant_message = ConversationMessage.objects.create(
            conversation=conversation,
            sequence=next_sequence,
            role=MessageRole.ASSISTANT,
            content=content,
        )

        for item in controlled_context.items:
            result = item.retrieval_result
            SourceEvidence.objects.create(
                message=assistant_message,
                document_id=result.document_id,
                chunk_id=result.chunk_id,
                rank=item.rank,
                distance=result.distance,
                document_title=result.document_title,
                document_slug=result.document_slug,
                document_language=result.language,
                document_category=result.category,
                chunk_content=result.content,
            )

        conversation.status = ConversationStatus.ACTIVE
        conversation.save(update_fields=["status", "updated_at"])

        return assistant_message

    def _mark_failed_if_non_recoverable(
        self,
        conversation: Conversation,
        exc: Exception,
    ) -> None:
        """Mark conversation FAILED only for non-recoverable failures.

        Transient OpenAI failures (timeout, rate-limit, connection) preserve ACTIVE
        because retry may succeed. Non-retryable provider errors and retrieval
        failures mark the conversation as FAILED for diagnostic visibility.
        """
        if isinstance(exc, (LLMNonRetryableError, ProviderError, RetrievalError)):
            conversation.status = ConversationStatus.FAILED
            conversation.save(update_fields=["status", "updated_at"])
