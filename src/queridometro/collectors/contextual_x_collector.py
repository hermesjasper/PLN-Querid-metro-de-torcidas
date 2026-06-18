"""Planned contextual collector for official club posts and reactions.

This module is intentionally a placeholder. It documents the planned collection
surface for the next stage of the PoC, but it does not call the X/Twitter API,
does not require tokens and does not spend API budget.

Future collection must respect the cost ceiling described in
`docs/plano_coleta.md` and log every run in `data/metadata/collection_log.csv`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_COLLECTION_LOG = Path("data/metadata/collection_log.csv")


@dataclass(frozen=True)
class CollectionPlan:
    """Small plan object for a future contextual collection run."""

    club: str = "A DEFINIR"
    club_username: str = "A DEFINIR"
    official_posts_limit: int = 15
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
    """Placeholder for collecting official posts from the club profile."""
    raise NotImplementedError(
        "Future step: fetch official club posts after cost and endpoint checks."
    )


def fetch_replies(parent_post_id: str, limit: int) -> list[dict[str, Any]]:
    """Placeholder for collecting replies associated with one official post."""
    raise NotImplementedError(
        "Future step: fetch replies for a selected official post."
    )


def fetch_quote_tweets(parent_post_id: str, limit: int) -> list[dict[str, Any]]:
    """Placeholder for collecting quote tweets associated with one official post."""
    raise NotImplementedError(
        "Future step: fetch quote tweets for a selected official post."
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
    estimated_cost: float,
    status: str,
    notes: str,
    log_path: Path = DEFAULT_COLLECTION_LOG,
) -> None:
    """Placeholder for appending future collection metadata to the log CSV."""
    raise NotImplementedError(
        "Future step: append collection metadata after a real collection run."
    )


def build_collection_plan(
    club: str = "A DEFINIR",
    club_username: str = "A DEFINIR",
) -> CollectionPlan:
    """Return the default low-cost plan for the next collection stage."""
    return CollectionPlan(club=club, club_username=club_username)
