"""Deterministic knowledge content chunking.

Governing documents: SPEC-004 §17.
"""

from __future__ import annotations

import re

from apps.knowledge.services.normalization import normalize_text


class Chunker:
    """Split normalized knowledge content into deterministic chunks.

    The chunker is paragraph-aware and sentence-boundary-aware where practical.
    If a single sentence exceeds the target size, it is split on word boundaries
    as a deterministic fallback. No whitespace-only chunks are emitted.
    """

    def __init__(self, target_size: int = 1200, overlap_size: int = 150):
        self.target_size = target_size
        self.overlap_size = overlap_size

    def chunk(self, text: str) -> list[str]:
        """Return deterministic, non-empty chunks for the given source text."""
        normalized = normalize_text(text)
        if not normalized:
            return []

        paragraphs = [p.strip() for p in normalized.split("\n\n") if p.strip()]
        if not paragraphs:
            return []

        raw_chunks = self._group_paragraphs(paragraphs)
        final_chunks: list[str] = []
        for raw in raw_chunks:
            final_chunks.extend(self._split_at_sentence_boundaries(raw))

        if not final_chunks:
            return []

        chunks = [final_chunks[0]]
        for chunk in final_chunks[1:]:
            overlap = self._compute_overlap(chunks[-1])
            chunks.append(f"{overlap}\n\n{chunk}" if overlap else chunk)

        return [c.strip() for c in chunks if c.strip()]

    def _group_paragraphs(self, paragraphs: list[str]) -> list[str]:
        """Group paragraphs into chunks that fit within target_size."""
        groups: list[str] = []
        current: list[str] = []
        current_length = 0

        for paragraph in paragraphs:
            para_len = len(paragraph)
            added_length = para_len if not current else para_len + 2  # "\n\n"
            if current and current_length + added_length > self.target_size:
                groups.append("\n\n".join(current))
                current = [paragraph]
                current_length = para_len
            else:
                current.append(paragraph)
                current_length += added_length

        if current:
            groups.append("\n\n".join(current))

        return groups

    def _split_at_sentence_boundaries(self, text: str) -> list[str]:
        """Split text at sentence boundaries, falling back to words if needed."""
        if len(text) <= self.target_size:
            return [text]

        sentences = self._split_sentences(text)
        pieces: list[str] = []
        for sentence in sentences:
            if len(sentence) <= self.target_size:
                pieces.append(sentence)
            else:
                pieces.extend(self._split_oversized(sentence))

        chunks: list[str] = []
        current = ""
        for piece in pieces:
            candidate = f"{current} {piece}".strip() if current else piece
            if len(candidate) > self.target_size and current:
                chunks.append(current)
                current = piece
            else:
                current = candidate

        if current.strip():
            chunks.append(current.strip())

        return chunks

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences preserving terminators."""
        parts = re.split(r"(?<=[.!?])\s+", text)
        return [p.strip() for p in parts if p.strip()]

    def _split_oversized(self, text: str) -> list[str]:
        """Split an oversized sentence on word boundaries deterministically."""
        words = text.split()
        chunks: list[str] = []
        current = ""

        for word in words:
            candidate = f"{current} {word}".strip() if current else word
            if len(candidate) > self.target_size and current:
                chunks.append(current)
                current = word
            else:
                current = candidate

        if current.strip():
            chunks.append(current.strip())

        # If a single word is still larger than target_size, split it by characters.
        final_chunks: list[str] = []
        for chunk in chunks:
            if len(chunk) <= self.target_size:
                final_chunks.append(chunk)
            else:
                final_chunks.extend(self._split_by_character(chunk))

        return final_chunks

    def _split_by_character(self, text: str) -> list[str]:
        """Last-resort deterministic split by characters."""
        return [
            text[i : i + self.target_size].strip()
            for i in range(0, len(text), self.target_size)
            if text[i : i + self.target_size].strip()
        ]

    def _compute_overlap(self, previous_chunk: str) -> str:
        """Return text from the previous chunk to prepend for continuity."""
        sentences = self._split_sentences(previous_chunk)
        overlap = ""
        for sentence in reversed(sentences):
            candidate = f"{sentence} {overlap}".strip() if overlap else sentence
            if len(candidate) <= self.overlap_size:
                overlap = candidate
            else:
                break
        if overlap:
            return overlap

        if len(previous_chunk) <= self.overlap_size:
            return previous_chunk
        return previous_chunk[-self.overlap_size :].strip()


def chunk_text(text: str, *, target_size: int = 1200, overlap_size: int = 150) -> list[str]:
    """Module-level convenience wrapper for content chunking."""
    return Chunker(target_size=target_size, overlap_size=overlap_size).chunk(text)
