"""OpenAI embedding provider integration.

Governing documents: ADR-006 §9.3, SPEC-004 §14.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Sequence
from typing import cast

from django.conf import settings
from openai import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    OpenAI,
    RateLimitError,
)

from apps.knowledge.services.embedding_provider import EmbeddingError, EmbeddingProvider

logger = logging.getLogger(__name__)


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI adapter implementing the application EmbeddingProvider contract."""

    _DEFAULT_MODEL = "text-embedding-3-small"
    _DEFAULT_DIMENSIONS = 1024
    _DEFAULT_TIMEOUT = 30.0
    _DEFAULT_MAX_RETRIES = 3
    _DEFAULT_BATCH_SIZE = 32

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        dimensions: int | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        batch_size: int | None = None,
    ) -> None:
        self.api_key = (
            api_key if api_key is not None else cast(str, getattr(settings, "OPENAI_API_KEY", ""))
        )
        self.model = (
            model
            if model is not None
            else cast(str, getattr(settings, "KNOWLEDGE_EMBEDDING_MODEL", self._DEFAULT_MODEL))
        )
        self.dimensions = (
            dimensions
            if dimensions is not None
            else cast(
                int,
                getattr(settings, "KNOWLEDGE_EMBEDDING_DIMENSIONS", self._DEFAULT_DIMENSIONS),
            )
        )
        self.timeout = (
            timeout
            if timeout is not None
            else cast(
                float,
                getattr(settings, "KNOWLEDGE_OPENAI_TIMEOUT", self._DEFAULT_TIMEOUT),
            )
        )
        self.max_retries = (
            max_retries
            if max_retries is not None
            else cast(
                int,
                getattr(settings, "KNOWLEDGE_OPENAI_MAX_RETRIES", self._DEFAULT_MAX_RETRIES),
            )
        )
        self.batch_size = (
            batch_size
            if batch_size is not None
            else cast(
                int,
                getattr(settings, "KNOWLEDGE_OPENAI_BATCH_SIZE", self._DEFAULT_BATCH_SIZE),
            )
        )

        if not self.api_key:
            raise EmbeddingError("OPENAI_API_KEY is not configured")
        if self.dimensions != self._DEFAULT_DIMENSIONS:
            raise EmbeddingError(
                f"Configured dimensions {self.dimensions} do not match "
                f"schema {self._DEFAULT_DIMENSIONS}"
            )
        if self.max_retries < 1:
            raise EmbeddingError("max_retries must be at least 1")
        if self.batch_size < 1:
            raise EmbeddingError("batch_size must be at least 1")
        if self.timeout <= 0:
            raise EmbeddingError("timeout must be greater than 0")

        self._client = OpenAI(
            api_key=self.api_key,
            timeout=self.timeout,
            max_retries=0,  # Application controls retry classification.
        )

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """Return embeddings for document chunks."""
        if not texts:
            return []

        all_embeddings: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = list(texts[i : i + self.batch_size])
            all_embeddings.extend(self._request_embeddings(batch))
        return all_embeddings

    def embed_query(self, text: str) -> list[float]:
        """Return embedding for a retrieval query."""
        embeddings = self._request_embeddings([text])
        return embeddings[0]

    def _request_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Call OpenAI with bounded retries for transient failures."""
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self._client.embeddings.create(
                    input=texts,
                    model=self.model,
                    dimensions=self.dimensions,
                )
                return self._validate_response(texts, response)
            except EmbeddingError:
                # Application validation failures are not retryable.
                raise
            except (APIConnectionError, APITimeoutError, RateLimitError) as exc:
                last_error = exc
                logger.warning(
                    "OpenAI embedding transient failure (attempt %s/%s): %s",
                    attempt,
                    self.max_retries,
                    exc.__class__.__name__,
                )
                if attempt < self.max_retries:
                    time.sleep(0.5 * (2 ** (attempt - 1)))
            except APIError as exc:
                logger.warning(
                    "OpenAI embedding API error: %s",
                    exc.__class__.__name__,
                )
                raise EmbeddingError(f"OpenAI API error: {exc.__class__.__name__}") from exc
            except Exception as exc:
                logger.warning(
                    "OpenAI embedding unexpected error: %s",
                    exc.__class__.__name__,
                )
                raise EmbeddingError(f"Unexpected OpenAI error: {exc.__class__.__name__}") from exc

        raise EmbeddingError(
            f"OpenAI embedding failed after {self.max_retries} attempts"
        ) from last_error

    def _validate_response(
        self,
        texts: list[str],
        response,
    ) -> list[list[float]]:
        """Validate OpenAI response count and dimensions."""
        items = list(response.data)
        if len(items) != len(texts):
            raise EmbeddingError(
                f"Embedding count mismatch: expected {len(texts)}, got {len(items)}"
            )

        embeddings: list[list[float]] = []
        for item in items:
            vector = list(item.embedding)
            if len(vector) != self.dimensions:
                raise EmbeddingError(
                    f"Dimension mismatch: expected {self.dimensions}, got {len(vector)}"
                )
            embeddings.append(vector)

        return embeddings
