"""Controlled RAG context builder for IA Jujuju.

Governing documents: ADR-007 §10; SPEC-005 §17–18.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.knowledge.services.retrieval import RetrievalResult


@dataclass(frozen=True)
class ContextItem:
    """One bounded source item entering the provider context."""

    rank: int
    content: str
    retrieval_result: RetrievalResult


@dataclass(frozen=True)
class ControlledContext:
    """Application-owned context ready for the prompt builder."""

    text: str
    items: list[ContextItem]
    has_evidence: bool


class ContextBuilder:
    """Transform RetrievalResult values into a bounded, deterministic context."""

    _DEFAULT_MAX_CONTEXT_CHARS = 4000

    def __init__(self, max_context_chars: int | None = None) -> None:
        self.max_context_chars = (
            max_context_chars if max_context_chars is not None else self._DEFAULT_MAX_CONTEXT_CHARS
        )
        if self.max_context_chars < 0:
            raise ValueError("max_context_chars must be non-negative")

    def build(self, results: list[RetrievalResult]) -> ControlledContext:
        """Build a bounded context preserving rank and source boundaries."""
        items: list[ContextItem] = []
        seen_contents: set[str] = set()

        for rank, result in enumerate(results, start=1):
            content = (result.content or "").strip()
            if not content:
                continue
            # Avoid unnecessary duplicates while preserving rank.
            if content in seen_contents:
                continue
            seen_contents.add(content)
            items.append(
                ContextItem(
                    rank=rank,
                    content=content,
                    retrieval_result=result,
                )
            )

        text_parts: list[str] = []
        kept_items: list[ContextItem] = []

        for item in items:
            entry = f"[Source {item.rank}]\n{item.content}"
            candidate = "\n\n".join(text_parts + [entry])
            if len(candidate) > self.max_context_chars:
                # Deterministic boundary: keep higher-ranked evidence; do not split
                # a source boundary through arbitrary partial truncation.
                break
            text_parts.append(entry)
            kept_items.append(item)

        context_text = "\n\n".join(text_parts)
        return ControlledContext(
            text=context_text,
            items=kept_items,
            has_evidence=len(kept_items) > 0,
        )
