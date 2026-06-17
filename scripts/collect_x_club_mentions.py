"""Collect recent X/Twitter mentions of major Brazilian club accounts.

This script uses the official recent search API and keeps the dataset useful for
NLP and network analysis while avoiding raw user and tweet identifiers in CSVs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from queridometro.collectors.twitter_public_collector import anonymize_post_text


RECENT_SEARCH_URL = "https://api.x.com/2/tweets/search/recent"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw" / "club_mentions_x_api.csv"
DEFAULT_TWEETS_PER_CLUB = 100
MIN_API_RESULTS = 10
MAX_API_RESULTS = 100

CLUB_HANDLES = {
    "Sao Paulo": "@SaoPauloFC",
    "Corinthians": "@Corinthians",
    "Palmeiras": "@Palmeiras",
    "Flamengo": "@Flamengo",
    "Vasco": "@VascodaGama",
    "Fluminense": "@FluminenseFC",
    "Botafogo": "@Botafogo",
    "Santos": "@SantosFC",
    "Atletico Mineiro": "@Atletico",
    "Cruzeiro": "@Cruzeiro",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Coleta 100 tweets recentes por arroba oficial dos clubes."
    )
    parser.add_argument(
        "--tweets-per-club",
        type=int,
        default=DEFAULT_TWEETS_PER_CLUB,
        help="Quantidade de tweets por clube. A API aceita de 10 a 100 por chamada.",
    )
    parser.add_argument("--language", default="pt", help="Filtro de idioma.")
    parser.add_argument(
        "--include-retweets",
        action="store_true",
        help="Inclui retweets. Por padrao, retweets sao removidos.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Caminho do CSV consolidado.",
    )
    parser.add_argument(
        "--show-sample",
        action="store_true",
        help="Mostra uma pequena amostra ao final.",
    )
    return parser.parse_args()


def get_bearer_token() -> str:
    load_dotenv()
    token = os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN")
    if not token:
        raise SystemExit(
            "Defina X_BEARER_TOKEN ou TWITTER_BEARER_TOKEN no arquivo .env."
        )
    return token


def hash_identifier(value: Any) -> str:
    """Create a stable anonymous identifier for tweet/user/network analysis."""
    if value is None:
        return ""
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:16]


def normalize_handle(handle: str) -> str:
    return handle.removeprefix("@").lower()


def build_query(handle: str, language: str, include_retweets: bool) -> str:
    query_parts = [handle]
    if language:
        query_parts.append(f"lang:{language}")
    if not include_retweets:
        query_parts.append("-is:retweet")
    return " ".join(query_parts)


def extract_referenced_tweet(tweet: dict[str, Any]) -> tuple[str, str]:
    referenced = tweet.get("referenced_tweets")
    if not isinstance(referenced, list) or not referenced:
        return "", ""

    first_reference = referenced[0]
    if not isinstance(first_reference, dict):
        return "", ""

    return (
        str(first_reference.get("type", "")),
        hash_identifier(first_reference.get("id")),
    )


def extract_mentions(tweet: dict[str, Any]) -> list[str]:
    entities = tweet.get("entities")
    if not isinstance(entities, dict):
        return []

    mentions = entities.get("mentions")
    if not isinstance(mentions, list):
        return []

    usernames: list[str] = []
    for mention in mentions:
        if not isinstance(mention, dict):
            continue
        username = mention.get("username")
        if isinstance(username, str) and username.strip():
            usernames.append(username.strip())
    return usernames


def split_mentions(usernames: list[str]) -> tuple[list[str], list[str]]:
    club_usernames = {normalize_handle(handle) for handle in CLUB_HANDLES.values()}
    club_mentions: list[str] = []
    user_hashes: list[str] = []

    for username in usernames:
        normalized = username.lower()
        if normalized in club_usernames:
            club_mentions.append(f"@{username}")
        else:
            user_hashes.append(hash_identifier(normalized))

    return sorted(set(club_mentions)), sorted(set(user_hashes))


def public_metrics_json(tweet: dict[str, Any]) -> str:
    metrics = tweet.get("public_metrics")
    if not isinstance(metrics, dict):
        metrics = {}
    return json.dumps(metrics, ensure_ascii=False, sort_keys=True)


def fetch_recent_mentions(
    *,
    bearer_token: str,
    club_name: str,
    club_handle: str,
    tweets_per_club: int,
    language: str,
    include_retweets: bool,
    collected_at: str,
) -> list[dict[str, Any]]:
    api_max_results = max(MIN_API_RESULTS, min(tweets_per_club, MAX_API_RESULTS))
    params = {
        "query": build_query(club_handle, language, include_retweets),
        "max_results": api_max_results,
        "tweet.fields": (
            "author_id,conversation_id,created_at,entities,lang,"
            "public_metrics,referenced_tweets"
        ),
    }
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = requests.get(
        RECENT_SEARCH_URL,
        headers=headers,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    payload = response.json()
    tweets = payload.get("data", [])
    if not isinstance(tweets, list):
        return []

    rows: list[dict[str, Any]] = []
    for tweet in tweets[:tweets_per_club]:
        if not isinstance(tweet, dict):
            continue

        reference_type, referenced_tweet_id_hash = extract_referenced_tweet(tweet)
        club_mentions, mentioned_user_hashes = split_mentions(extract_mentions(tweet))
        metrics = tweet.get("public_metrics") if isinstance(tweet, dict) else {}

        rows.append(
            {
                "club_name": club_name,
                "club_handle": club_handle,
                "search_query": params["query"],
                "tweet_id_hash": hash_identifier(tweet.get("id")),
                "conversation_id_hash": hash_identifier(tweet.get("conversation_id")),
                "author_id_hash": hash_identifier(tweet.get("author_id")),
                "created_at": tweet.get("created_at", ""),
                "lang": tweet.get("lang", ""),
                "text": anonymize_post_text(str(tweet.get("text", ""))),
                "reference_type": reference_type,
                "referenced_tweet_id_hash": referenced_tweet_id_hash,
                "mentioned_club_handles": "|".join(club_mentions),
                "mentioned_user_hashes": "|".join(mentioned_user_hashes),
                "retweet_count": int(metrics.get("retweet_count", 0))
                if isinstance(metrics, dict)
                else 0,
                "reply_count": int(metrics.get("reply_count", 0))
                if isinstance(metrics, dict)
                else 0,
                "like_count": int(metrics.get("like_count", 0))
                if isinstance(metrics, dict)
                else 0,
                "quote_count": int(metrics.get("quote_count", 0))
                if isinstance(metrics, dict)
                else 0,
                "bookmark_count": int(metrics.get("bookmark_count", 0))
                if isinstance(metrics, dict)
                else 0,
                "impression_count": int(metrics.get("impression_count", 0))
                if isinstance(metrics, dict)
                else 0,
                "public_metrics_json": public_metrics_json(tweet),
                "source": "x_api_recent_search",
                "collected_at": collected_at,
            }
        )

    return rows


def main() -> None:
    args = parse_args()
    if not MIN_API_RESULTS <= args.tweets_per_club <= MAX_API_RESULTS:
        raise SystemExit("Use --tweets-per-club entre 10 e 100.")

    bearer_token = get_bearer_token()
    collected_at = datetime.now(UTC).isoformat(timespec="seconds")
    all_rows: list[dict[str, Any]] = []

    print("Coleta X API recent search por arroba oficial")
    print(f"Clubes: {len(CLUB_HANDLES)}")
    print(f"Tweets por clube: {args.tweets_per_club}")
    print(f"Saida: {args.output}")

    for club_name, club_handle in CLUB_HANDLES.items():
        try:
            rows = fetch_recent_mentions(
                bearer_token=bearer_token,
                club_name=club_name,
                club_handle=club_handle,
                tweets_per_club=args.tweets_per_club,
                language=args.language,
                include_retweets=args.include_retweets,
                collected_at=collected_at,
            )
        except requests.HTTPError as exc:
            response = exc.response
            detail = response.text if response is not None else str(exc)
            print(f"[ERRO] {club_handle}: {detail}")
            continue
        except requests.RequestException as exc:
            print(f"[ERRO] {club_handle}: {exc}")
            continue

        all_rows.extend(rows)
        print(f"[OK] {club_handle}: {len(rows)} tweets")

    columns = [
        "club_name",
        "club_handle",
        "search_query",
        "tweet_id_hash",
        "conversation_id_hash",
        "author_id_hash",
        "created_at",
        "lang",
        "text",
        "reference_type",
        "referenced_tweet_id_hash",
        "mentioned_club_handles",
        "mentioned_user_hashes",
        "retweet_count",
        "reply_count",
        "like_count",
        "quote_count",
        "bookmark_count",
        "impression_count",
        "public_metrics_json",
        "source",
        "collected_at",
    ]
    df = pd.DataFrame(all_rows, columns=columns)

    if df.empty:
        raise SystemExit(
            "\nNenhum tweet foi coletado. Confira conexao, token, plano da API "
            "e mensagens de erro acima. CSV nao foi sobrescrito."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False, encoding="utf-8-sig")

    print(f"\nTotal coletado: {len(df)} tweets")
    print(f"CSV salvo em: {args.output}")

    if args.show_sample and not df.empty:
        print("\nAmostra:")
        for row in df[["club_handle", "created_at", "text"]].head(5).itertuples():
            print(f"- {row.club_handle} [{row.created_at}] {row.text[:180]}")


if __name__ == "__main__":
    main()
