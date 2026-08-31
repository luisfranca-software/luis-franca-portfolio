"""Unit tests for Knowledge Base services.

Governing documents: SPEC-004 §52.
"""

from __future__ import annotations

import pytest

from apps.knowledge.integrations.fake_embedding_provider import FakeEmbeddingProvider
from apps.knowledge.models import Category, IndexingStatus, KnowledgeDocument, Language
from apps.knowledge.services.chunking import chunk_text
from apps.knowledge.services.embedding_provider import EmbeddingError
from apps.knowledge.services.indexing import IndexingService
from apps.knowledge.services.normalization import Normalizer, normalize_text


class TestNormalization:
    """KB-UT-001 normalization is deterministic."""

    def test_normalization_is_deterministic(self) -> None:
        text = "Hello\r\nWorld.\n\n\nAnother   paragraph.\t\tDone."
        assert normalize_text(text) == normalize_text(text)
        assert "\r" not in normalize_text(text)
        assert "   " not in normalize_text(text)

    def test_normalizer_instance_is_deterministic(self) -> None:
        normalizer = Normalizer()
        text = "Line one\n\n\nLine two"
        assert normalizer.normalize(text) == normalizer.normalize(text)


class TestChunking:
    """KB-UT-002 through KB-UT-006 chunking behavior."""

    def test_chunking_is_deterministic(self) -> None:
        text = "First sentence. Second sentence. Third sentence." * 50
        assert chunk_text(text) == chunk_text(text)

    def test_empty_chunks_are_excluded(self) -> None:
        assert chunk_text("") == []
        assert chunk_text("   \n\n   ") == []

    def test_stable_sequence(self) -> None:
        text = "A. " * 300 + "B. " * 300
        chunks = chunk_text(text)
        for index, chunk in enumerate(chunks):
            assert chunk == chunk_text(text)[index]

    def test_en_chunking(self) -> None:
        text = "This is a sentence. Here is another one. " * 50
        chunks = chunk_text(text)
        assert all(len(chunk.strip()) > 0 for chunk in chunks)
        assert all("." in chunk for chunk in chunks)

    def test_pt_br_chunking(self) -> None:
        text = "Esta é uma frase. Aqui está outra frase. " * 50
        chunks = chunk_text(text)
        assert all(len(chunk.strip()) > 0 for chunk in chunks)

    def test_whitespace_only_chunks_not_persisted(self) -> None:
        chunks = chunk_text("Real content.\n\n   \n\nMore content.")
        assert all(chunk.strip() for chunk in chunks)

    def test_oversized_sentence_is_split(self) -> None:
        """A sentence longer than target_size must be deterministically split."""
        target_size = 1200
        long_word = "word"
        words = []
        while len(" ".join(words + [long_word])) <= target_size:
            words.append(long_word)
        words.extend(["overflow"] * 50)
        text = " ".join(words) + "."

        chunks = chunk_text(text, target_size=target_size)

        assert len(chunks) > 1
        assert all(len(chunk) <= target_size for chunk in chunks)
        assert all(chunk.strip() for chunk in chunks)
        joined = " ".join(chunk.replace("\n\n", " ") for chunk in chunks)
        for word in words:
            assert word in joined


class TestEmbeddingValidation:
    """KB-UT-007 and KB-UT-008 embedding validation."""

    def test_count_validation(self) -> None:
        service = IndexingService(FakeEmbeddingProvider())
        with pytest.raises(EmbeddingError, match="Embedding count mismatch"):
            service._validate_embeddings(["a", "b"], [[0.0] * 1024])

    def test_dimension_validation(self) -> None:
        service = IndexingService(FakeEmbeddingProvider())
        with pytest.raises(EmbeddingError, match="Dimension mismatch"):
            service._validate_embeddings(["a"], [[0.0] * 512])


@pytest.mark.django_db
class TestIndexLifecycle:
    """KB-UT-011 index lifecycle transitions."""

    def test_service_mark_failure_updates_state(self) -> None:
        service = IndexingService(FakeEmbeddingProvider())
        doc = KnowledgeDocument.objects.create(
            title="T",
            slug="t",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        service._mark_failed(doc, "test error")
        doc.refresh_from_db()
        assert doc.indexing_status == IndexingStatus.FAILED
        assert doc.last_index_error == "test error"


@pytest.mark.django_db
class TestIndexingDocumentValidation:
    """Invalid documents must fail before the embedding provider is invoked."""

    def test_blank_title_rejected(self) -> None:
        doc = KnowledgeDocument(
            title="   ",
            slug="blank-title",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        with pytest.raises(EmbeddingError, match="validation failed"):
            IndexingService(FakeEmbeddingProvider()).index_document(doc)

    def test_blank_content_rejected(self) -> None:
        doc = KnowledgeDocument(
            title="Title",
            slug="blank-content",
            language=Language.EN,
            category=Category.GENERAL,
            content="   ",
        )
        with pytest.raises(EmbeddingError, match="validation failed"):
            IndexingService(FakeEmbeddingProvider()).index_document(doc)

    def test_unsupported_language_rejected(self) -> None:
        doc = KnowledgeDocument(
            title="Title",
            slug="bad-language",
            language="zz",
            category=Category.GENERAL,
            content="Content.",
        )
        with pytest.raises(EmbeddingError, match="Unsupported language"):
            IndexingService(FakeEmbeddingProvider()).index_document(doc)

    def test_unsupported_category_rejected(self) -> None:
        doc = KnowledgeDocument(
            title="Title",
            slug="bad-category",
            language=Language.EN,
            category="UNKNOWN",
            content="Content.",
        )
        with pytest.raises(EmbeddingError, match="Unsupported category"):
            IndexingService(FakeEmbeddingProvider()).index_document(doc)

    def test_invalid_document_status_set_to_failed(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Title",
            slug="invalid-failed",
            language=Language.EN,
            category=Category.GENERAL,
            content="   ",
        )
        with pytest.raises(EmbeddingError):
            IndexingService(FakeEmbeddingProvider()).index_document(doc)
        doc.refresh_from_db()
        assert doc.indexing_status == IndexingStatus.FAILED


@pytest.mark.django_db
class TestIndexingMetadataPreservation:
    """Last successful index metadata must survive content edits and failures."""

    def test_successful_index_metadata_set(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Title",
            slug="metadata-success",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content to index.",
        )
        IndexingService(FakeEmbeddingProvider()).index_document(doc)
        doc.refresh_from_db()

        assert doc.indexing_status == IndexingStatus.INDEXED
        assert doc.embedding_model == "fake"
        assert doc.indexed_at is not None
        assert doc.index_version == 2

    def test_failed_reindex_preserves_previous_metadata(self) -> None:
        service = IndexingService(FakeEmbeddingProvider())
        doc = KnowledgeDocument.objects.create(
            title="Title",
            slug="metadata-failure",
            language=Language.EN,
            category=Category.GENERAL,
            content="Original content for indexing.",
        )
        service.index_document(doc)
        original_indexed_at = doc.indexed_at
        original_embedding_model = doc.embedding_model
        original_chunks = list(doc.chunks.all())
        assert original_chunks

        doc.content = FakeEmbeddingProvider.failure_text()
        doc.save()
        with pytest.raises(EmbeddingError):
            service.index_document(doc)
        doc.refresh_from_db()

        assert doc.indexing_status == IndexingStatus.FAILED
        assert doc.embedding_model == original_embedding_model
        assert doc.indexed_at == original_indexed_at
        assert list(doc.chunks.all()) == original_chunks
        assert doc.last_index_error != ""
