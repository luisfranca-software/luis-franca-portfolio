"""Application-owned embedding-provider contract.

Governing documents: ADR-006 §9.3, SPEC-004 §13.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol


class EmbeddingError(Exception):
    """Raised when embedding generation fails in a provider-independent way."""


class EmbeddingProvider(Protocol):
    """Contract for embedding chunk and query text."""

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """Return one embedding vector for each input text."""
        ...

    def embed_query(self, text: str) -> list[float]:
        """Return the embedding vector for a retrieval query."""
        ...
