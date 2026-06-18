"""Text cleaning helpers for the contextual pipeline."""

from __future__ import annotations

import re


URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
WHITESPACE_PATTERN = re.compile(r"\s+")


def clean_reaction_text(text: str) -> str:
    """Normalize text for future PLN steps while preserving semantic content."""
    without_urls = URL_PATTERN.sub("", text)
    return WHITESPACE_PATTERN.sub(" ", without_urls).strip()
