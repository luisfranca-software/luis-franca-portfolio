"""Public interaction tests for IA Jujuju.

Governing documents: SPEC-005 §59.
"""

from __future__ import annotations

import pytest
from django.test import Client
from django.urls import reverse

from apps.assistant.models import Conversation, ConversationMessage, MessageRole
from apps.assistant.services.orchestration import AssistantService
from apps.knowledge.integrations.fake_embedding_provider import FakeEmbeddingProvider
from apps.knowledge.models import Category, KnowledgeDocument, Language
from apps.knowledge.services.indexing import IndexingService
from apps.knowledge.services.retrieval import RetrievalService


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
def service():
    from apps.assistant.integrations.fake_provider import FakeLLMProvider

    return AssistantService(
        llm_provider=FakeLLMProvider(),
        retrieval_service=RetrievalService(FakeEmbeddingProvider()),
    )


@pytest.fixture(autouse=True)
def _patch_assistant_service_for_tests(service, monkeypatch):
    """Replace the default AssistantService in views with the test double."""
    import apps.assistant.views as views_module

    monkeypatch.setattr(views_module, "AssistantService", lambda: service)


@pytest.mark.django_db
class TestAssistantPanelEndpoint:
    def test_panel_endpoint_reachable(self) -> None:
        response = Client().get("/assistant/")
        assert response.status_code == 200
        content = response.content.decode()
        assert "IA Jujuju" in content
        assert 'id="assistant-question"' in content

    def test_panel_with_conversation_reachable(self, client: Client) -> None:
        session = client.session
        session.create()
        conversation = Conversation.objects.create(
            session_key=session.session_key,
            language="en",
        )
        response = client.get(f"/assistant/{conversation.pk}/")
        assert response.status_code == 200

    def test_panel_renders_english_strings_by_default(self) -> None:
        response = Client().get("/assistant/")
        assert response.status_code == 200
        content = response.content.decode()

        assert (
            "Hi, I'm Jujuju, your virtual assistant for Luís França's professional portfolio."
            in content
        )
        assert "Type your question..." in content
        assert "Send" in content
        assert "Olá, sou a Jujuju" not in content
        assert "Digite sua pergunta" not in content
        assert "Enviar" not in content

    def test_panel_renders_translated_strings_in_pt_br(self) -> None:
        client_pt = Client(HTTP_ACCEPT_LANGUAGE="pt-br")
        response = client_pt.get("/assistant/")
        assert response.status_code == 200
        content = response.content.decode()

        assert (
            "Olá, sou a Jujuju, sua assistente virtual do portfólio profissional de Luís França."
            in content
        )
        assert "Digite sua pergunta..." in content
        assert "Enviar" in content
        assert (
            "Hi, I'm Jujuju, your virtual assistant for Luís França's professional portfolio."
            not in content
        )
        assert "Type your question..." not in content
        assert ">Send<" not in content

    def test_panel_has_htmx_submit_guards_and_stable_empty_conversation_field(self) -> None:
        response = Client().get("/assistant/")
        assert response.status_code == 200
        content = response.content.decode()

        assert 'hx-sync="this:drop"' in content
        assert "hx-disabled-elt=\"find button[type='submit']\"" in content
        assert content.count('id="assistant-conversation-id"') == 1
        assert 'name="conversation_id"' in content
        assert 'value=""' in content

    def test_panel_with_existing_conversation_populates_stable_conversation_field(
        self, client: Client
    ) -> None:
        session = client.session
        session.create()
        conversation = Conversation.objects.create(
            session_key=session.session_key,
            language="en",
        )

        response = client.get(reverse("assistant:panel_conversation", args=[conversation.pk]))
        assert response.status_code == 200
        content = response.content.decode()

        assert content.count('id="assistant-conversation-id"') == 1
        assert f'value="{conversation.pk}"' in content


@pytest.mark.django_db
class TestAskEndpoint:
    def test_post_only(self) -> None:
        response = Client().get("/assistant/ask/")
        assert response.status_code == 405

    def test_csrf_required(self) -> None:
        client = Client(enforce_csrf_checks=True)
        response = client.post("/assistant/ask/", {"question": "Hello"})
        assert response.status_code == 403

    def test_empty_question_rejected(self, client: Client) -> None:
        response = client.post("/assistant/ask/", {"question": "  "})
        assert response.status_code == 422
        content = response.content.decode()
        assert "valid question" in content.lower() or "question" in content.lower()

    def test_oversized_question_rejected(self, client: Client) -> None:
        response = client.post("/assistant/ask/", {"question": "a" * 501})
        assert response.status_code == 422

    def test_malformed_conversation_id_rejected(self, client: Client) -> None:
        response = client.post(
            "/assistant/ask/",
            {"question": "Hello", "conversation_id": "not-an-id"},
        )
        assert response.status_code == 422
        content = response.content.decode()
        assert "conversation" in content.lower() or "not available" in content.lower()
        assert Conversation.objects.count() == 0

    def test_valid_en_request_succeeds(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        response = client.post("/assistant/ask/", {"question": "python backend"})
        assert response.status_code == 200
        content = response.content.decode()
        assert "Test answer from IA Jujuju" in content

    def test_valid_pt_br_request_succeeds(self, client: Client) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Perfil",
            slug="perfil",
            language=Language.PT_BR,
            category=Category.PROFILE,
            content="Luís França é engenheiro de software.",
        )
        IndexingService(FakeEmbeddingProvider()).index_document(doc)

        client_pt = Client(HTTP_ACCEPT_LANGUAGE="pt-br")
        response = client_pt.post("/assistant/ask/", {"question": "engenheiro"})
        assert response.status_code == 200
        content = response.content.decode()
        assert "Resposta de teste" in content

    def test_conversation_continuity(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        response_one = client.post("/assistant/ask/", {"question": "First"})
        assert response_one.status_code == 200

        conversation = Conversation.objects.get(session_key=client.session.session_key)
        response_two = client.post(
            "/assistant/ask/",
            {"question": "Second", "conversation_id": str(conversation.pk)},
        )
        assert response_two.status_code == 200
        assert conversation.messages.count() == 4

    def test_successful_htmx_response_returns_single_exchange_and_oob_conversation_update(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        response = client.post(
            "/assistant/ask/",
            {"question": "python backend"},
            HTTP_HX_REQUEST="true",
        )

        assert response.status_code == 200
        content = response.content.decode()
        conversation = Conversation.objects.get(session_key=client.session.session_key)

        assert content.count('id="assistant-conversation-id"') == 1
        assert 'hx-swap-oob="true"' in content
        assert f'value="{conversation.pk}"' in content
        assert content.count("assistant-message--user") == 1
        assert content.count("assistant-message--assistant") == 1

    def test_subsequent_post_reuses_returned_conversation_id_without_creating_new_conversation(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        first_response = client.post(
            "/assistant/ask/",
            {"question": "First"},
            HTTP_HX_REQUEST="true",
        )
        assert first_response.status_code == 200

        conversation = Conversation.objects.get(session_key=client.session.session_key)
        second_response = client.post(
            "/assistant/ask/",
            {"question": "Second", "conversation_id": str(conversation.pk)},
        )

        assert second_response.status_code == 200
        assert Conversation.objects.count() == 1
        conversation.refresh_from_db()
        messages = list(conversation.messages.order_by("sequence"))
        assert [message.role for message in messages] == [
            MessageRole.USER,
            MessageRole.ASSISTANT,
            MessageRole.USER,
            MessageRole.ASSISTANT,
        ]
        assert messages[0].content == "First"
        assert messages[2].content == "Second"

    def test_successful_turn_persists_exactly_one_user_and_one_assistant_message(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        response = client.post("/assistant/ask/", {"question": "python backend"})
        assert response.status_code == 200

        conversation = Conversation.objects.get(session_key=client.session.session_key)
        messages = ConversationMessage.objects.filter(conversation=conversation)

        assert messages.count() == 2
        assert messages.filter(role=MessageRole.USER).count() == 1
        assert messages.filter(role=MessageRole.ASSISTANT).count() == 1

    def test_cross_session_rejection(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        client_one = Client()
        client_one.post("/assistant/ask/", {"question": "Hello"})
        conversation = Conversation.objects.get(session_key=client_one.session.session_key)

        client_two = Client()
        response = client_two.post(
            "/assistant/ask/",
            {"question": "Follow up", "conversation_id": str(conversation.pk)},
        )
        assert response.status_code == 422
        content = response.content.decode()
        assert (
            "conversation" in content.lower()
            or "session" in content.lower()
            or "not available" in content.lower()
        )

    def test_provider_failure_sanitized(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        from apps.assistant.integrations.fake_provider import FakeLLMProvider

        response = client.post(
            "/assistant/ask/",
            {"question": FakeLLMProvider.timeout_text()},
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "temporarily unavailable" in content.lower()
        assert FakeLLMProvider.timeout_text() not in content

    def test_no_api_key_in_output(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        response = client.post("/assistant/ask/", {"question": "python backend"})
        content = response.content.decode()
        assert "OPENAI_API_KEY" not in content
        assert "sk-" not in content

    def test_htmx_partial_returned(
        self,
        client: Client,
        indexed_document: KnowledgeDocument,
    ) -> None:
        response = client.post(
            "/assistant/ask/",
            {"question": "python backend"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "assistant-message--assistant" in content
