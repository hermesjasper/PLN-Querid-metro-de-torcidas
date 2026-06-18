"""Prepare a manual annotation sample from contextual reaction data."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OFFICIAL_POSTS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "official_posts_test_sao_paulo.csv"
)
DEFAULT_REACTIONS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "post_reactions_test_sao_paulo.csv"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "annotated" / "manual_annotation_sample_sao_paulo.csv"
)


ANNOTATION_COLUMNS = [
    "relevancia",
    "tema",
    "emocao",
    "polaridade",
    "intencao",
    "confianca_modelo",
    "justificativa_curta",
    "validado_manual",
    "rotulo_corrigido",
    "observacoes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera uma amostra de reacoes para anotacao manual."
    )
    parser.add_argument("--official-posts", type=Path, default=DEFAULT_OFFICIAL_POSTS)
    parser.add_argument("--reactions", type=Path, default=DEFAULT_REACTIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sample-size", type=int, default=30)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def build_sample(
    official_posts: pd.DataFrame,
    reactions: pd.DataFrame,
    sample_size: int,
    random_state: int,
) -> pd.DataFrame:
    official_context = official_posts[
        [
            "post_id",
            "official_text",
            "created_at",
            "like_count",
            "reply_count",
            "quote_count",
        ]
    ].rename(
        columns={
            "post_id": "parent_post_id",
            "official_text": "official_text",
            "created_at": "official_created_at",
            "like_count": "official_like_count",
            "reply_count": "official_reply_count",
            "quote_count": "official_quote_count",
        }
    )
    merged = reactions.merge(official_context, on="parent_post_id", how="left")
    if len(merged) <= sample_size:
        sample = merged.copy()
    else:
        grouped = merged.groupby("reaction_type", group_keys=False)
        base_per_group = max(1, sample_size // max(1, merged["reaction_type"].nunique()))
        sampled_parts = [
            group.sample(
                n=min(len(group), base_per_group),
                random_state=random_state,
            )
            for _, group in grouped
        ]
        sample = pd.concat(sampled_parts, ignore_index=True)
        remaining = sample_size - len(sample)
        if remaining > 0:
            remaining_pool = merged.drop(sample.index, errors="ignore")
            extra = remaining_pool.sample(
                n=min(remaining, len(remaining_pool)),
                random_state=random_state,
            )
            sample = pd.concat([sample, extra], ignore_index=True)

    for column in ANNOTATION_COLUMNS:
        sample[column] = ""

    sample["validado_manual"] = "NAO"
    sample["confianca_modelo"] = ""

    ordered_columns = [
        "reaction_id",
        "parent_post_id",
        "club",
        "reaction_type",
        "clean_text",
        "official_text",
        "official_created_at",
        "official_like_count",
        "official_reply_count",
        "official_quote_count",
        "like_count",
        "reply_count",
        "retweet_count",
        "quote_count",
        *ANNOTATION_COLUMNS,
    ]
    return sample[ordered_columns].sort_values(
        by=["parent_post_id", "reaction_type", "reaction_id"]
    )


def main() -> None:
    args = parse_args()
    official_posts = pd.read_csv(args.official_posts, encoding="utf-8-sig")
    reactions = pd.read_csv(args.reactions, encoding="utf-8-sig")
    sample = build_sample(
        official_posts=official_posts,
        reactions=reactions,
        sample_size=args.sample_size,
        random_state=args.random_state,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"Amostra gerada: {len(sample)} reacoes")
    print(f"CSV salvo em: {args.output}")


if __name__ == "__main__":
    main()
