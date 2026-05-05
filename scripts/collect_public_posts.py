"""Collect anonymized public posts through an authorized third-party API."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from queridometro.collectors.twitter_public_collector import collect_from_third_party_api
from queridometro.config import (
    MAX_POSTS,
    RAW_DATA_DIR,
    SEARCH_TERMS,
    TWITTER_API_AUTH_HEADER,
    TWITTER_API_AUTH_PREFIX,
    TWITTER_API_BASE_URL,
    TWITTER_API_ITEMS_PATH,
    TWITTER_API_KEY,
    TWITTER_API_QUERY_PARAM,
    TWITTER_API_TEXT_FIELD,
    TWITTER_PROVIDER_NAME,
)
from queridometro.utils.io import write_csv


def main() -> None:
    df = collect_from_third_party_api(
        search_terms=SEARCH_TERMS,
        base_url=TWITTER_API_BASE_URL,
        api_key=TWITTER_API_KEY,
        provider_name=TWITTER_PROVIDER_NAME,
        query_param=TWITTER_API_QUERY_PARAM,
        items_path=TWITTER_API_ITEMS_PATH,
        text_field=TWITTER_API_TEXT_FIELD,
        auth_header=TWITTER_API_AUTH_HEADER,
        auth_prefix=TWITTER_API_AUTH_PREFIX,
        max_posts=MAX_POSTS,
    )

    if df.empty:
        print("No posts collected. Check the third-party API configuration and terms.")
        return

    output_path = write_csv(df, RAW_DATA_DIR / "twitter_public_comments.csv")
    print(f"Anonymized public comments saved to {output_path}")


if __name__ == "__main__":
    main()
