"""Analyze LLM-only labels for the expanded Sao Paulo contextual sample."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLE = (
    PROJECT_ROOT / "data" / "annotated" / "manual_annotation_sample_sao_paulo_expanded.csv"
)
DEFAULT_PREDICTIONS = (
    PROJECT_ROOT / "data" / "llm_outputs" / "reaction_annotation_predictions_expanded.jsonl"
)
DEFAULT_OUTPUT_CSV = (
    PROJECT_ROOT / "data" / "processed" / "expanded_llm_annotations_sao_paulo.csv"
)
DEFAULT_OUTPUT_MD = (
    PROJECT_ROOT / "data" / "processed" / "expanded_llm_analysis_sao_paulo.md"
)
DEFAULT_TABLES_DIR = PROJECT_ROOT / "data" / "processed" / "expanded_llm_analysis_tables"

LABEL_COLUMNS = ["relevancia", "tema", "emocao", "polaridade", "intencao"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analisa rotulos LLM da amostra expandida Sao Paulo."
    )
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--tables-dir", type=Path, default=DEFAULT_TABLES_DIR)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def build_dataset(sample: pd.DataFrame, predictions: list[dict[str, Any]]) -> pd.DataFrame:
    prediction_df = pd.DataFrame(predictions)
    selected_prediction_columns = [
        "reaction_id",
        *LABEL_COLUMNS,
        "confianca_modelo",
        "justificativa_curta",
    ]
    for column in selected_prediction_columns:
        if column not in prediction_df:
            prediction_df[column] = ""

    base_columns = [
        "reaction_id",
        "parent_post_id",
        "club",
        "reaction_type",
        "clean_text",
        "official_text",
        "official_post_type",
        "official_post_topic",
    ]
    merged = sample[base_columns].merge(
        prediction_df[selected_prediction_columns],
        on="reaction_id",
        how="left",
    )
    return merged.fillna("")


def count_lines(counter: Counter[str]) -> list[str]:
    if not counter:
        return ["- nenhum registro"]
    return [f"- `{label}`: {count}" for label, count in counter.most_common()]


def grouped_count(df: pd.DataFrame, group_column: str, value_column: str) -> pd.DataFrame:
    return (
        df.groupby([group_column, value_column])
        .size()
        .reset_index(name="count")
        .sort_values([group_column, "count", value_column], ascending=[True, False, True])
    )


def write_tables(df: pd.DataFrame, tables_dir: Path) -> list[Path]:
    tables_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "llm_polaridade_por_tipo_post.csv": grouped_count(
            df, "official_post_type", "polaridade"
        ),
        "llm_polaridade_por_assunto_post.csv": grouped_count(
            df, "official_post_topic", "polaridade"
        ),
        "llm_tema_por_assunto_post.csv": grouped_count(
            df, "official_post_topic", "tema"
        ),
        "llm_intencao_por_tipo_post.csv": grouped_count(
            df, "official_post_type", "intencao"
        ),
    }
    paths: list[Path] = []
    for filename, table in tables.items():
        path = tables_dir / filename
        table.to_csv(path, index=False, encoding="utf-8-sig")
        paths.append(path)
    return paths


def render_report(df: pd.DataFrame, table_paths: list[Path]) -> str:
    lines = [
        "# Analise LLM Expandida - Sao Paulo",
        "",
        "Relatorio exploratorio com rotulos automaticos da DeepSeek para a amostra expandida.",
        "",
        "## Cobertura",
        "",
        f"- reacoes na amostra expandida: {len(df)}",
        f"- reacoes com predicao LLM: {int((df['polaridade'].astype(str).str.strip() != '').sum())}",
        "",
        "## Tipo de Reacao",
        "",
        *count_lines(Counter(df["reaction_type"])),
        "",
        "## Tipo de Publicacao Oficial",
        "",
        *count_lines(Counter(df["official_post_type"])),
        "",
        "## Assunto da Publicacao Oficial",
        "",
        *count_lines(Counter(df["official_post_topic"])),
        "",
        "## Polaridade LLM",
        "",
        *count_lines(Counter(df["polaridade"])),
        "",
        "## Temas LLM",
        "",
        *count_lines(Counter(df["tema"])),
        "",
        "## Emocoes LLM",
        "",
        *count_lines(Counter(df["emocao"])),
        "",
        "## Intencoes LLM",
        "",
        *count_lines(Counter(df["intencao"])),
        "",
        "## Leitura Inicial",
        "",
        (
            "Esta analise ainda nao substitui validacao manual. Ela serve para "
            "explorar a base 5x maior e identificar padroes gerais antes de "
            "selecionar novos casos para revisao humana."
        ),
        "",
        "## Tabelas Geradas",
        "",
    ]
    for path in table_paths:
        relative_path = path.relative_to(PROJECT_ROOT)
        lines.append(f"- `{relative_path.as_posix()}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    sample = pd.read_csv(args.sample, encoding="utf-8-sig").fillna("")
    predictions = read_jsonl(args.predictions)
    dataset = build_dataset(sample, predictions)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(args.output_csv, index=False, encoding="utf-8-sig")

    table_paths = write_tables(dataset, args.tables_dir)
    args.output_md.write_text(render_report(dataset, table_paths), encoding="utf-8")

    print(f"Registros analisados: {len(dataset)}")
    print(f"CSV salvo em: {args.output_csv}")
    print(f"Relatorio salvo em: {args.output_md}")
    print(f"Tabelas salvas em: {args.tables_dir}")


if __name__ == "__main__":
    main()
