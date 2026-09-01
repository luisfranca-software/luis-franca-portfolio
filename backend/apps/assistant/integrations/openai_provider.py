"""OpenAI Responses API adapter for the LLMProvider contract.

Governing documents: ADR-007 §8, §24; SPEC-005 §24.
"""

from __future__ import annotations

import logging
import time
from typing import cast

from django.conf import settings
from openai import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    OpenAI,
    PermissionDeniedError,
    RateLimitError,
)

from apps.assistant.services.llm_provider import (
    GenerationInput,
    GenerationResult,
    LLMNonRetryableError,
    LLMProviderError,
    LLMResponseError,
    LLMTimeoutError,
    LLMTransientError,
)

logger = logging.getLogger(__name__)


class OpenAILLMProvider:
    """Production OpenAI adapter implementing the application LLMProvider contract."""

    _DEFAULT_MODEL = "gpt-5.6-luna"
    _DEFAULT_TIMEOUT = 30.0
    _DEFAULT_MAX_RETRIES = 3
    _DEFAULT_MAX_OUTPUT_TOKENS = 512

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        max_output_tokens: int | None = None,
    ) -> None:
        self.api_key = (
            api_key if api_key is not None else cast(str, getattr(settings, "OPENAI_API_KEY", ""))
        )
        self.model = (
            model
            if model is not None
            else cast(str, getattr(settings, "ASSISTANT_MODEL", self._DEFAULT_MODEL))
        )
        self.timeout = (
            timeout
            if timeout is not None
            else cast(
                float,
                getattr(settings, "ASSISTANT_OPENAI_TIMEOUT", self._DEFAULT_TIMEOUT),
            )
        )
        self.max_retries = (
            max_retries
            if max_retries is not None
            else cast(
                int,
                getattr(settings, "ASSISTANT_OPENAI_MAX_RETRIES", self._DEFAULT_MAX_RETRIES),
            )
        )
        self.max_output_tokens = (
            max_output_tokens
            if max_output_tokens is not None
            else cast(
                int,
                getattr(
                    settings,
                    "ASSISTANT_MAX_OUTPUT_TOKENS",
                    self._DEFAULT_MAX_OUTPUT_TOKENS,
                ),
            )
        )

        if not self.api_key:
            raise LLMNonRetryableError("OPENAI_API_KEY is not configured")
        if self.timeout <= 0:
            raise LLMNonRetryableError("timeout must be greater than 0")
        if self.max_retries < 1:
            raise LLMNonRetryableError("max_retries must be at least 1")
        if self.max_output_tokens < 1:
            raise LLMNonRetryableError("max_output_tokens must be at least 1")

        self._client = OpenAI(
            api_key=self.api_key,
            timeout=self.timeout,
            max_retries=0,  # Application controls retry classification.
        )

    def generate(self, input_data: GenerationInput) -> GenerationResult:
        """Call OpenAI Responses API with bounded retries."""
        user_input = self._build_user_input(input_data)
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self._client.responses.create(
                    model=self.model,
                    instructions=input_data.system_prompt,
                    input=user_input,
                    max_output_tokens=self.max_output_tokens,
                    timeout=self.timeout,
                    stream=False,
                    store=False,
                )
                return self._normalize_response(response)
            except LLMProviderError:
                raise
            except APITimeoutError as exc:
                last_error = exc
                logger.warning(
                    "OpenAI generation timeout (attempt %s/%s)",
                    attempt,
                    self.max_retries,
                )
                if attempt < self.max_retries:
                    time.sleep(0.5 * (2 ** (attempt - 1)))
            except (APIConnectionError, RateLimitError) as exc:
                last_error = exc
                logger.warning(
                    "OpenAI generation transient failure (attempt %s/%s): %s",
                    attempt,
                    self.max_retries,
                    exc.__class__.__name__,
                )
                if attempt < self.max_retries:
                    time.sleep(0.5 * (2 ** (attempt - 1)))
            except (AuthenticationError, PermissionDeniedError, BadRequestError) as exc:
                logger.warning(
                    "OpenAI generation non-retryable error: %s",
                    exc.__class__.__name__,
                )
                raise LLMNonRetryableError(
                    f"OpenAI request rejected: {exc.__class__.__name__}"
                ) from exc
            except APIError as exc:
                logger.warning(
                    "OpenAI generation API error: %s (status %s)",
                    exc.__class__.__name__,
                    getattr(exc, "status_code", "unknown"),
                )
                # 5xx class errors may be transient; everything else is not retried.
                status = getattr(exc, "status_code", None)
                if status is not None and status >= 500:
                    last_error = exc
                    if attempt < self.max_retries:
                        time.sleep(0.5 * (2 ** (attempt - 1)))
                    continue
                raise LLMNonRetryableError(f"OpenAI API error: {exc.__class__.__name__}") from exc
            except Exception as exc:
                logger.warning(
                    "OpenAI generation unexpected error: %s",
                    exc.__class__.__name__,
                )
                raise LLMProviderError(
                    f"Unexpected OpenAI error: {exc.__class__.__name__}"
                ) from exc

        if isinstance(last_error, APITimeoutError):
            raise LLMTimeoutError(
                f"OpenAI generation failed after {self.max_retries} attempts"
            ) from last_error
        raise LLMTransientError(
            f"OpenAI generation failed after {self.max_retries} attempts"
        ) from last_error

    def _build_user_input(self, input_data: GenerationInput) -> str:
        """Combine controlled context and user question for the provider input.

        The context is carried separately from the question so that prompt rules
        remain owned by the application layer and the context appears exactly once.
        """
        parts: list[str] = []
        if input_data.context:
            parts.append(input_data.context)
        parts.append(input_data.user_question)
        return "\n\n".join(parts)

    def _normalize_response(self, response) -> GenerationResult:
        """Validate and convert an OpenAI Response to an application-owned result."""
        output_text = getattr(response, "output_text", None)
        if not isinstance(output_text, str):
            raise LLMResponseError("OpenAI response did not contain textual output")
        content = output_text.strip()
        if not content:
            raise LLMResponseError("OpenAI returned an empty response")
        if len(content) > self.max_output_tokens * 8:
            # Rough conservative boundary; the provider should already enforce tokens.
            raise LLMResponseError("OpenAI response exceeded application output boundary")
        return GenerationResult(
            content=content,
            model=getattr(response, "model", self.model),
            finish_reason=None,
        )
