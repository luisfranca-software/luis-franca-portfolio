"""Knowledge semantic retrieval service.

Governing documents: ADR-006 §11, SPEC-004 §28–36.
"""

from __future__ import annotations

from dataclasses import dataclass

from pgvector.django import CosineDistance

from apps.knowledge.models import Category, KnowledgeChunk, Language
from apps.knowledge.services.embedding_provider import EmbeddingProvider


@dataclass(frozen=True)
class RetrievalResult:
    """Structured result for downstream controlled-context construction."""

    chunk_id: int
    document_id: int
    document_title: str
    document_slug: str
    content: str
    distance: float
    language: str
    category: str


class RetrievalService:
    """Metadata-constrained exact cosine retrieval over KnowledgeChunk."""

    _DEFAULT_TOP_K = 5
    _MAX_TOP_K = 100

    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    def retrieve(
        self,
        query: str,
        language: str,
        *,
        category: str | None = None,
        top_k: int = _DEFAULT_TOP_K,
    ) -> list[RetrievalResult]:
        """Return top-k chunks eligible for the given query and filters."""
        if not query or not query.strip():
            return []
        if not language:
            return []
        if top_k < 1:
            return []
        top_k = min(top_k, self._MAX_TOP_K)

        if language not in Language.values:
            raise ValueError(f"Unsupported language: {language}")
        if category is not None and category not in Category.values:
            raise ValueError(f"Unsupported category: {category}")

        query_embedding = self.provider.embed_query(query)
        if len(query_embedding) != 1024:
            raise ValueError("Query embedding dimensions do not match schema")

        qs = (
            KnowledgeChunk.objects.filter(
                document__is_active=True,
                document__indexed_at__isnull=False,
                document__language=language,
            )
            .annotate(distance=CosineDistance("embedding", query_embedding))
            .order_by("distance")
        )

        if category:
            qs = qs.filter(document__category=category)

        return [
            RetrievalResult(
                chunk_id=chunk.pk,
                document_id=chunk.document.pk,
                document_title=chunk.document.title,
                document_slug=chunk.document.slug,
                content=chunk.content,
                distance=float(chunk.distance),
                language=chunk.document.language,
                category=chunk.document.category,
            )
            for chunk in qs[:top_k]
        ]
