"""Unit tests for IA Jujuju input validation, abuse protection, and orchestration.

Governing documents: SPEC-005 §13, §47, §56.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from django.test import RequestFactory

from apps.assistant.integrations.fake_provider import FakeLLMProvider
from apps.assistant.models import Conversation, ConversationStatus, MessageRole
from apps.assistant.services.llm_provider import LLMNonRetryableError, LLMTransientError
from apps.assistant.services.orchestration import (
    AbuseError,
    AbuseProtection,
    AssistantService,
    QuestionValidator,
    ValidationError,
)


class TestQuestionValidator:
    def test_normalizes_whitespace(self) -> None:
        validator = QuestionValidator(max_length=100)
        assert validator.validate("  hello   world  ") == "hello world"

    def test_rejects_empty_question(self) -> None:
        validator = QuestionValidator(max_length=100)
        with pytest.raises(ValidationError, match="empty"):
            validator.validate("")
        with pytest.raises(ValidationError, match="empty"):
            validator.validate("   ")
        with pytest.raises(ValidationError, match="required"):
            validator.validate(None)

    def test_rejects_oversized_question(self) -> None:
        validator = QuestionValidator(max_length=10)
        with pytest.raises(ValidationError, match="exceeds"):
            validator.validate("a" * 11)

    def test_accepts_max_length(self) -> None:
        validator = QuestionValidator(max_length=10)
        assert validator.validate("a" * 10) == "a" * 10


class TestAbuseProtection:
    def test_allows_under_threshold(self) -> None:
        protection = AbuseProtection(window_seconds=60, max_requests=2)
        request = RequestFactory().get("/")
        request.session = {}

        protection.check(request)
        protection.check(request)

    def test_rejects_over_threshold(self) -> None:
        protection = AbuseProtection(window_seconds=60, max_requests=2)
        request = RequestFactory().get("/")
        request.session = {}

        protection.check(request)
        protection.check(request)
        with pytest.raises(AbuseError):
            protection.check(request)

    def test_window_expires(self) -> None:
        protection = AbuseProtection(window_seconds=0, max_requests=1)
        request = RequestFactory().get("/")
        request.session = {}

        protection.check(request)
        protection.check(request)


@pytest.fixture
def request_with_session():
    from django.contrib.sessions.backends.db import SessionStore

    request = RequestFactory().post("/assistant/ask/")
    session = SessionStore()
    session.create()
    request.session = session
    return request


@pytest.mark.django_db
class TestAssistantServiceUnit:
    def test_invalid_input_returns_error(self, request_with_session) -> None:
        service = AssistantService(llm_provider=FakeLLMProvider())

        result = service.ask(request_with_session, "", "en")

        assert result.success is False
        assert result.error_code == "invalid_question"

    def test_oversized_input_returns_error(self, request_with_session) -> None:
        service = AssistantService(
            llm_provider=FakeLLMProvider(),
            question_validator=QuestionValidator(max_length=5),
        )

        result = service.ask(request_with_session, "a" * 100, "en")

        assert result.success is False
        assert result.error_code == "invalid_question"

    def test_unsupported_language_returns_error(self, request_with_session) -> None:
        service = AssistantService(llm_provider=FakeLLMProvider())

        result = service.ask(request_with_session, "Hello", "zz")

        assert result.success is False
        assert result.error_code == "unsupported_language"

    def test_abuse_protection_returns_error_before_provider(self, request_with_session) -> None:
        service = AssistantService(
            llm_provider=FakeLLMProvider(),
            abuse_protection=AbuseProtection(window_seconds=60, max_requests=0),
        )

        result = service.ask(request_with_session, "Hello", "en")

        assert result.success is False
        assert result.error_code == "abuse_protection"

    def test_missing_api_key_returns_provider_error(self, request_with_session, settings) -> None:
        settings.OPENAI_API_KEY = ""
        service = AssistantService(retrieval_service=MagicMock())

        result = service.ask(request_with_session, "Hello", "en")

        assert result.success is False
        assert result.error_code == "provider_error"
        assert "temporarily unavailable" in result.error_message.lower()

    def test_invalid_provider_config_returns_provider_error(
        self, request_with_session, settings
    ) -> None:
        settings.OPENAI_API_KEY = "test-key"
        settings.ASSISTANT_OPENAI_TIMEOUT = "0"
        service = AssistantService(retrieval_service=MagicMock())

        result = service.ask(request_with_session, "Hello", "en")

        assert result.success is False
        assert result.error_code == "provider_error"

    def test_user_message_persisted_when_provider_missing(
        self, request_with_session, settings
    ) -> None:
        settings.OPENAI_API_KEY = ""
        service = AssistantService(retrieval_service=MagicMock())

        result = service.ask(request_with_session, "Hello", "en")

        assert result.success is False
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.messages.filter(role=MessageRole.USER).exists()
        assert not conversation.messages.filter(role=MessageRole.ASSISTANT).exists()

    def test_malformed_conversation_id_rejected(self, request_with_session) -> None:
        service = AssistantService(
            llm_provider=FakeLLMProvider(),
            retrieval_service=MagicMock(),
        )

        result = service.ask(request_with_session, "Hello", "en", conversation_id="not-an-id")

        assert result.success is False
        assert result.error_code == "invalid_conversation"

    def test_non_retryable_provider_error_marks_conversation_failed(
        self, request_with_session
    ) -> None:
        class FailingProvider(FakeLLMProvider):
            def generate(self, input_data):
                raise LLMNonRetryableError("simulated auth failure")

        service = AssistantService(
            llm_provider=FailingProvider(),
            retrieval_service=MagicMock(),
        )

        result = service.ask(request_with_session, "Hello", "en")

        assert result.success is False
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.status == ConversationStatus.FAILED

    def test_transient_provider_error_preserves_active_status(self, request_with_session) -> None:
        class FailingProvider(FakeLLMProvider):
            def generate(self, input_data):
                raise LLMTransientError("simulated transient failure")

        service = AssistantService(
            llm_provider=FailingProvider(),
            retrieval_service=MagicMock(),
        )

        result = service.ask(request_with_session, "Hello", "en")

        assert result.success is False
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.status == ConversationStatus.ACTIVE


@pytest.mark.django_db
class TestGenerationInputContract:
    def test_context_passed_to_provider_exactly_once(self, request_with_session) -> None:
        captured = []

        class CapturingProvider(FakeLLMProvider):
            def generate(self, input_data):
                captured.append(input_data)
                return super().generate(input_data)

        from apps.knowledge.integrations.fake_embedding_provider import FakeEmbeddingProvider
        from apps.knowledge.models import Category, KnowledgeDocument, Language
        from apps.knowledge.services.indexing import IndexingService
        from apps.knowledge.services.retrieval import RetrievalService

        doc = KnowledgeDocument.objects.create(
            title="Python",
            slug="python",
            language=Language.EN,
            category=Category.SKILL,
            content="Python is a programming language.",
        )
        IndexingService(FakeEmbeddingProvider()).index_document(doc)

        service = AssistantService(
            llm_provider=CapturingProvider(),
            retrieval_service=RetrievalService(FakeEmbeddingProvider()),
        )
        result = service.ask(request_with_session, "python", "en")

        assert result.success is True
        assert len(captured) == 1
        input_data = captured[0]
        assert "Python is a programming language" in input_data.context
        assert "Visitor question:" in input_data.user_question
        # The provider input is built from context + user_question; context text
        # must appear exactly once.
        assert input_data.context.count("Python is a programming language") == 1
        combined = f"{input_data.context}\n\n{input_data.user_question}"
        assert combined.count("Python is a programming language") == 1

    def test_no_evidence_question_reaches_provider(self, request_with_session) -> None:
        captured = []

        class CapturingProvider(FakeLLMProvider):
            def generate(self, input_data):
                captured.append(input_data)
                return super().generate(input_data)

        fake_retrieval = MagicMock()
        fake_retrieval.retrieve.return_value = []
        service = AssistantService(
            llm_provider=CapturingProvider(),
            retrieval_service=fake_retrieval,
        )
        result = service.ask(request_with_session, "quantum computing", "en")

        assert result.success is True
        assert len(captured) == 1
        input_data = captured[0]
        assert input_data.context == ""
        assert "quantum computing" in input_data.user_question
        assert "does not contain sufficient information" in input_data.user_question

    def test_portuguese_question_reaches_provider(self, request_with_session) -> None:
        captured = []

        class CapturingProvider(FakeLLMProvider):
            def generate(self, input_data):
                captured.append(input_data)
                return super().generate(input_data)

        fake_retrieval = MagicMock()
        fake_retrieval.retrieve.return_value = []
        service = AssistantService(
            llm_provider=CapturingProvider(),
            retrieval_service=fake_retrieval,
        )
        result = service.ask(request_with_session, "engenheiro", "pt-br")

        assert result.success is True
        assert len(captured) == 1
        input_data = captured[0]
        assert input_data.language == "pt-br"
        assert "engenheiro" in input_data.user_question
