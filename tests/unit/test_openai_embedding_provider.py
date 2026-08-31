"""Behavioral tests for OpenAIEmbeddingProvider retry logic.

Governing documents: SPEC-004 §15–16.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)
from openai._exceptions import httpx2

from apps.knowledge.integrations.openai_embedding_provider import OpenAIEmbeddingProvider
from apps.knowledge.services.embedding_provider import EmbeddingError


def _make_error_response(status_code: int):
    request = httpx2.Request("POST", "https://api.openai.com/v1/embeddings")
    return httpx2.Response(status_code, request=request, text="error")


def _make_embedding_response(vectors: list[list[float]]):
    response = MagicMock()
    response.data = [MagicMock(embedding=v) for v in vectors]
    return response


@pytest.fixture
def provider(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda *_args, **_kwargs: None)
    return OpenAIEmbeddingProvider(api_key="test-key", max_retries=3, timeout=1)


class TestOpenAIRetryBehavior:
    """KB-UT-009 through KB-UT-010: real retry behavior without network."""

    def test_transient_failure_retries_and_succeeds(self, provider, monkeypatch):
        call_count = 0

        def fake_create(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise APIConnectionError(
                    request=httpx2.Request("POST", "https://api.openai.com/v1/embeddings"),
                    message="connection error",
                )
            return _make_embedding_response([[0.1] * 1024])

        monkeypatch.setattr(provider._client.embeddings, "create", fake_create)

        result = provider.embed_query("test query")

        assert call_count == 3
        assert result == [0.1] * 1024

    def test_permanent_failure_does_not_blindly_retry(self, provider, monkeypatch):
        call_count = 0

        def fake_create(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            raise AuthenticationError(
                "invalid key",
                response=_make_error_response(401),
                body=None,
            )

        monkeypatch.setattr(provider._client.embeddings, "create", fake_create)

        with pytest.raises(EmbeddingError, match="OpenAI API error"):
            provider.embed_query("test query")

        assert call_count == 1

    def test_max_transient_retries_bounded(self, provider, monkeypatch):
        call_count = 0

        def fake_create(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            raise RateLimitError(
                "rate limited",
                response=_make_error_response(429),
                body=None,
            )

        monkeypatch.setattr(provider._client.embeddings, "create", fake_create)

        with pytest.raises(EmbeddingError, match="failed after 3 attempts"):
            provider.embed_query("test query")

        assert call_count == 3

    def test_timeout_failure_is_transient_and_retries(self, provider, monkeypatch):
        call_count = 0

        def fake_create(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise APITimeoutError(
                    request=httpx2.Request("POST", "https://api.openai.com/v1/embeddings")
                )
            return _make_embedding_response([[0.2] * 1024, [0.2] * 1024])

        monkeypatch.setattr(provider._client.embeddings, "create", fake_create)

        result = provider.embed_documents(["doc one", "doc two"])

        assert call_count == 2
        assert len(result) == 2
        assert result[0] == [0.2] * 1024

    def test_api_error_response_validation_failure(self, provider, monkeypatch):
        """A successful HTTP response with wrong count raises EmbeddingError."""

        def fake_create(*_args, **_kwargs):
            return _make_embedding_response([[0.3] * 1024])

        monkeypatch.setattr(provider._client.embeddings, "create", fake_create)

        with pytest.raises(EmbeddingError, match="Embedding count mismatch"):
            provider.embed_documents(["one", "two"])

    def test_api_error_response_dimension_validation_failure(self, provider, monkeypatch):
        def fake_create(*_args, **_kwargs):
            return _make_embedding_response([[0.3] * 512])

        monkeypatch.setattr(provider._client.embeddings, "create", fake_create)

        with pytest.raises(EmbeddingError, match="Dimension mismatch"):
            provider.embed_documents(["one"])


class TestOpenAIProviderConfigValidation:
    """Provider configuration sanity checks."""

    def test_invalid_dimensions_rejected(self):
        with pytest.raises(EmbeddingError, match="Configured dimensions"):
            OpenAIEmbeddingProvider(api_key="test-key", dimensions=768)

    def test_zero_max_retries_rejected(self):
        with pytest.raises(EmbeddingError, match="max_retries"):
            OpenAIEmbeddingProvider(api_key="test-key", max_retries=0)

    def test_zero_batch_size_rejected(self):
        with pytest.raises(EmbeddingError, match="batch_size"):
            OpenAIEmbeddingProvider(api_key="test-key", batch_size=0)

    def test_zero_timeout_rejected(self):
        with pytest.raises(EmbeddingError, match="timeout"):
            OpenAIEmbeddingProvider(api_key="test-key", timeout=0)

    def test_missing_api_key_rejected(self, monkeypatch):
        monkeypatch.setattr("django.conf.settings.OPENAI_API_KEY", "")
        with pytest.raises(EmbeddingError, match="OPENAI_API_KEY"):
            OpenAIEmbeddingProvider()
