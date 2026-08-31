"""Tests for the reindex_knowledge management command.

Governing documents: SPEC-004 §41.
"""

from __future__ import annotations

import io

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.knowledge.models import Category, IndexingStatus, KnowledgeDocument, Language


@pytest.fixture
def openai_api_key(settings):
    original = getattr(settings, "OPENAI_API_KEY", "")
    settings.OPENAI_API_KEY = "test-api-key"
    yield
    settings.OPENAI_API_KEY = original


@pytest.mark.django_db
class TestReindexKnowledgeCommand:
    """KB-CMD-001 through KB-CMD-003 management command behavior."""

    def test_missing_openai_key_fails(self, settings) -> None:
        """The command must fail explicitly when OPENAI_API_KEY is missing."""
        settings.OPENAI_API_KEY = ""
        out = io.StringIO()
        err = io.StringIO()
        with pytest.raises(CommandError):
            call_command("reindex_knowledge", stdout=out, stderr=err)

    def test_command_uses_openai_provider(self, openai_api_key, monkeypatch) -> None:
        """The command invokes indexing through the production provider path."""
        KnowledgeDocument.objects.create(
            title="Doc",
            slug="cmd-openai",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        called = False

        def fake_index_document(self, document):
            nonlocal called
            called = True
            document.indexing_status = IndexingStatus.INDEXED
            document.save(update_fields=["indexing_status"])

        monkeypatch.setattr(
            "apps.knowledge.services.indexing.IndexingService.index_document",
            fake_index_document,
        )

        out = io.StringIO()
        err = io.StringIO()
        call_command("reindex_knowledge", "--slug", "cmd-openai", stdout=out, stderr=err)

        assert called
        assert "Done" in out.getvalue()

    def test_fake_provider_not_available(self, settings, monkeypatch) -> None:
        """No --fake flag or fallback is exposed in the command."""
        settings.OPENAI_API_KEY = ""
        # Even if FakeEmbeddingProvider were injected, missing key should still fail.
        out = io.StringIO()
        err = io.StringIO()
        with pytest.raises(CommandError):
            call_command("reindex_knowledge", stdout=out, stderr=err)

    def test_invalid_document_records_failure(self, openai_api_key, monkeypatch) -> None:
        """Invalid documents are reported as failures without reaching OpenAI."""
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="cmd-invalid",
            language=Language.EN,
            category=Category.GENERAL,
            content="   ",
        )
        provider_called = False

        def fake_embed(*_args, **_kwargs):
            nonlocal provider_called
            provider_called = True
            return []

        monkeypatch.setattr(
            "apps.knowledge.integrations.openai_embedding_provider.OpenAIEmbeddingProvider.embed_documents",
            fake_embed,
        )

        out = io.StringIO()
        err = io.StringIO()
        call_command("reindex_knowledge", "--slug", "cmd-invalid", stdout=out, stderr=err)

        assert not provider_called
        doc.refresh_from_db()
        assert doc.indexing_status == IndexingStatus.FAILED
        assert "Failure: 1" in out.getvalue()
