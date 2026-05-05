"""Generate mock football comments."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from queridometro.collectors.mock_collector import save_mock_comments


def main() -> None:
    output_path = save_mock_comments()
    print(f"Mock data saved to {output_path}")


if __name__ == "__main__":
    main()

