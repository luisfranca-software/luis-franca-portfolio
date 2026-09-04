"""Unit tests for IA Jujuju input validation, abuse protection, and orchestration.

Governing documents: SPEC-005 §13, §47, §56.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from django.test import RequestFactory

from apps.assistant.integrations.fake_provider import FakeLLMProvider
from apps.assistant.models import Conversation, ConversationStatus, MessageRole
from apps.assistant.services.llm_provider import (
    GenerationResult,
    LLMNonRetryableError,
    LLMTransientError,
)
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

    def test_generation_input_receives_bounded_authorized_history(
        self,
        request_with_session,
    ) -> None:
        captured_questions: list[str] = []

        class CapturingProvider:
            def __init__(self) -> None:
                self.call_count = 0

            def generate(self, input_data):
                captured_questions.append(input_data.user_question)
                self.call_count += 1
                return GenerationResult(
                    content=f"Assistant reply {self.call_count}",
                    model="capturing",
                )

        retrieval_service = MagicMock()
        retrieval_service.retrieve.return_value = []
        service = AssistantService(
            llm_provider=CapturingProvider(),
            retrieval_service=retrieval_service,
            history_messages=4,
        )

        first = service.ask(request_with_session, "Turn one", "en")
        service.ask(request_with_session, "Turn two", "en", conversation_id=first.conversation_id)
        service.ask(
            request_with_session,
            "Turn three",
            "en",
            conversation_id=first.conversation_id,
        )
        result = service.ask(
            request_with_session,
            "Current question",
            "en",
            conversation_id=first.conversation_id,
        )

        assert result.success is True
        conversation = Conversation.objects.get(pk=first.conversation_id)
        history = service._recent_history(conversation, before_sequence=6)
        assert history == [
            ("user", "Turn two"),
            ("assistant", "Assistant reply 2"),
            ("user", "Turn three"),
            ("assistant", "Assistant reply 3"),
        ]

        prompt = captured_questions[-1]
        assert "Visitor: Turn one" not in prompt
        assert "Assistant: Assistant reply 1" not in prompt
        assert "Visitor: Turn two" in prompt
        assert "Assistant: Assistant reply 2" in prompt
        assert "Visitor: Turn three" in prompt
        assert "Assistant: Assistant reply 3" in prompt
        assert prompt.index("Visitor: Turn two") < prompt.index("Assistant: Assistant reply 2")
        assert prompt.index("Assistant: Assistant reply 2") < prompt.index("Visitor: Turn three")
        assert prompt.index("Visitor: Turn three") < prompt.index("Assistant: Assistant reply 3")
        assert "Visitor question: Current question" in prompt

    def test_retrieval_query_is_contextualized_with_recent_history(
        self,
        request_with_session,
    ) -> None:
        retrieval_service = MagicMock()
        retrieval_service.retrieve.return_value = []
        service = AssistantService(
            llm_provider=FakeLLMProvider(),
            retrieval_service=retrieval_service,
        )

        first = service.ask(request_with_session, "Does Luís have RAG experience?", "en")
        assert first.success is True

        second = service.ask(
            request_with_session,
            "Which project?",
            "en",
            conversation_id=first.conversation_id,
        )

        assert second.success is True
        retrieval_query = retrieval_service.retrieve.call_args_list[-1].args[0]
        assert "Does Luís have RAG experience?" in retrieval_query
        assert "Test answer from IA Jujuju" in retrieval_query
        assert "Which project?" in retrieval_query


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
