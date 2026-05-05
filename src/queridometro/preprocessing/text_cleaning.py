"""Text cleaning functions for short football comments."""

from __future__ import annotations

import re

import pandas as pd

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
MENTION_PATTERN = re.compile(r"(?<!\w)@\w+")
WHITESPACE_PATTERN = re.compile(r"\s+")
EMOJI_REPLACEMENTS = {
    "😂": " risada ",
    "🤣": " risada ",
    "😭": " choro ",
    "🔥": " fogo ",
    "👏": " aplausos ",
    "❤️": " amor ",
    "❤": " amor ",
}


def lowercase_text(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


def remove_urls(text: str) -> str:
    """Remove URLs from text."""
    return URL_PATTERN.sub(" ", text)


def remove_mentions(text: str) -> str:
    """Remove @mentions while preserving hashtags."""
    return MENTION_PATTERN.sub(" ", text)


def replace_simple_emojis(text: str) -> str:
    """Replace a small set of common emojis with textual tokens."""
    cleaned = text
    for emoji, replacement in EMOJI_REPLACEMENTS.items():
        cleaned = cleaned.replace(emoji, replacement)
    return cleaned


def normalize_whitespace(text: str) -> str:
    """Remove line breaks and repeated spaces."""
    return WHITESPACE_PATTERN.sub(" ", text.replace("\n", " ")).strip()


def clean_text(text: str) -> str:
    """Apply the project text cleaning pipeline."""
    if not isinstance(text, str):
        return ""

    cleaned = lowercase_text(text)
    cleaned = remove_urls(cleaned)
    cleaned = remove_mentions(cleaned)
    cleaned = replace_simple_emojis(cleaned)
    cleaned = normalize_whitespace(cleaned)
    return cleaned


def add_clean_text_column(df: pd.DataFrame, source_column: str = "text") -> pd.DataFrame:
    """Return a copy of the DataFrame with a clean_text column."""
    if source_column not in df.columns:
        raise ValueError(f"Column '{source_column}' not found in DataFrame.")

    output = df.copy()
    output["clean_text"] = output[source_column].apply(clean_text)
    return output

