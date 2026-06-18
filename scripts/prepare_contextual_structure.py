"""Create expected folders for the contextual pipeline.

This helper is safe to run locally. It creates directories only; it does not
collect data, call LLMs or train models.
"""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_DIRS = [
    "data/raw/initial_mentions",
    "data/raw/contextual_collection",
    "data/processed",
    "data/annotated",
    "data/metadata",
    "config",
    "docs",
]


def main() -> None:
    for relative_path in EXPECTED_DIRS:
        path = PROJECT_ROOT / relative_path
        path.mkdir(parents=True, exist_ok=True)
        print(f"ok: {path}")


if __name__ == "__main__":
    main()
