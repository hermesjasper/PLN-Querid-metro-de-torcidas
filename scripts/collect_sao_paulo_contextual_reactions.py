"""Collect replies and quote tweets for saved Sao Paulo official posts.

The script reads `official_posts_test_sao_paulo.csv`, uses each saved
`post_id`, and writes `post_reactions_test_sao_paulo.csv`. It saves every
reaction returned by each paid API request.
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
    clamp_recent_search_limit,
    fetch_quote_tweets,
    fetch_replies,
    save_collection_log,
)


DEFAULT_OFFICIAL_POSTS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "official_posts_test_sao_paulo.csv"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "post_reactions_test_sao_paulo.csv"
)
DEFAULT_LOG = PROJECT_ROOT / "data" / "metadata" / "collection_log.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Coleta replies e quotes dos posts oficiais salvos do Sao Paulo."
    )
    parser.add_argument("--official-posts", type=Path, default=DEFAULT_OFFICIAL_POSTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument(
        "--max-posts",
        type=int,
        default=2,
        help="Quantidade de posts oficiais a processar neste teste.",
    )
    parser.add_argument(
        "--replies-limit",
        type=int,
        default=10,
        help="max_results para replies por post. Deve ficar entre 10 e 100.",
    )
    parser.add_argument(
        "--quotes-limit",
        type=int,
        default=10,
        help="max_results para quotes por post. Deve ficar entre 10 e 100.",
    )
    return parser.parse_args()


def read_official_posts(path: Path, max_posts: int) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))
    return [row for row in rows if row.get("post_id")][:max_posts]


def write_reactions(rows: list[dict[str, object]], output: Path) -> None:
    columns = [
        "reaction_id",
        "source_reaction_id_hash",
        "parent_post_id",
        "club",
        "reaction_type",
        "author_id_hash",
        "text",
        "created_at",
        "lang",
        "like_count",
        "reply_count",
        "retweet_count",
        "quote_count",
        "collected_at",
        "clean_text",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def log_search(
    *,
    log_path: Path,
    collection_id: str,
    club: str,
    requested_limit: int,
    returned_count: int,
    notes: str,
) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    save_collection_log(
        collection_id=collection_id,
        date=now,
        club=club,
        endpoint=RECENT_SEARCH_URL,
        requested_limit=requested_limit,
        returned_count=returned_count,
        estimated_cost="A_DEFINIR",
        status="success",
        notes=notes,
        log_path=log_path,
    )


def main() -> None:
    args = parse_args()
    official_posts = read_official_posts(args.official_posts, args.max_posts)
    all_reactions: list[dict[str, object]] = []

    replies_limit = clamp_recent_search_limit(args.replies_limit)
    quotes_limit = clamp_recent_search_limit(args.quotes_limit)

    for official_post in official_posts:
        parent_post_id = str(official_post["post_id"])

        replies = fetch_replies(parent_post_id, replies_limit)
        all_reactions.extend(replies)
        log_search(
            log_path=args.log,
            collection_id=f"sao-paulo-replies-{parent_post_id}",
            club="Sao Paulo",
            requested_limit=replies_limit,
            returned_count=len(replies),
            notes=(
                f"query=in_reply_to_tweet_id:{parent_post_id} "
                "-from:SaoPauloFC -is:retweet; saved_all_returned=true."
            ),
        )

        quotes = fetch_quote_tweets(parent_post_id, quotes_limit)
        all_reactions.extend(quotes)
        log_search(
            log_path=args.log,
            collection_id=f"sao-paulo-quotes-{parent_post_id}",
            club="Sao Paulo",
            requested_limit=quotes_limit,
            returned_count=len(quotes),
            notes=(
                f"query=quotes_of_tweet_id:{parent_post_id} -is:retweet; "
                "saved_all_returned=true."
            ),
        )

    write_reactions(all_reactions, args.output)
    print(f"Posts oficiais processados: {len(official_posts)}")
    print(f"Reacoes coletadas: {len(all_reactions)}")
    print(f"CSV salvo em: {args.output}")
    print(f"Log atualizado em: {args.log}")


if __name__ == "__main__":
    main()
