"""Generate a focused report of LLM/manual annotation disagreements."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMPARISON = (
    PROJECT_ROOT / "data" / "llm_outputs" / "llm_annotation_comparison_taxonomy_v3.csv"
)
DEFAULT_ANNOTATED = PROJECT_ROOT / "data" / "annotated" / "annotated_reactions_sao_paulo.csv"
DEFAULT_OUTPUT_CSV = (
    PROJECT_ROOT / "data" / "processed" / "llm_disagreements_taxonomy_v3.csv"
)
DEFAULT_OUTPUT_MD = (
    PROJECT_ROOT / "data" / "processed" / "llm_disagreement_analysis_taxonomy_v3.md"
)

LABEL_COLUMNS = ["relevancia", "tema", "emocao", "polaridade", "intencao"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analisa divergencias entre LLM e referencia manual."
    )
    parser.add_argument("--comparison", type=Path, default=DEFAULT_COMPARISON)
    parser.add_argument("--annotated", type=Path, default=DEFAULT_ANNOTATED)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser.parse_args()


def normalize_bool(value: object) -> bool:
    return str(value).strip().upper() == "TRUE"


def build_disagreement_rows(
    comparison: pd.DataFrame,
    annotated: pd.DataFrame,
) -> list[dict[str, str]]:
    context = annotated[
        [
            "reaction_id",
            "parent_post_id",
            "club",
            "official_post_type",
            "official_post_topic",
            "reaction_type",
            "clean_text",
        ]
    ]
    merged = comparison.merge(context, on="reaction_id", how="left").fillna("")

    rows: list[dict[str, str]] = []
    for _, row in merged.iterrows():
        for column in LABEL_COLUMNS:
            if normalize_bool(row.get(f"match_{column}", "")):
                continue
            rows.append(
                {
                    "reaction_id": str(row["reaction_id"]),
                    "field": column,
                    "manual_value": str(row.get(f"manual_{column}", "")),
                    "llm_value": str(row.get(f"llm_{column}", "")),
                    "official_post_type": str(row.get("official_post_type", "")),
                    "official_post_topic": str(row.get("official_post_topic", "")),
                    "reaction_type": str(row.get("reaction_type", "")),
                    "clean_text": str(row.get("clean_text", "")),
                }
            )
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    fieldnames = [
        "reaction_id",
        "field",
        "manual_value",
        "llm_value",
        "official_post_type",
        "official_post_topic",
        "reaction_type",
        "clean_text",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_counter(counter: Counter[str]) -> list[str]:
    if not counter:
        return ["- nenhum registro"]
    return [f"- `{label}`: {count}" for label, count in counter.most_common()]


def render_markdown(rows: list[dict[str, str]]) -> str:
    by_field = Counter(row["field"] for row in rows)
    by_topic = Counter(row["official_post_topic"] for row in rows)
    by_type = Counter(row["official_post_type"] for row in rows)

    tema_rows = [row for row in rows if row["field"] == "tema"]
    tema_pairs = Counter(
        f"{row['manual_value']} -> {row['llm_value']}" for row in tema_rows
    )

    lines = [
        "# Analise de Divergencias LLM vs Manual",
        "",
        "Relatorio focado nos casos em que a DeepSeek `taxonomy_v3` discordou da referencia manual.",
        "",
        f"Total de divergencias por campo: {len(rows)}",
        "",
        "## Divergencias por Campo",
        "",
        *render_counter(by_field),
        "",
        "## Divergencias por Assunto do Post",
        "",
        *render_counter(by_topic),
        "",
        "## Divergencias por Tipo de Post",
        "",
        *render_counter(by_type),
        "",
        "## Pares de Divergencia em Tema",
        "",
        *render_counter(tema_pairs),
        "",
        "## Casos de Tema para Revisao",
        "",
    ]

    if not tema_rows:
        lines.append("- nenhum registro")
    else:
        for row in tema_rows:
            text = row["clean_text"].replace("\n", " ").strip()
            if len(text) > 180:
                text = text[:177].rstrip() + "..."
            lines.extend(
                [
                    f"### `{row['reaction_id']}`",
                    "",
                    f"- assunto do post: `{row['official_post_topic']}`",
                    f"- tipo do post: `{row['official_post_type']}`",
                    f"- manual: `{row['manual_value']}`",
                    f"- llm: `{row['llm_value']}`",
                    f"- texto: {text}",
                    "",
                ]
            )

    lines.extend(
        [
            "## Leitura Inicial",
            "",
            "As divergencias em `tema` se concentram em casos em que a reacao mistura alvo esportivo, contexto da base e critica institucional. Isso sugere que a taxonomia precisa de criterios de desempate mais explicitos para decidir entre `CATEGORIA_BASE`, `DESEMPENHO_EM_CAMPO`, `ELENCO`, `DIRETORIA` e `COMUNICACAO_DO_CLUBE`.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    comparison = pd.read_csv(args.comparison, encoding="utf-8-sig").fillna("")
    annotated = pd.read_csv(args.annotated, encoding="utf-8-sig").fillna("")
    rows = build_disagreement_rows(comparison, annotated)

    write_csv(rows, args.output_csv)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(rows), encoding="utf-8")

    print(f"Divergencias: {len(rows)}")
    print(f"CSV salvo em: {args.output_csv}")
    print(f"Relatorio salvo em: {args.output_md}")


if __name__ == "__main__":
    main()
