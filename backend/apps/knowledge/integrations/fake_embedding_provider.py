"""Deterministic fake embedding provider for automated testing.

Governing documents: SPEC-004 §51.
"""

from __future__ import annotations

import hashlib
import math
import re
from collections.abc import Sequence

from apps.knowledge.services.embedding_provider import EmbeddingError, EmbeddingProvider


class FakeEmbeddingProvider(EmbeddingProvider):
    """Deterministic, network-free embedding provider.

    The provider produces 1024-dimensional vectors from a simple term-hash
    representation. Texts that share words receive more similar vectors,
    supporting controlled retrieval tests without live provider access.
    """

    _DIMENSIONS = 1024
    _HASHES_PER_TOKEN = 3
    _FAILURE_TEXT = "__FAKE_EMBEDDING_FAILURE__"
    model = "fake"

    def __init__(self, dimensions: int = _DIMENSIONS):
        if dimensions != self._DIMENSIONS:
            raise EmbeddingError(
                f"FakeEmbeddingProvider only supports {self._DIMENSIONS} dimensions"
            )
        self.dimensions = dimensions

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """Return deterministic embeddings for the given texts."""
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        """Return a deterministic embedding for the query text."""
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        if text == self._FAILURE_TEXT:
            raise EmbeddingError("Simulated fake embedding failure")

        vector = [0.0] * self.dimensions
        tokens = self._tokenize(text)
        for token in tokens:
            for round_ in range(self._HASHES_PER_TOKEN):
                seed = f"{round_}:{token}".encode()
                digest = hashlib.sha256(seed).digest()
                index = int.from_bytes(digest[:4], "big") % self.dimensions
                value = (int.from_bytes(digest[4:8], "big") % 1000) / 1000.0
                if digest[8] % 2 == 0:
                    value = -value
                vector[index] += value

        return self._normalize(vector)

    def _tokenize(self, text: str) -> list[str]:
        """Return normalized alphanumeric tokens."""
        tokens = re.findall(r"[a-zA-Z0-9\u00C0-\u00FF]+", text.lower())
        return [t for t in tokens if len(t) > 1]

    def _normalize(self, vector: list[float]) -> list[float]:
        """Return an L2-normalized copy of the vector."""
        norm = math.sqrt(sum(v * v for v in vector))
        if norm == 0:
            return [1.0 / self.dimensions] * self.dimensions
        return [v / norm for v in vector]

    @classmethod
    def failure_text(cls) -> str:
        """Return the sentinel text that triggers a controlled failure."""
        return cls._FAILURE_TEXT
