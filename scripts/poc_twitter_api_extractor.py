"""POC de extracao do Twitter/X via biblioteca de scraping.

Esta POC usa `ntscraper`, uma biblioteca nao oficial baseada em instancias do
Nitter. Ela nao usa API terceira, nao faz login, nao tenta burlar captcha,
paywall, bloqueios ou limites da plataforma.

O objetivo e entender a viabilidade tecnica para um trabalho academico. O CSV
gerado salva somente texto anonimizado e metadados do projeto:
text, search_term, source, collected_at.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def anonymize_post_text(text: str) -> str:
    """Keep textual content compact without storing extra profile metadata."""
    return " ".join(text.replace("\n", " ").split())


def parse_args() -> argparse.Namespace:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="POC para coletar textos publicos via ntscraper/Nitter."
    )
    parser.add_argument("--term", default="Flamengo", help="Termo de busca.")
    parser.add_argument(
        "--mode",
        choices=["term", "hashtag"],
        default="term",
        help="Modo de busca do ntscraper. Evite modo user para nao focar perfis.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Quantidade maxima de posts. Mantenha baixo em POC.",
    )
    parser.add_argument(
        "--language",
        default="pt",
        help="Idioma ISO 639-1 usado na busca, quando suportado pela instancia.",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="Data inicial no formato YYYY-MM-DD.",
    )
    parser.add_argument(
        "--until",
        default=None,
        help="Data final no formato YYYY-MM-DD.",
    )
    parser.add_argument(
        "--instance",
        default=None,
        help="Instancia Nitter especifica. Prefira uma instancia propria/autorizada.",
    )
    parser.add_argument(
        "--skip-instance-check",
        action="store_true",
        help="Pula a checagem inicial da instancia do Nitter.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "raw" / "poc_ntscraper_comments.csv",
    )
    parser.add_argument(
        "--show-sample",
        action="store_true",
        help="Mostra uma pequena amostra dos textos anonimizados extraidos.",
    )
    return parser.parse_args()


def import_ntscraper() -> Any:
    """Import ntscraper lazily to keep the error message helpful."""
    try:
        from ntscraper import Nitter
    except ImportError as exc:
        raise SystemExit(
            "A biblioteca ntscraper nao esta instalada. Rode:\n"
            "  .\\.venv\\Scripts\\python.exe -m pip install ntscraper\n"
            "ou adicione `ntscraper` ao requirements.txt e reinstale."
        ) from exc
    return Nitter


def extract_text_from_tweet(tweet: dict[str, Any]) -> str:
    """Extract only textual content from a tweet-like object."""
    for field in ("text", "content", "tweetText"):
        value = tweet.get(field)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def build_rows(
    tweets_payload: dict[str, Any],
    search_term: str,
    source: str,
    limit: int,
) -> list[dict[str, str]]:
    """Build anonymized rows from ntscraper output."""
    tweets = tweets_payload.get("tweets", [])
    if not isinstance(tweets, list):
        return []

    collected_at = datetime.now(UTC).isoformat(timespec="seconds")
    rows: list[dict[str, str]] = []

    for tweet in tweets:
        if len(rows) >= limit:
            break
        if not isinstance(tweet, dict):
            continue

        text = extract_text_from_tweet(tweet)
        if not text:
            continue

        rows.append(
            {
                "text": anonymize_post_text(text),
                "search_term": search_term,
                "source": source,
                "collected_at": collected_at,
            }
        )

    return rows


def main() -> None:
    args = parse_args()
    if args.limit > 50:
        raise SystemExit("Para POC, use --limit ate 50 para evitar coleta excessiva.")

    Nitter = import_ntscraper()
    scraper = Nitter(log_level=1, skip_instance_check=args.skip_instance_check)

    print("POC ntscraper/Nitter")
    print("Uso academico experimental, sem login, sem bypass e sem dados pessoais no CSV.")
    print(f"Termo: {args.term}")
    print(f"Modo: {args.mode}")
    print(f"Limite: {args.limit}")
    print(f"Instancia: {args.instance or 'auto'}")

    payload = scraper.get_tweets(
        args.term,
        mode=args.mode,
        number=args.limit,
        since=args.since,
        until=args.until,
        language=args.language,
        replies=False,
        instance=args.instance,
        max_retries=2,
    )

    rows = build_rows(
        tweets_payload=payload,
        search_term=args.term,
        source="ntscraper_nitter",
        limit=args.limit,
    )

    if not rows:
        raise SystemExit(
            "Nenhum texto extraido. A instancia Nitter pode estar indisponivel, "
            "bloqueada ou sem resultados para o termo."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows, columns=["text", "search_term", "source", "collected_at"])
    df.to_csv(args.output, index=False, encoding="utf-8")

    print(f"Textos anonimizados extraidos: {len(df)}")
    print(f"CSV salvo em: {args.output}")
    print("Colunas salvas: text, search_term, source, collected_at")

    if args.show_sample:
        print("\nAmostra:")
        for text in df["text"].head(3):
            print(f"- {text[:240]}")


if __name__ == "__main__":
    main()
