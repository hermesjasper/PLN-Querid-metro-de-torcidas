"""Collect a Sao Paulo official-post sample with X recent search.

This is the first controlled contextual collection test. It calls
`/2/tweets/search/recent` with `from:SaoPauloFC -is:retweet` and saves every
Post returned by the paid request.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from queridometro.collectors.contextual_x_collector import (
    RECENT_SEARCH_URL,
    build_collection_plan,
    clamp_recent_search_limit,
    fetch_official_posts,
    save_collection_log,
)


DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "official_posts_test_sao_paulo.csv"
)
DEFAULT_LOG = PROJECT_ROOT / "data" / "metadata" / "collection_log.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Teste pequeno de coleta oficial do Sao Paulo via recent search."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Resultados solicitados a API. Deve ficar entre 10 e 100.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    return parser.parse_args()


def write_rows(rows: list[dict[str, object]], output: Path) -> None:
    columns = [
        "post_id",
        "post_id_hash",
        "conversation_id",
        "club",
        "club_username",
        "official_text",
        "created_at",
        "lang",
        "like_count",
        "reply_count",
        "retweet_count",
        "quote_count",
        "collected_at",
        "post_type_llm",
        "post_type_manual",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.limit < 1:
        raise SystemExit("Use --limit maior ou igual a 1.")

    plan = build_collection_plan(
        club="Sao Paulo",
        club_username="SaoPauloFC",
    )
    plan = plan.__class__(
        club=plan.club,
        club_username=plan.club_username,
        official_posts_limit=args.limit,
        replies_per_post_limit=plan.replies_per_post_limit,
        quotes_per_post_limit=plan.quotes_per_post_limit,
        max_estimated_cost_brl=plan.max_estimated_cost_brl,
    )

    rows = fetch_official_posts(plan)
    write_rows(rows, args.output)

    now = datetime.now(UTC).isoformat(timespec="seconds")
    requested_limit = clamp_recent_search_limit(args.limit)
    save_collection_log(
        collection_id=f"sao-paulo-official-posts-test-{now}",
        date=now,
        club=plan.club,
        endpoint=RECENT_SEARCH_URL,
        requested_limit=requested_limit,
        returned_count=len(rows),
        estimated_cost="A_DEFINIR",
        status="success",
        notes=(
            "Teste inicial autorizado: query=from:SaoPauloFC -is:retweet; "
            f"API max_results={requested_limit}; saved_all_returned=true."
        ),
        log_path=args.log,
    )

    print(f"Coletados: {len(rows)} posts oficiais")
    print(f"CSV salvo em: {args.output}")
    print(f"Log atualizado em: {args.log}")


if __name__ == "__main__":
    main()
