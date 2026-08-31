"""Knowledge document indexing service.

Governing documents: ADR-006 §14, SPEC-004 §19–27.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from datetime import UTC, datetime

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.knowledge.models import (
    Category,
    IndexingStatus,
    KnowledgeChunk,
    KnowledgeDocument,
    Language,
)
from apps.knowledge.services.chunking import chunk_text
from apps.knowledge.services.embedding_provider import EmbeddingError, EmbeddingProvider

logger = logging.getLogger(__name__)


class IndexingService:
    """Coordinate normalization, chunking, embedding, and atomic persistence."""

    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    def index_document(self, document: KnowledgeDocument) -> None:
        """Index or reindex a KnowledgeDocument safely.

        The provider call happens outside the database transaction. The old chunk
        set is replaced only after the new embeddings are successfully generated
        and validated. If anything fails, the previous chunks and successful
        index metadata are preserved and the failure is recorded.
        """
        try:
            self._validate_document(document)
            document.indexing_status = IndexingStatus.INDEXING
            document.save(update_fields=["indexing_status", "updated_at"])

            normalized = self._normalize(document.content)
            chunks = chunk_text(normalized)
            if not chunks:
                raise EmbeddingError("No chunks generated from document content")

            embeddings = self.provider.embed_documents(chunks)
            self._validate_embeddings(chunks, embeddings)

            self._replace_chunks(document, chunks, embeddings)
        except EmbeddingError as exc:
            if document.pk:
                self._mark_failed(document, str(exc))
            logger.warning(
                "Indexing failed for document %s: %s",
                document.pk,
                exc,
            )
            raise
        except Exception as exc:
            if document.pk:
                self._mark_failed(document, f"Unexpected indexing error: {exc.__class__.__name__}")
            logger.exception("Unexpected indexing failure for document %s", document.pk)
            raise EmbeddingError("Unexpected indexing failure") from exc

    def _validate_document(self, document: KnowledgeDocument) -> None:
        """Validate source document state before invoking the embedding provider.

        Model-level validation is not run automatically on save()/objects.create(),
        so the indexing pipeline performs it explicitly.
        """
        if document.language not in Language.values:
            raise EmbeddingError(f"Unsupported language: {document.language}")
        if document.category not in Category.values:
            raise EmbeddingError(f"Unsupported category: {document.category}")

        try:
            document.full_clean()
        except ValidationError as exc:
            messages: list[str] = []
            for field_errors in exc.error_dict.values():
                messages.extend(str(e) for e in field_errors)
            raise EmbeddingError(f"Document validation failed: {'; '.join(messages)}") from exc

    def _normalize(self, content: str) -> str:
        from apps.knowledge.services.normalization import normalize_text

        return normalize_text(content)

    def _validate_embeddings(
        self,
        chunks: Sequence[str],
        embeddings: Sequence[Sequence[float]],
    ) -> None:
        if len(embeddings) != len(chunks):
            raise EmbeddingError(
                f"Embedding count mismatch: expected {len(chunks)}, got {len(embeddings)}"
            )
        expected_dimensions = 1024
        for index, vector in enumerate(embeddings):
            if len(vector) != expected_dimensions:
                raise EmbeddingError(
                    f"Dimension mismatch at chunk {index}: "
                    f"expected {expected_dimensions}, got {len(vector)}"
                )

    @transaction.atomic
    def _replace_chunks(
        self,
        document: KnowledgeDocument,
        chunks: Sequence[str],
        embeddings: Sequence[Sequence[float]],
    ) -> None:
        document.chunks.all().delete()

        model_name = getattr(self.provider, "model", "unknown")
        created_chunks = [
            KnowledgeChunk(
                document=document,
                sequence=index,
                content=chunk,
                embedding=list(embedding),
            )
            for index, (chunk, embedding) in enumerate(zip(chunks, embeddings, strict=True))
        ]
        KnowledgeChunk.objects.bulk_create(created_chunks)

        document.indexing_status = IndexingStatus.INDEXED
        document.index_version += 1
        document.embedding_model = model_name
        document.indexed_at = datetime.now(UTC)
        document.last_index_error = ""
        document.save(
            update_fields=[
                "indexing_status",
                "index_version",
                "embedding_model",
                "indexed_at",
                "last_index_error",
                "updated_at",
            ]
        )

    def _mark_failed(self, document: KnowledgeDocument, error: str) -> None:
        """Record a failed attempt without destroying the last successful index.

        Old chunks, embedding_model, and indexed_at are preserved so that the
        previous valid index remains intact until a new successful index replaces
        it.
        """
        document.indexing_status = IndexingStatus.FAILED
        document.last_index_error = error[:1000]
        document.save(update_fields=["indexing_status", "last_index_error", "updated_at"])
