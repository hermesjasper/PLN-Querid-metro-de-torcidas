"""Project configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROJECT_NAME = os.getenv("PROJECT_NAME", "PLN Queridometro de Torcidas")
MAX_POSTS = int(os.getenv("MAX_POSTS", "100"))
SEARCH_TERMS = [
    term.strip()
    for term in os.getenv(
        "SEARCH_TERMS",
        "Flamengo,Corinthians,Palmeiras,Sao Paulo,Vasco,Fluminense,Botafogo,Santos,Gremio,Internacional",
    ).split(",")
    if term.strip()
]

DATA_DIR = PROJECT_ROOT / os.getenv("DATA_DIR", "data")
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

TWITTER_PROVIDER_NAME = os.getenv("TWITTER_PROVIDER_NAME", "third_party_twitter_api")
TWITTER_API_BASE_URL = os.getenv("TWITTER_API_BASE_URL", "")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_QUERY_PARAM = os.getenv("TWITTER_API_QUERY_PARAM", "query")
TWITTER_API_ITEMS_PATH = os.getenv("TWITTER_API_ITEMS_PATH", "data")
TWITTER_API_TEXT_FIELD = os.getenv("TWITTER_API_TEXT_FIELD", "text")
TWITTER_API_AUTH_HEADER = os.getenv("TWITTER_API_AUTH_HEADER", "Authorization")
TWITTER_API_AUTH_PREFIX = os.getenv("TWITTER_API_AUTH_PREFIX", "Bearer")
