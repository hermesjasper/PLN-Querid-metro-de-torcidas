"""Input/output helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_csv(path: Path | str) -> pd.DataFrame:
    """Read a UTF-8 CSV file."""
    return pd.read_csv(path, encoding="utf-8")


def write_csv(df: pd.DataFrame, path: Path | str) -> Path:
    """Write a DataFrame as UTF-8 CSV, creating parent folders as needed."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False, encoding="utf-8")
    return destination

