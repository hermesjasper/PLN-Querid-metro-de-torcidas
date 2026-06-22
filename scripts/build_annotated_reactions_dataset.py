"""Build the first annotated reactions dataset from manual validation."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    PROJECT_ROOT / "data" / "annotated" / "manual_annotation_sample_sao_paulo.csv"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "annotated" / "annotated_reactions_sao_paulo.csv"
)
DEFAULT_OFFICIAL_POSTS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "official_posts_test_sao_paulo.csv"
)
DEFAULT_SUMMARY = (
    PROJECT_ROOT / "data" / "annotated" / "annotation_summary_sao_paulo.md"
)

ANNOTATED_COLUMNS = [
    "reaction_id",
    "parent_post_id",
    "club",
    "official_post_type",
    "official_post_topic",
    "reaction_type",
    "clean_text",
    "relevancia",
    "tema",
    "emocao",
    "polaridade",
    "intencao",
    "confianca_modelo",
    "justificativa_curta",
    "validado_manual",
    "rotulo_corrigido",
]

SUMMARY_COLUMNS = [
    "official_post_type",
    "official_post_topic",
    "reaction_type",
    "relevancia",
    "tema",
    "emocao",
    "polaridade",
    "intencao",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Consolida a amostra manual validada em base anotada."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--official-posts", type=Path, default=DEFAULT_OFFICIAL_POSTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def add_official_post_type(
    df: pd.DataFrame,
    official_posts: pd.DataFrame,
) -> pd.DataFrame:
    required_columns = [
        "post_id",
        "post_type_manual",
        "post_type_llm",
        "post_topic_manual",
        "post_topic_llm",
    ]
    for column in required_columns:
        if column not in official_posts:
            official_posts[column] = ""

    post_context = official_posts[required_columns].rename(
        columns={
            "post_id": "parent_post_id",
            "post_type_manual": "official_post_type_manual",
            "post_type_llm": "official_post_type_llm",
            "post_topic_manual": "official_post_topic_manual",
            "post_topic_llm": "official_post_topic_llm",
        }
    )
    merged = df.copy()
    merged["parent_post_id"] = merged["parent_post_id"].astype(str)
    post_context["parent_post_id"] = post_context["parent_post_id"].astype(str)
    merged = merged.merge(post_context, on="parent_post_id", how="left")
    merged["official_post_type"] = merged["official_post_type_manual"].where(
        merged["official_post_type_manual"].astype(str).str.strip() != "",
        merged["official_post_type_llm"],
    )
    merged["official_post_topic"] = merged["official_post_topic_manual"].where(
        merged["official_post_topic_manual"].astype(str).str.strip() != "",
        merged["official_post_topic_llm"],
    )
    return merged.drop(
        columns=[
            "official_post_type_manual",
            "official_post_type_llm",
            "official_post_topic_manual",
            "official_post_topic_llm",
        ]
    )


def build_annotated_dataset(
    df: pd.DataFrame,
    official_posts: pd.DataFrame,
) -> pd.DataFrame:
    validated = df[df["validado_manual"].astype(str).str.upper() == "SIM"].copy()
    validated = add_official_post_type(validated, official_posts)
    missing_columns = [column for column in ANNOTATED_COLUMNS if column not in validated]
    if missing_columns:
        raise ValueError(f"Colunas ausentes: {missing_columns}")
    return validated[ANNOTATED_COLUMNS].sort_values(
        by=["parent_post_id", "reaction_type", "reaction_id"]
    )


def render_value_counts(df: pd.DataFrame, column: str) -> list[str]:
    counts = df[column].fillna("").replace("", "NAO_PREENCHIDO").value_counts()
    lines = [f"## {column}", ""]
    for label, count in counts.items():
        lines.append(f"- `{label}`: {count}")
    lines.append("")
    return lines


def write_summary(df: pd.DataFrame, path: Path) -> None:
    lines = [
        "# Resumo da Base Anotada",
        "",
        f"Total de reacoes anotadas: {len(df)}",
        "",
    ]
    for column in SUMMARY_COLUMNS:
        lines.extend(render_value_counts(df, column))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input, encoding="utf-8-sig").fillna("")
    official_posts = pd.read_csv(args.official_posts, encoding="utf-8-sig").fillna("")
    annotated = build_annotated_dataset(df, official_posts)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    annotated.to_csv(args.output, index=False, encoding="utf-8-sig")
    write_summary(annotated, args.summary)

    print(f"Reacoes anotadas: {len(annotated)}")
    print(f"CSV salvo em: {args.output}")
    print(f"Resumo salvo em: {args.summary}")


if __name__ == "__main__":
    main()
