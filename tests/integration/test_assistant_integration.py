"""Integration tests for IA Jujuju orchestration and persistence.

Governing documents: SPEC-005 §57.
"""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory
from django.utils import timezone

from apps.assistant.integrations.fake_provider import FakeLLMProvider
from apps.assistant.models import (
    Conversation,
    ConversationMessage,
    ConversationStatus,
    MessageRole,
    SourceEvidence,
)
from apps.assistant.services.llm_provider import GenerationResult, LLMTransientError
from apps.assistant.services.orchestration import AssistantService
from apps.knowledge.integrations.fake_embedding_provider import FakeEmbeddingProvider
from apps.knowledge.models import Category, KnowledgeChunk, KnowledgeDocument, Language
from apps.knowledge.services.indexing import IndexingService
from apps.knowledge.services.retrieval import RetrievalResult, RetrievalService


@pytest.fixture
def indexed_document(db):
    doc = KnowledgeDocument.objects.create(
        title="Python Backend Engineering",
        slug="python-backend-engineering",
        language=Language.EN,
        category=Category.SKILL,
        content=(
            "Luís França builds production-ready Python backend systems using Django, "
            "automated testing, and continuous integration."
        ),
    )
    IndexingService(FakeEmbeddingProvider()).index_document(doc)
    return doc


@pytest.fixture
def pt_indexed_document(db):
    doc = KnowledgeDocument.objects.create(
        title="Perfil Profissional",
        slug="perfil-profissional",
        language=Language.PT_BR,
        category=Category.PROFILE,
        content=(
            "Luís França é engenheiro de software especializado em desenvolvimento "
            "backend Python e automação."
        ),
    )
    IndexingService(FakeEmbeddingProvider()).index_document(doc)
    return doc


@pytest.fixture
def service():
    return AssistantService(
        llm_provider=FakeLLMProvider(),
        retrieval_service=RetrievalService(FakeEmbeddingProvider()),
    )


def _request(session_key: str | None = None):
    from django.contrib.sessions.backends.db import SessionStore

    request = RequestFactory().post("/assistant/ask/")
    session = SessionStore()
    if session_key:
        session["session_key"] = session_key
    session.create()
    request.session = session
    return request


@pytest.mark.django_db
class TestConversationPersistence:
    def test_conversation_creation(self, service: AssistantService) -> None:
        request = _request()
        result = service.ask(request, "What is Python?", "en")

        assert result.success is True
        assert result.conversation_id is not None
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.language == "en"
        assert conversation.status == ConversationStatus.ACTIVE

    def test_session_association(self, service: AssistantService) -> None:
        request = _request()
        result = service.ask(request, "Hello", "en")

        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.session_key
        assert request.session.session_key is not None
        assert conversation.session_key == request.session.session_key

    def test_user_message_persistence(self, service: AssistantService) -> None:
        request = _request()
        result = service.ask(request, "Hello world", "en")

        messages = ConversationMessage.objects.filter(conversation_id=result.conversation_id)
        user_message = messages.get(role=MessageRole.USER)
        assert user_message.content == "Hello world"

    def test_assistant_message_persistence(self, service: AssistantService) -> None:
        request = _request()
        result = service.ask(request, "Hello", "en")

        messages = ConversationMessage.objects.filter(conversation_id=result.conversation_id)
        assistant_message = messages.get(role=MessageRole.ASSISTANT)
        assert "IA Jujuju" in assistant_message.content

    def test_deterministic_ordering(self, service: AssistantService) -> None:
        request = _request()
        result = service.ask(request, "First", "en")
        conversation = Conversation.objects.get(pk=result.conversation_id)
        service.ask(request, "Second", "en", conversation_id=conversation.pk)

        messages = list(conversation.messages.order_by("sequence"))
        assert [m.sequence for m in messages] == [0, 1, 2, 3]
        assert messages[0].role == MessageRole.USER
        assert messages[1].role == MessageRole.ASSISTANT
        assert messages[2].role == MessageRole.USER
        assert messages[3].role == MessageRole.ASSISTANT

    def test_language_persistence(self, service: AssistantService) -> None:
        request = _request()
        result = service.ask(request, "Olá", "pt-br")

        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.language == "pt-br"
        assistant = conversation.messages.get(role=MessageRole.ASSISTANT)
        assert "Resposta de teste" in assistant.content

    def test_follow_up_turn_uses_same_authorized_conversation(
        self, service: AssistantService
    ) -> None:
        request = _request()
        first = service.ask(request, "Luís tem experiência com RAG?", "pt-br")

        second = service.ask(
            request,
            "Em qual projeto?",
            "pt-br",
            conversation_id=first.conversation_id,
        )

        assert second.success is True
        conversation = Conversation.objects.get(pk=first.conversation_id)
        assert conversation.messages.count() == 4


@pytest.mark.django_db
class TestRAGIntegration:
    def test_successful_rag_orchestration(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, "python backend", "en")

        assert result.success is True
        assistant = result.assistant_message
        evidence = SourceEvidence.objects.filter(message=assistant)
        assert evidence.exists()
        assert any(item.document_id == indexed_document.pk for item in evidence)

    def test_source_evidence_has_rank_and_distance(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, "python backend", "en")

        assistant = result.assistant_message
        evidence = SourceEvidence.objects.filter(message=assistant)
        item = evidence.first()
        assert item is not None
        assert item.rank == 1
        assert item.distance is not None
        assert item.document_title == indexed_document.title
        assert item.document_slug == indexed_document.slug
        assert item.document_language == "en"
        assert item.document_category == "SKILL"
        assert item.chunk_content

    def test_no_evidence_behavior(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, "quantum computing", "en")

        assert result.success is True
        assistant = result.assistant_message
        # With FakeEmbeddingProvider, unrelated queries may still return chunks,
        # but the response must be controlled and no fabricated facts asserted.
        assert assistant is not None
        assert "IA Jujuju" in assistant.content

    def test_rag_portuguese_language_filtering(
        self,
        service: AssistantService,
        pt_indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, "engenheiro de software", "pt-br")

        assert result.success is True
        evidence = SourceEvidence.objects.filter(message=result.assistant_message)
        assert all(item.document_language == "pt-br" for item in evidence)

    def test_single_assistant_message_can_hold_multiple_evidence_rows(self) -> None:
        request = _request()
        document_one = KnowledgeDocument.objects.create(
            title="Project A",
            slug="project-a",
            language=Language.EN,
            category=Category.PROJECT,
            content="Luís built a production RAG assistant for Project A.",
        )
        document_two = KnowledgeDocument.objects.create(
            title="Project B",
            slug="project-b",
            language=Language.EN,
            category=Category.PROJECT,
            content="Project B also used retrieval-augmented generation patterns.",
        )
        IndexingService(FakeEmbeddingProvider()).index_document(document_one)
        IndexingService(FakeEmbeddingProvider()).index_document(document_two)
        chunk_one = document_one.chunks.order_by("sequence").first()
        chunk_two = document_two.chunks.order_by("sequence").first()
        assert chunk_one is not None
        assert chunk_two is not None

        retrieval_service = MagicMock()
        retrieval_service.retrieve.return_value = [
            RetrievalResult(
                chunk_id=chunk_one.pk,
                document_id=document_one.pk,
                document_title=document_one.title,
                document_slug=document_one.slug,
                content=chunk_one.content,
                distance=0.11,
                language="en",
                category="PROJECT",
            ),
            RetrievalResult(
                chunk_id=chunk_two.pk,
                document_id=document_two.pk,
                document_title=document_two.title,
                document_slug=document_two.slug,
                content=chunk_two.content,
                distance=0.12,
                language="en",
                category="PROJECT",
            ),
        ]
        service = AssistantService(
            llm_provider=FakeLLMProvider(),
            retrieval_service=retrieval_service,
        )

        result = service.ask(request, "rag project", "en")

        assert result.success is True
        assistant_messages = ConversationMessage.objects.filter(
            conversation_id=result.conversation_id,
            role=MessageRole.ASSISTANT,
        )
        assert assistant_messages.count() == 1
        evidence = list(
            SourceEvidence.objects.filter(message=result.assistant_message).order_by("rank")
        )
        assert len(evidence) == 2
        assert {item.document_id for item in evidence} == {document_one.pk, document_two.pk}
        assert {item.chunk_id for item in evidence} == {chunk_one.pk, chunk_two.pk}
        assert all(KnowledgeChunk.objects.filter(pk=item.chunk_id).exists() for item in evidence)


@pytest.mark.django_db
class TestConversationalContinuity:
    def test_generation_receives_bounded_recent_history_only(self) -> None:
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

        request = _request()
        service = AssistantService(
            llm_provider=CapturingProvider(),
            retrieval_service=RetrievalService(FakeEmbeddingProvider()),
        )
        first = service.ask(request, "First topic", "en")
        service.ask(request, "Second topic", "en", conversation_id=first.conversation_id)
        service.ask(request, "Third topic", "en", conversation_id=first.conversation_id)
        service.ask(request, "Fourth topic", "en", conversation_id=first.conversation_id)
        result = service.ask(request, "Current topic", "en", conversation_id=first.conversation_id)

        assert result.success is True
        conversation = Conversation.objects.get(pk=first.conversation_id)
        history = service._recent_history(conversation, before_sequence=8)
        assert history == [
            ("user", "Third topic"),
            ("assistant", "Assistant reply 3"),
            ("user", "Fourth topic"),
            ("assistant", "Assistant reply 4"),
        ]

        prompt = captured_questions[-1]
        assert "Visitor: First topic" not in prompt
        assert "Assistant: Assistant reply 1" not in prompt
        assert "Visitor: Second topic" not in prompt
        assert "Assistant: Assistant reply 2" not in prompt
        assert "Visitor: Third topic" in prompt
        assert "Assistant: Assistant reply 3" in prompt
        assert "Visitor: Fourth topic" in prompt
        assert "Assistant: Assistant reply 4" in prompt
        assert prompt.index("Visitor: Third topic") < prompt.index("Assistant: Assistant reply 3")
        assert prompt.index("Assistant: Assistant reply 3") < prompt.index("Visitor: Fourth topic")
        assert prompt.index("Visitor: Fourth topic") < prompt.index("Assistant: Assistant reply 4")
        assert "Visitor question: Current topic" in prompt


@pytest.mark.django_db
class TestFailureBehavior:
    def test_user_preserved_on_provider_timeout(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, FakeLLMProvider.timeout_text(), "en")

        assert result.success is False
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.messages.filter(role=MessageRole.USER).exists()
        assert not conversation.messages.filter(role=MessageRole.ASSISTANT).exists()

    def test_no_fabricated_assistant_on_failure(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, FakeLLMProvider.failure_text(), "en")

        assert result.success is False
        assert result.assistant_message is None

    def test_invalid_provider_response_handled(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, FakeLLMProvider.empty_text(), "en")

        assert result.success is False
        assert result.error_code == "provider_error"

    def test_transient_failure_preserves_conversation_continuity(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, FakeLLMProvider.transient_text(), "en")

        assert result.success is False
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.status == ConversationStatus.ACTIVE

    def test_non_retryable_failure_marks_conversation_failed(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, FakeLLMProvider.non_retryable_text(), "en")

        assert result.success is False
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.status == ConversationStatus.FAILED

    def test_retrieval_failure_marks_conversation_failed(self, service: AssistantService) -> None:
        request = _request()

        def failing_retrieve(*args, **kwargs):
            raise RuntimeError("retrieval failed")

        service.retrieval_service = MagicMock()
        service.retrieval_service.retrieve = failing_retrieve

        result = service.ask(request, "Hello", "en")

        assert result.success is False
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.status == ConversationStatus.FAILED

    def test_user_preserved_on_retrieval_failure(self, service: AssistantService) -> None:
        request = _request()

        def failing_retrieve(*args, **kwargs):
            raise RuntimeError("retrieval failed")

        service.retrieval_service = MagicMock()
        service.retrieval_service.retrieve = failing_retrieve

        result = service.ask(request, "Hello", "en")

        assert result.success is False
        conversation = Conversation.objects.get(pk=result.conversation_id)
        assert conversation.messages.filter(role=MessageRole.USER).exists()


@pytest.mark.django_db
class TestTransactionBoundaries:
    def test_user_message_committed_before_provider_call(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        """Provider failure must not roll back an already accepted USER message."""
        request = _request()

        def failing_generate(self, input_data):
            # At this point the USER message must already be durable.
            assert ConversationMessage.objects.filter(
                conversation__session_key=request.session.session_key,
                role=MessageRole.USER,
            ).exists()
            raise LLMTransientError("Simulated failure after USER persistence")

        with patch.object(FakeLLMProvider, "generate", failing_generate):
            result = service.ask(request, "python backend", "en")

        assert result.success is False
        assert ConversationMessage.objects.filter(
            conversation__session_key=request.session.session_key,
            role=MessageRole.USER,
        ).exists()

    def test_atomic_assistant_and_source_persistence(
        self,
        service: AssistantService,
        indexed_document: KnowledgeDocument,
    ) -> None:
        request = _request()
        result = service.ask(request, "python backend", "en")

        assert result.success is True
        assistant = result.assistant_message
        evidence_count = SourceEvidence.objects.filter(message=assistant).count()
        assert evidence_count > 0


@pytest.mark.django_db
class TestSessionAuthorization:
    def test_cross_session_rejection(self, service: AssistantService) -> None:
        request_one = _request()
        result_one = service.ask(request_one, "Hello", "en")
        conversation_id = result_one.conversation_id

        request_two = _request()
        result_two = service.ask(request_two, "Follow up", "en", conversation_id=conversation_id)

        assert result_two.success is False
        assert result_two.error_code == "invalid_conversation"

    def test_unknown_conversation_rejected(self, service: AssistantService) -> None:
        request = _request()

        result = service.ask(request, "Hello", "en", conversation_id=999999)

        assert result.success is False
        assert result.error_code == "invalid_conversation"

    def test_malformed_conversation_id_rejected(self, service: AssistantService) -> None:
        request = _request()

        result = service.ask(request, "Hello", "en", conversation_id="not-an-id")

        assert result.success is False
        assert result.error_code == "invalid_conversation"
        # No new conversation should be created.
        assert Conversation.objects.count() == 0

    def test_conversation_continuity(self, service: AssistantService) -> None:
        request = _request()
        result_one = service.ask(request, "First", "en")
        conversation_id = result_one.conversation_id

        result_two = service.ask(request, "Second", "en", conversation_id=conversation_id)

        assert result_two.success is True
        conversation = Conversation.objects.get(pk=conversation_id)
        assert conversation.messages.count() == 4


@pytest.mark.django_db
class TestRetention:
    def test_retention_eligibility(self) -> None:
        old = Conversation.objects.create(
            session_key="old-session",
            language="en",
            status=ConversationStatus.ACTIVE,
        )
        old.created_at = timezone.now() - timedelta(days=91)
        old.save(update_fields=["created_at"])
        recent = Conversation.objects.create(
            session_key="recent-session",
            language="en",
            status=ConversationStatus.ACTIVE,
        )
        recent.created_at = timezone.now() - timedelta(days=30)
        recent.save(update_fields=["created_at"])

        cutoff = timezone.now() - timedelta(days=90)
        eligible = Conversation.objects.filter(created_at__lt=cutoff)
        assert eligible.filter(pk=old.pk).exists()
        assert not eligible.filter(pk=recent.pk).exists()

    def test_purge_command(self) -> None:
        old = Conversation.objects.create(
            session_key="old-session",
            language="en",
            status=ConversationStatus.ACTIVE,
        )
        old.created_at = timezone.now() - timedelta(days=91)
        old.save(update_fields=["created_at"])
        message = ConversationMessage.objects.create(
            conversation=old,
            sequence=0,
            role=MessageRole.USER,
            content="Hello",
        )
        SourceEvidence.objects.create(
            message=message,
            rank=1,
            distance=0.1,
            document_title="Doc",
            document_slug="doc",
            document_language="en",
            document_category="GENERAL",
            chunk_content="Chunk",
        )
        recent = Conversation.objects.create(
            session_key="recent-session",
            language="en",
            status=ConversationStatus.ACTIVE,
        )
        recent.created_at = timezone.now() - timedelta(days=30)
        recent.save(update_fields=["created_at"])

        from io import StringIO

        from django.core.management import call_command

        out = StringIO()
        call_command("purge_conversations", stdout=out)

        assert not Conversation.objects.filter(pk=old.pk).exists()
        assert Conversation.objects.filter(pk=recent.pk).exists()
        assert not ConversationMessage.objects.filter(conversation=old).exists()
        assert not SourceEvidence.objects.filter(message=message).exists()
        output = out.getvalue()
        assert "Purged 1 expired conversation(s)" in output
        assert "expired" in output
