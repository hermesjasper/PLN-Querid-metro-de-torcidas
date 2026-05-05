"""Third-party Twitter/X API collector.

This collector is designed for academic use with authorized third-party APIs.
It does not scrape protected pages and does not implement login automation,
captcha bypass, paywall bypass, rate-limit evasion or any mechanism that could
violate platform protections.

Only anonymized text rows are persisted by the public functions in this module.
Usernames, profile URLs, user IDs, tweet IDs, avatars, locations and similar
identifiers are intentionally ignored even when the provider response includes
them.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pandas as pd
import requests


class ThirdPartyCollectionUnavailable(RuntimeError):
    """Raised when an authorized third-party collection cannot be completed."""


def anonymize_post_text(text: str) -> str:
    """Keep only textual content and remove obvious line noise."""
    return " ".join(text.replace("\n", " ").split())


def _get_nested_value(payload: dict[str, Any], path: str) -> Any:
    """Read a dotted path from a JSON object."""
    value: Any = payload
    for part in path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def _build_auth_headers(
    api_key: str,
    auth_header: str,
    auth_prefix: str,
) -> dict[str, str]:
    """Build minimal auth headers without logging or persisting the key."""
    if not api_key:
        return {}

    token = f"{auth_prefix} {api_key}".strip() if auth_prefix else api_key
    return {auth_header: token}


def collect_from_third_party_api(
    search_terms: list[str],
    *,
    base_url: str,
    api_key: str,
    provider_name: str,
    query_param: str = "query",
    items_path: str = "data",
    text_field: str = "text",
    auth_header: str = "Authorization",
    auth_prefix: str = "Bearer",
    max_posts: int = 100,
) -> pd.DataFrame:
    """Collect public football comments through an authorized third-party API.

    The provider must be configured to return public posts that the researcher
    is allowed to access. This function stores only anonymized text plus project
    metadata needed for NLP experiments.
    """
    columns = ["text", "search_term", "source", "collected_at"]

    if not base_url or not api_key:
        print(
            "API terceirizada nao configurada. Defina TWITTER_API_BASE_URL e "
            "TWITTER_API_KEY no arquivo .env."
        )
        return pd.DataFrame(columns=columns)

    collected_at = datetime.now(UTC).isoformat(timespec="seconds")
    rows: list[dict[str, str]] = []

    headers = {
        "Accept": "application/json",
        "User-Agent": "pln-queridometro-academic/0.1",
        **_build_auth_headers(api_key, auth_header, auth_prefix),
    }

    for term in search_terms:
        if len(rows) >= max_posts:
            break

        try:
            response = requests.get(
                base_url,
                params={query_param: term, "limit": max_posts},
                headers=headers,
                timeout=20,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ThirdPartyCollectionUnavailable(
                "Nao foi possivel coletar via API terceirizada configurada."
            ) from exc

        payload = response.json()
        items = _get_nested_value(payload, items_path)
        if not isinstance(items, list):
            print(f"Nenhuma lista encontrada em items_path='{items_path}' para {term}.")
            continue

        for item in items:
            if len(rows) >= max_posts:
                break
            if not isinstance(item, dict):
                continue

            raw_text = item.get(text_field)
            if not isinstance(raw_text, str) or not raw_text.strip():
                continue

            rows.append(
                {
                    "text": anonymize_post_text(raw_text),
                    "search_term": term,
                    "source": provider_name,
                    "collected_at": collected_at,
                }
            )

    return pd.DataFrame(rows[:max_posts], columns=columns)


# Backward-compatible alias for the original project structure.
collect_public_posts = collect_from_third_party_api
