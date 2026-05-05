"""Helpers for creating manual sentiment-labeling templates."""

from __future__ import annotations

import pandas as pd

ALLOWED_LABELS = ["positivo", "negativo", "neutro", "provocativo/ironico"]


def create_labeling_template(df: pd.DataFrame) -> pd.DataFrame:
    """Create a manual labeling table with empty label and notes columns."""
    columns = ["text"]
    if "clean_text" in df.columns:
        columns.append("clean_text")
    if "search_term" in df.columns:
        columns.append("search_term")

    template = df[columns].copy()
    template["label"] = ""
    template["notes"] = ""
    return template

