"""Preprocess collected or simulated comments."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from queridometro.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from queridometro.preprocessing.text_cleaning import add_clean_text_column
from queridometro.utils.io import read_csv, write_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess football comments CSV.")
    parser.add_argument(
        "--input",
        type=Path,
        default=RAW_DATA_DIR / "mock_comments.csv",
        help="Input CSV path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROCESSED_DATA_DIR / "mock_comments_clean.csv",
        help="Output CSV path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = read_csv(args.input)
    cleaned_df = add_clean_text_column(df)
    output_path = write_csv(cleaned_df, args.output)
    print(f"Preprocessed data saved to {output_path}")


if __name__ == "__main__":
    main()

