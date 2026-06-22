"""Contextual collector for official club posts and reactions.

This module keeps most contextual collection steps as placeholders, but includes
a small controlled test for official club posts using X recent search.

Future collection must respect the cost ceiling described in
`docs/plano_coleta.md` and log every run in `data/metadata/collection_log.csv`.
"""

from __future__ import annotations

import csv
import hashlib
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


DEFAULT_COLLECTION_LOG = Path("data/metadata/collection_log.csv")
RECENT_SEARCH_URL = "https://api.x.com/2/tweets/search/recent"
MIN_RECENT_SEARCH_RESULTS = 10
MAX_RECENT_SEARCH_RESULTS = 100


@dataclass(frozen=True)
class CollectionPlan:
    """Small plan object for a future contextual collection run."""

    club: str = "Sao Paulo"
    club_username: str = "SaoPauloFC"
    official_posts_limit: int = 10
    replies_per_post_limit: int = 30
    quotes_per_post_limit: int = 10
    max_estimated_cost_brl: float = 25.0


def get_club_user_id(club_username: str) -> str:
    """Placeholder for resolving a club username to a platform user ID."""
    raise NotImplementedError(
        "Future step: resolve club username through the X API without running "
        "this placeholder during repository setup."
    )


def fetch_official_posts(plan: CollectionPlan) -> list[dict[str, Any]]:
    """Fetch a small official-post sample through recent search.

    The recent search endpoint requires `max_results` between 10 and 100. The
    function persists every Post returned by the paid request; it does not trim
    successful responses after the API has returned them.
    """
    bearer_token = get_bearer_token()
    requested_limit = clamp_recent_search_limit(plan.official_posts_limit)
    query = f"from:{plan.club_username} -is:retweet"
    params = {
        "query": query,
        "max_results": requested_limit,
        "tweet.fields": "created_at,lang,public_metrics,conversation_id",
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

    collected_at = datetime.now(UTC).isoformat(timespec="seconds")
    return [
        build_official_post_row(tweet, plan, collected_at)
        for tweet in tweets
        if isinstance(tweet, dict)
    ]


def fetch_replies(parent_post_id: str, limit: int) -> list[dict[str, Any]]:
    """Fetch replies associated with one official post via recent search."""
    query = f"in_reply_to_tweet_id:{parent_post_id} -from:SaoPauloFC -is:retweet"
    return fetch_reactions_for_query(
        parent_post_id=parent_post_id,
        reaction_type="REPLY",
        query=query,
        limit=limit,
    )


def fetch_quote_tweets(parent_post_id: str, limit: int) -> list[dict[str, Any]]:
    """Fetch quote tweets associated with one official post via recent search."""
    query = f"quotes_of_tweet_id:{parent_post_id} -is:retweet"
    return fetch_reactions_for_query(
        parent_post_id=parent_post_id,
        reaction_type="QUOTE",
        query=query,
        limit=limit,
    )


def estimate_collection_volume(plan: CollectionPlan) -> int:
    """Estimate maximum records for the planned contextual collection."""
    reactions_per_post = plan.replies_per_post_limit + plan.quotes_per_post_limit
    return plan.official_posts_limit * (1 + reactions_per_post)


def save_collection_log(
    *,
    collection_id: str,
    date: str,
    club: str,
    endpoint: str,
    requested_limit: int,
    returned_count: int,
    estimated_cost: float | str,
    status: str,
    notes: str,
    log_path: Path = DEFAULT_COLLECTION_LOG,
) -> None:
    """Append collection metadata to the log CSV."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "collection_id",
                "date",
                "club",
                "endpoint",
                "requested_limit",
                "returned_count",
                "estimated_cost",
                "status",
                "notes",
            ],
        )
        if not file_exists or log_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(
            {
                "collection_id": collection_id,
                "date": date,
                "club": club,
                "endpoint": endpoint,
                "requested_limit": requested_limit,
                "returned_count": returned_count,
                "estimated_cost": estimated_cost,
                "status": status,
                "notes": notes,
            }
        )


def build_collection_plan(
    club: str = "Sao Paulo",
    club_username: str = "SaoPauloFC",
) -> CollectionPlan:
    """Return the default low-cost plan for the next collection stage."""
    return CollectionPlan(club=club, club_username=club_username)


def get_bearer_token() -> str:
    """Load the local X API bearer token for an authorized test collection."""
    load_dotenv()
    token = os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN")
    if not token:
        raise RuntimeError("Defina X_BEARER_TOKEN ou TWITTER_BEARER_TOKEN no .env.")
    return token


def clamp_recent_search_limit(limit: int) -> int:
    """Clamp recent search max_results to the range required by X."""
    return max(MIN_RECENT_SEARCH_RESULTS, min(limit, MAX_RECENT_SEARCH_RESULTS))


def stable_hash(value: Any) -> str:
    """Create a stable short hash for IDs persisted in CSV outputs."""
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:16]


def build_official_post_row(
    tweet: dict[str, Any],
    plan: CollectionPlan,
    collected_at: str,
) -> dict[str, Any]:
    """Normalize one X API tweet object into the planned official_posts schema."""
    metrics = tweet.get("public_metrics")
    if not isinstance(metrics, dict):
        metrics = {}

    return {
        "post_id": str(tweet.get("id", "")),
        "post_id_hash": stable_hash(tweet.get("id", "")),
        "conversation_id": str(tweet.get("conversation_id", "")),
        "club": plan.club,
        "club_username": plan.club_username,
        "official_text": " ".join(str(tweet.get("text", "")).split()),
        "created_at": tweet.get("created_at", ""),
        "lang": tweet.get("lang", ""),
        "like_count": int(metrics.get("like_count", 0)),
        "reply_count": int(metrics.get("reply_count", 0)),
        "retweet_count": int(metrics.get("retweet_count", 0)),
        "quote_count": int(metrics.get("quote_count", 0)),
        "collected_at": collected_at,
        "post_type_llm": "",
        "post_type_manual": "",
        "post_topic_manual": "",
        "post_topic_llm": "",
    }


def fetch_reactions_for_query(
    *,
    parent_post_id: str,
    reaction_type: str,
    query: str,
    limit: int,
) -> list[dict[str, Any]]:
    """Fetch all reactions returned by a paid recent-search request."""
    bearer_token = get_bearer_token()
    requested_limit = clamp_recent_search_limit(limit)
    params = {
        "query": query,
        "max_results": requested_limit,
        "tweet.fields": (
            "author_id,conversation_id,created_at,in_reply_to_user_id,lang,"
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

    collected_at = datetime.now(UTC).isoformat(timespec="seconds")
    return [
        build_reaction_row(tweet, parent_post_id, reaction_type, collected_at)
        for tweet in tweets
        if isinstance(tweet, dict)
    ]


def clean_text(text: str) -> str:
    """Compact whitespace for a first clean_text field."""
    return " ".join(text.replace("\n", " ").split())


def build_reaction_row(
    tweet: dict[str, Any],
    parent_post_id: str,
    reaction_type: str,
    collected_at: str,
) -> dict[str, Any]:
    """Normalize one reaction tweet into the planned post_reactions schema."""
    metrics = tweet.get("public_metrics")
    if not isinstance(metrics, dict):
        metrics = {}

    text = clean_text(str(tweet.get("text", "")))
    return {
        "reaction_id": stable_hash(tweet.get("id", "")),
        "source_reaction_id_hash": stable_hash(tweet.get("id", "")),
        "parent_post_id": parent_post_id,
        "club": "Sao Paulo",
        "reaction_type": reaction_type,
        "author_id_hash": stable_hash(tweet.get("author_id", "")),
        "text": text,
        "created_at": tweet.get("created_at", ""),
        "lang": tweet.get("lang", ""),
        "like_count": int(metrics.get("like_count", 0)),
        "reply_count": int(metrics.get("reply_count", 0)),
        "retweet_count": int(metrics.get("retweet_count", 0)),
        "quote_count": int(metrics.get("quote_count", 0)),
        "collected_at": collected_at,
        "clean_text": text,
    }
