"""Deterministic fake LLM provider for automated testing.

Governing documents: ADR-007 §7, §25; SPEC-005 §25.

This provider is intended for tests only and must never become a production
fallback.
"""

from __future__ import annotations

from apps.assistant.services.llm_provider import (
    GenerationInput,
    GenerationResult,
    LLMNonRetryableError,
    LLMResponseError,
    LLMTimeoutError,
    LLMTransientError,
)


class FakeLLMProvider:
    """Network-free deterministic LLM provider for tests."""

    _FAILURE_TEXT = "__FAKE_LLM_FAILURE__"
    _TIMEOUT_TEXT = "__FAKE_LLM_TIMEOUT__"
    _TRANSIENT_TEXT = "__FAKE_LLM_TRANSIENT__"
    _NON_RETRYABLE_TEXT = "__FAKE_LLM_NON_RETRYABLE__"
    _EMPTY_TEXT = "__FAKE_LLM_EMPTY__"
    model = "fake"

    def __init__(
        self,
        *,
        max_output_tokens: int = 512,
    ) -> None:
        self.max_output_tokens = max_output_tokens

    def generate(self, input_data: GenerationInput) -> GenerationResult:
        """Return deterministic test content or raise controlled failures."""
        question = input_data.user_question

        if self._FAILURE_TEXT in question:
            raise LLMResponseError("Simulated fake LLM failure")
        if self._TIMEOUT_TEXT in question:
            raise LLMTimeoutError("Simulated fake LLM timeout")
        if self._TRANSIENT_TEXT in question:
            raise LLMTransientError("Simulated fake LLM transient failure")
        if self._NON_RETRYABLE_TEXT in question:
            raise LLMNonRetryableError("Simulated fake LLM non-retryable failure")
        if self._EMPTY_TEXT in question:
            raise LLMResponseError("Simulated fake empty response")

        language = input_data.language
        if language == "pt-br":
            prefix = "Resposta de teste da IA Jujuju"
        else:
            prefix = "Test answer from IA Jujuju"

        context_indicator = ""
        if input_data.context:
            context_indicator = " (context present)"

        content = f"{prefix}: {question}{context_indicator}"
        if len(content) > self.max_output_tokens * 8:
            content = content[: self.max_output_tokens * 8]

        return GenerationResult(
            content=content,
            model=self.model,
        )

    @classmethod
    def failure_text(cls) -> str:
        return cls._FAILURE_TEXT

    @classmethod
    def timeout_text(cls) -> str:
        return cls._TIMEOUT_TEXT

    @classmethod
    def transient_text(cls) -> str:
        return cls._TRANSIENT_TEXT

    @classmethod
    def non_retryable_text(cls) -> str:
        return cls._NON_RETRYABLE_TEXT

    @classmethod
    def empty_text(cls) -> str:
        return cls._EMPTY_TEXT
