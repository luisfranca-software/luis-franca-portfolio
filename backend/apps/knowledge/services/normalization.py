"""Deterministic knowledge content normalization.

Governing documents: SPEC-004 §16.
"""

from __future__ import annotations

import re


class Normalizer:
    """Normalize source knowledge content without rewriting meaning."""

    # Normalize all newline variants to a single \n.
    _NEWLINE_PATTERN = re.compile(r"\r\n|\r")
    # Collapse repeated blank lines to a single blank line.
    _BLANK_LINES_PATTERN = re.compile(r"\n{3,}")
    # Collapse other repeated whitespace to a single space.
    _WHITESPACE_PATTERN = re.compile(r"[ \t]+")

    def normalize(self, text: str) -> str:
        """Return deterministic normalized text preserving semantic content."""
        if not text:
            return ""

        text = self._NEWLINE_PATTERN.sub("\n", text)
        text = self._WHITESPACE_PATTERN.sub(" ", text)
        text = self._BLANK_LINES_PATTERN.sub("\n\n", text)
        return text.strip()


def normalize_text(text: str) -> str:
    """Module-level convenience wrapper for content normalization."""
    return Normalizer().normalize(text)
