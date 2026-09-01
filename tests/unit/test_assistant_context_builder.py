"""Unit tests for the IA Jujuju context builder.

Governing documents: SPEC-005 §17, §56.
"""

from __future__ import annotations

import pytest

from apps.assistant.services.context_builder import ContextBuilder
from apps.knowledge.services.retrieval import RetrievalResult


def _result(chunk_id: int, content: str, distance: float = 0.1) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        document_id=chunk_id,
        document_title=f"Doc {chunk_id}",
        document_slug=f"doc-{chunk_id}",
        content=content,
        distance=distance,
        language="en",
        category="GENERAL",
    )


def test_empty_results_produce_no_evidence() -> None:
    builder = ContextBuilder()
    context = builder.build([])

    assert context.text == ""
    assert context.items == []
    assert context.has_evidence is False


def test_preserves_retrieval_rank() -> None:
    builder = ContextBuilder()
    context = builder.build(
        [
            _result(1, "First chunk"),
            _result(2, "Second chunk"),
        ]
    )

    assert [item.rank for item in context.items] == [1, 2]
    assert "[Source 1]" in context.text
    assert "[Source 2]" in context.text


def test_removes_empty_chunks() -> None:
    builder = ContextBuilder()
    context = builder.build(
        [
            _result(1, "   "),
            _result(2, "Valid chunk"),
        ]
    )

    assert len(context.items) == 1
    assert context.items[0].content == "Valid chunk"


def test_removes_duplicate_content() -> None:
    builder = ContextBuilder()
    context = builder.build(
        [
            _result(1, "Duplicate content"),
            _result(2, "Duplicate content"),
            _result(3, "Unique content"),
        ]
    )

    assert len(context.items) == 2
    assert context.items[0].content == "Duplicate content"
    assert context.items[1].content == "Unique content"


def test_context_size_boundary_rejects_oversized_first_item() -> None:
    long_content = "word " * 500  # 2500+ characters
    builder = ContextBuilder(max_context_chars=100)
    context = builder.build(
        [
            _result(1, long_content),
            _result(2, "Second"),
        ]
    )

    assert context.items == []
    assert context.text == ""
    assert context.has_evidence is False


def test_context_boundary_keeps_higher_rank_first() -> None:
    builder = ContextBuilder(max_context_chars=15)
    context = builder.build(
        [
            _result(1, "A"),
            _result(2, "B"),
            _result(3, "C"),
        ]
    )

    assert len(context.items) == 1
    assert context.items[0].rank == 1


def test_zero_context_boundary_produces_no_evidence() -> None:
    builder = ContextBuilder(max_context_chars=0)
    context = builder.build(
        [
            _result(1, "First"),
            _result(2, "Second"),
        ]
    )

    assert context.items == []
    assert context.text == ""
    assert context.has_evidence is False


def test_exact_boundary_keeps_item() -> None:
    # "[Source 1]\nA" is exactly 12 characters.
    builder = ContextBuilder(max_context_chars=12)
    context = builder.build([_result(1, "A")])

    assert len(context.items) == 1
    assert context.text == "[Source 1]\nA"


def test_boundary_excludes_item_one_char_over() -> None:
    builder = ContextBuilder(max_context_chars=11)
    context = builder.build([_result(1, "A")])

    assert context.items == []
    assert context.text == ""


def test_multiple_sources_crossing_boundary_keeps_first_fit() -> None:
    builder = ContextBuilder(max_context_chars=30)
    context = builder.build(
        [
            _result(1, "First source"),
            _result(2, "Second source"),
            _result(3, "Third source"),
        ]
    )

    assert len(context.text) <= 30
    assert context.text.count("[Source") == 1
    assert context.items[0].rank == 1


def test_negative_context_size_raises() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        ContextBuilder(max_context_chars=-1)


def test_deterministic_for_equivalent_input() -> None:
    builder = ContextBuilder()
    results = [_result(i, f"Chunk {i}") for i in range(3)]

    first = builder.build(results)
    second = builder.build(results)

    assert first.text == second.text
    assert [item.rank for item in first.items] == [item.rank for item in second.items]


def test_source_boundaries_preserved() -> None:
    builder = ContextBuilder()
    context = builder.build(
        [
            _result(1, "First source text."),
            _result(2, "Second source text."),
        ]
    )

    parts = context.text.split("\n\n")
    assert len(parts) == 2
    assert parts[0].startswith("[Source 1]")
    assert parts[1].startswith("[Source 2]")


def test_final_text_never_exceeds_boundary() -> None:
    builder = ContextBuilder(max_context_chars=50)
    context = builder.build(
        [
            _result(1, "Short"),
            _result(2, "Another short piece"),
            _result(3, "Yet more text here"),
        ]
    )

    assert len(context.text) <= 50
    for item in context.items:
        assert item.content in context.text
