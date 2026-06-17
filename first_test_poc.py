from __future__ import annotations

import argparse
import os
from typing import Any

import requests
from dotenv import load_dotenv


RECENT_SEARCH_URL = "https://api.x.com/2/tweets/search/recent"
MIN_API_RESULTS = 10
MAX_API_RESULTS = 100


def clamp_api_max_results(value: int) -> int:
    """Keep max_results inside the range accepted by X recent search."""
    return max(MIN_API_RESULTS, min(value, MAX_API_RESULTS))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="POC simples da API X recent search.")
    parser.add_argument("--term", default="Palmeiras", help="Termo de busca.")
    parser.add_argument("--language", default="pt", help="Filtro de idioma.")
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Quantidade de tweets para mostrar. A API sempre busca pelo menos 10.",
    )
    parser.add_argument(
        "--include-retweets",
        action="store_true",
        help="Inclui retweets na busca.",
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


def build_query(term: str, language: str, include_retweets: bool) -> str:
    query_parts = [term]
    if language:
        query_parts.append(f"lang:{language}")
    if not include_retweets:
        query_parts.append("-is:retweet")
    return " ".join(query_parts)


def search_recent_tweets(
    bearer_token: str,
    query: str,
    display_limit: int,
) -> dict[str, Any]:
    api_max_results = clamp_api_max_results(display_limit)
    params = {
        "query": query,
        "max_results": api_max_results,
        "tweet.fields": "created_at,lang,public_metrics",
    }
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = requests.get(
        RECENT_SEARCH_URL,
        headers=headers,
        params=params,
        timeout=30,
    )
    print(response.status_code)
    print(response.text)
    response.raise_for_status()
    return response.json()


def main() -> None:
    args = parse_args()
    if args.limit < 1:
        raise SystemExit("Use --limit maior ou igual a 1.")

    query = build_query(args.term, args.language, args.include_retweets)
    payload = search_recent_tweets(get_bearer_token(), query, args.limit)

    tweets = payload.get("data", [])
    print(f"\nTweets exibidos: {min(args.limit, len(tweets))}")
    for tweet in tweets[: args.limit]:
        created_at = tweet.get("created_at", "sem_data")
        text = tweet.get("text", "").replace("\n", " ")
        print(f"- [{created_at}] {text}")


if __name__ == "__main__":
    main()
