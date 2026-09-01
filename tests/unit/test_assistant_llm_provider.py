"""Unit tests for the LLMProvider contract and adapters.

Governing documents: SPEC-005 §23–25, §56.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from apps.assistant.integrations.fake_provider import FakeLLMProvider
from apps.assistant.integrations.openai_provider import OpenAILLMProvider
from apps.assistant.services.llm_provider import (
    GenerationInput,
    LLMNonRetryableError,
    LLMResponseError,
    LLMTimeoutError,
    LLMTransientError,
)


@pytest.fixture
def generation_input() -> GenerationInput:
    return GenerationInput(
        system_prompt="You are IA Jujuju.",
        user_question="What is Python?",
        context="[Source 1]\nPython is a language.",
        language="en",
        max_output_tokens=128,
    )


class TestFakeLLMProvider:
    def test_returns_deterministic_content(self, generation_input: GenerationInput) -> None:
        provider = FakeLLMProvider()
        result = provider.generate(generation_input)

        assert "Test answer from IA Jujuju" in result.content
        assert result.model == "fake"

    def test_portuguese_response(self, generation_input: GenerationInput) -> None:
        provider = FakeLLMProvider()
        generation_input = GenerationInput(
            system_prompt="Você é IA Jujuju.",
            user_question="O que é Python?",
            context="",
            language="pt-br",
            max_output_tokens=128,
        )
        result = provider.generate(generation_input)

        assert "Resposta de teste da IA Jujuju" in result.content

    def test_simulated_response_error(self, generation_input: GenerationInput) -> None:
        provider = FakeLLMProvider()
        generation_input = GenerationInput(
            system_prompt="",
            user_question=FakeLLMProvider.failure_text(),
            context="",
            language="en",
            max_output_tokens=128,
        )

        with pytest.raises(LLMResponseError):
            provider.generate(generation_input)

    def test_simulated_timeout_error(self, generation_input: GenerationInput) -> None:
        provider = FakeLLMProvider()
        generation_input = GenerationInput(
            system_prompt="",
            user_question=FakeLLMProvider.timeout_text(),
            context="",
            language="en",
            max_output_tokens=128,
        )

        with pytest.raises(LLMTimeoutError):
            provider.generate(generation_input)

    def test_simulated_transient_error(self, generation_input: GenerationInput) -> None:
        provider = FakeLLMProvider()
        generation_input = GenerationInput(
            system_prompt="",
            user_question=FakeLLMProvider.transient_text(),
            context="",
            language="en",
            max_output_tokens=128,
        )

        with pytest.raises(LLMTransientError):
            provider.generate(generation_input)

    def test_simulated_non_retryable_error(self, generation_input: GenerationInput) -> None:
        provider = FakeLLMProvider()
        generation_input = GenerationInput(
            system_prompt="",
            user_question=FakeLLMProvider.non_retryable_text(),
            context="",
            language="en",
            max_output_tokens=128,
        )

        with pytest.raises(LLMNonRetryableError):
            provider.generate(generation_input)

    def test_simulated_empty_response(self, generation_input: GenerationInput) -> None:
        provider = FakeLLMProvider()
        generation_input = GenerationInput(
            system_prompt="",
            user_question=FakeLLMProvider.empty_text(),
            context="",
            language="en",
            max_output_tokens=128,
        )

        with pytest.raises(LLMResponseError):
            provider.generate(generation_input)

    def test_respects_output_boundary(self, generation_input: GenerationInput) -> None:
        provider = FakeLLMProvider(max_output_tokens=1)
        generation_input = GenerationInput(
            system_prompt="",
            user_question="a " * 1000,
            context="",
            language="en",
            max_output_tokens=1,
        )
        result = provider.generate(generation_input)

        assert len(result.content) <= 8


class TestOpenAILLMProviderConfiguration:
    def test_missing_api_key_raises(self, settings) -> None:
        settings.OPENAI_API_KEY = ""
        with pytest.raises(LLMNonRetryableError, match="OPENAI_API_KEY"):
            OpenAILLMProvider()

    def test_invalid_timeout_raises(self, settings) -> None:
        settings.OPENAI_API_KEY = "test-key"
        with pytest.raises(LLMNonRetryableError, match="timeout"):
            OpenAILLMProvider(timeout=0)

    def test_invalid_retries_raise(self, settings) -> None:
        settings.OPENAI_API_KEY = "test-key"
        with pytest.raises(LLMNonRetryableError, match="max_retries"):
            OpenAILLMProvider(max_retries=0)


class TestOpenAILLMProviderResponseNormalization:
    @pytest.fixture
    def provider(self, settings) -> OpenAILLMProvider:
        settings.OPENAI_API_KEY = "test-key"
        return OpenAILLMProvider(max_retries=1)

    def test_normalizes_successful_response(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        mock_response = MagicMock()
        mock_response.output_text = "  Python is a programming language.  "
        mock_response.model = "gpt-5.6-luna"

        with patch.object(
            provider._client.responses,
            "create",
            return_value=mock_response,
        ):
            result = provider.generate(generation_input)

        assert result.content == "Python is a programming language."
        assert result.model == "gpt-5.6-luna"

    def test_rejects_empty_response(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        mock_response = MagicMock()
        mock_response.output_text = "   "

        with patch.object(
            provider._client.responses,
            "create",
            return_value=mock_response,
        ):
            with pytest.raises(LLMResponseError, match="empty"):
                provider.generate(generation_input)

    def test_rejects_non_textual_response(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        mock_response = MagicMock()
        mock_response.output_text = None

        with patch.object(
            provider._client.responses,
            "create",
            return_value=mock_response,
        ):
            with pytest.raises(LLMResponseError, match="textual"):
                provider.generate(generation_input)

    def test_timeout_classified_as_transient(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        from openai import APITimeoutError

        with patch.object(
            provider._client.responses,
            "create",
            side_effect=APITimeoutError(request=MagicMock()),
        ):
            with pytest.raises(LLMTimeoutError):
                provider.generate(generation_input)

    def test_rate_limit_classified_as_transient(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        from openai import RateLimitError

        with patch.object(
            provider._client.responses,
            "create",
            side_effect=RateLimitError(
                response=MagicMock(status_code=429),
                body=None,
                message="rate limited",
            ),
        ):
            with pytest.raises(LLMTransientError):
                provider.generate(generation_input)

    def test_authentication_not_retried(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        from openai import AuthenticationError

        with patch.object(
            provider._client.responses,
            "create",
            side_effect=AuthenticationError(
                response=MagicMock(status_code=401),
                body=None,
                message="unauthorized",
            ),
        ):
            with pytest.raises(LLMNonRetryableError):
                provider.generate(generation_input)

    def test_bad_request_not_retried(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        from openai import BadRequestError

        with patch.object(
            provider._client.responses,
            "create",
            side_effect=BadRequestError(
                response=MagicMock(status_code=400),
                body=None,
                message="bad request",
            ),
        ):
            with pytest.raises(LLMNonRetryableError):
                provider.generate(generation_input)

    def test_retries_bounded(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        from openai import APIConnectionError

        provider.max_retries = 2
        mock_create = MagicMock(
            side_effect=APIConnectionError(request=MagicMock(), message="connection error")
        )

        with patch.object(provider._client.responses, "create", mock_create):
            with pytest.raises(LLMTransientError):
                provider.generate(generation_input)

        assert mock_create.call_count == 2

    def test_timeout_exhaustion_remains_timeout(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        from openai import APITimeoutError

        provider.max_retries = 2
        mock_create = MagicMock(side_effect=APITimeoutError(request=MagicMock()))

        with patch.object(provider._client.responses, "create", mock_create):
            with pytest.raises(LLMTimeoutError):
                provider.generate(generation_input)

        assert mock_create.call_count == 2

    def test_rate_limit_exhaustion_remains_transient(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        from openai import RateLimitError

        provider.max_retries = 2
        mock_create = MagicMock(
            side_effect=RateLimitError(
                response=MagicMock(status_code=429),
                body=None,
                message="rate limited",
            )
        )

        with patch.object(provider._client.responses, "create", mock_create):
            with pytest.raises(LLMTransientError):
                provider.generate(generation_input)

        assert mock_create.call_count == 2

    def test_5xx_exhaustion_remains_transient(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        from openai import InternalServerError

        provider.max_retries = 2
        mock_create = MagicMock(
            side_effect=InternalServerError(
                message="server error",
                response=MagicMock(status_code=503),
                body=None,
            )
        )

        with patch.object(provider._client.responses, "create", mock_create):
            with pytest.raises(LLMTransientError):
                provider.generate(generation_input)

        assert mock_create.call_count == 2

    def test_context_combined_with_question_exactly_once(
        self,
        provider: OpenAILLMProvider,
    ) -> None:
        input_data = GenerationInput(
            system_prompt="System",
            user_question="Visitor question: What is Python?",
            context="[Source 1]\nPython is a language.",
            language="en",
            max_output_tokens=128,
        )
        mock_response = MagicMock()
        mock_response.output_text = "Answer"
        mock_response.model = "gpt-5.6-luna"

        with patch.object(
            provider._client.responses,
            "create",
            return_value=mock_response,
        ) as mock_create:
            provider.generate(input_data)

        _, kwargs = mock_create.call_args
        user_input = kwargs["input"]
        assert user_input.count("Python is a language") == 1
        assert "Visitor question:" in user_input

    def test_store_disabled(
        self,
        provider: OpenAILLMProvider,
        generation_input: GenerationInput,
    ) -> None:
        mock_response = MagicMock()
        mock_response.output_text = "Answer"
        mock_response.model = "gpt-5.6-luna"

        with patch.object(
            provider._client.responses,
            "create",
            return_value=mock_response,
        ) as mock_create:
            provider.generate(generation_input)

        _, kwargs = mock_create.call_args
        assert kwargs.get("store") is False
        assert kwargs.get("stream") is False
