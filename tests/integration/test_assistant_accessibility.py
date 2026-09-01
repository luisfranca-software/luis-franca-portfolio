"""Accessibility tests for the IA Jujuju public interaction.

Governing documents: SPEC-005 §61.
"""

from __future__ import annotations

import pytest
from django.test import Client

from apps.assistant.integrations.fake_provider import FakeLLMProvider
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


@pytest.fixture(autouse=True)
def _patch_assistant_service_for_tests(monkeypatch):
    from apps.assistant import views as views_module

    service = AssistantService(
        llm_provider=FakeLLMProvider(),
        retrieval_service=RetrievalService(FakeEmbeddingProvider()),
    )
    monkeypatch.setattr(views_module, "AssistantService", lambda: service)


@pytest.mark.django_db
def test_launcher_is_focusable_button() -> None:
    content = Client().get("/").content.decode()

    assert "<button" in content
    assert 'class="home-ai-rag"' in content
    assert 'aria-label="' in content
    assert 'aria-expanded="false"' in content
    assert 'aria-controls="assistant-container"' in content
    launcher_block = content.split('class="home-ai-rag"', 1)[1].split("</button>", 1)[0]
    assert 'aria-hidden="true"' not in launcher_block


@pytest.mark.django_db
def test_panel_has_accessible_form_controls(indexed_document: KnowledgeDocument) -> None:
    response = Client().get("/assistant/")
    content = response.content.decode()

    assert 'role="dialog"' in content
    assert 'aria-modal="true"' in content
    assert 'id="assistant-title"' in content
    assert 'aria-labelledby="assistant-title"' in content
    assert 'id="assistant-question"' in content
    assert 'for="assistant-question"' in content
    assert 'id="assistant-input-help"' in content
    assert 'aria-describedby="assistant-input-help"' in content


@pytest.mark.django_db
def test_panel_has_live_region(indexed_document: KnowledgeDocument) -> None:
    response = Client().get("/assistant/")
    content = response.content.decode()

    assert 'aria-live="polite"' in content
    assert 'id="assistant-messages"' in content


@pytest.mark.django_db
def test_success_response_has_readable_roles(indexed_document: KnowledgeDocument) -> None:
    client = Client()
    response = client.post("/assistant/ask/", {"question": "python backend"})
    content = response.content.decode()

    assert "assistant-message--user" in content
    assert "assistant-message--assistant" in content
    assert "Test answer from IA Jujuju" in content


@pytest.mark.django_db
def test_error_response_has_alert_role(indexed_document: KnowledgeDocument) -> None:
    client = Client()
    response = client.post(
        "/assistant/ask/",
        {"question": FakeLLMProvider.timeout_text()},
    )
    content = response.content.decode()

    assert 'role="alert"' in content
    assert "temporarily unavailable" in content.lower()


@pytest.mark.django_db
def test_loading_state_is_accessible(indexed_document: KnowledgeDocument) -> None:
    response = Client().get("/assistant/")
    content = response.content.decode()

    assert "assistant-panel__loading" in content
    assert 'class="visually-hidden"' in content
    assert "processing" in content.lower()


@pytest.mark.django_db
def test_launcher_has_visible_focus_style() -> None:
    from pathlib import Path

    css_path = Path(__file__).resolve().parents[2] / "frontend" / "static" / "css" / "home.css"
    css = css_path.read_text()

    assert ".home-ai-rag:focus-visible" in css
    assert "outline" in css.split(".home-ai-rag:focus-visible", 1)[1].split("}", 1)[0]
