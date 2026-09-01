"""Application-owned LLM generation-provider contract.

Governing documents: ADR-007 §7, §23; SPEC-005 §23.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class LLMProviderError(Exception):
    """Base class for provider-independent generation failures."""


class LLMTransientError(LLMProviderError):
    """Failure that may be safe to retry (timeout, temporary unavailability)."""


class LLMTimeoutError(LLMTransientError):
    """Provider call exceeded the configured timeout."""


class LLMNonRetryableError(LLMProviderError):
    """Failure that should not be blindly retried."""


class LLMResponseError(LLMNonRetryableError):
    """Provider returned a malformed or unusable response."""


@dataclass(frozen=True)
class GenerationInput:
    """Structured input crossing the LLMProvider boundary."""

    system_prompt: str
    user_question: str
    context: str
    language: str
    max_output_tokens: int


@dataclass(frozen=True)
class GenerationResult:
    """Application-owned provider generation result."""

    content: str
    model: str
    finish_reason: str | None = None


class LLMProvider(Protocol):
    """Contract for LLM text generation."""

    def generate(self, input_data: GenerationInput) -> GenerationResult:
        """Generate a textual response from the provider."""
        ...
