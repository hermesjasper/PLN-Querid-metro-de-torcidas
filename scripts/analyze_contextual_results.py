"""Generate contextual analysis reports for the Sao Paulo pilot sample."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OFFICIAL_POSTS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "official_posts_test_sao_paulo.csv"
)
DEFAULT_REACTIONS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "post_reactions_test_sao_paulo.csv"
)
DEFAULT_ANNOTATED = PROJECT_ROOT / "data" / "annotated" / "annotated_reactions_sao_paulo.csv"
DEFAULT_PREDICTIONS = (
    PROJECT_ROOT / "data" / "llm_outputs" / "reaction_annotation_predictions_taxonomy_v2.jsonl"
)
DEFAULT_COMPARISON = (
    PROJECT_ROOT / "data" / "llm_outputs" / "llm_annotation_comparison_taxonomy_v2.csv"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "contextual_analysis_sao_paulo.md"
DEFAULT_TABLES_DIR = PROJECT_ROOT / "data" / "processed" / "contextual_analysis_tables"

LABEL_COLUMNS = ["relevancia", "tema", "emocao", "polaridade", "intencao"]
ALLOWED_VALUES = {
    "relevancia": {"RELEVANTE", "POUCO_INFORMATIVO", "NAO_RELEVANTE"},
    "tema": {
        "ELENCO",
        "TECNICO",
        "DIRETORIA",
        "ARBITRAGEM",
        "CONTRATACAO",
        "DESEMPENHO_EM_CAMPO",
        "TORCIDA",
        "RIVALIDADE",
        "PATROCINIO",
        "PARCERIA_COMERCIAL",
        "MARKETING",
        "PRODUTO_OFICIAL",
        "CATEGORIA_BASE",
        "FUTEBOL_FEMININO",
        "INGRESSOS",
        "SOCIO_TORCEDOR",
        "COMUNICACAO_DO_CLUBE",
        "OUTRO",
    },
    "emocao": {
        "ALEGRIA",
        "ORGULHO",
        "RAIVA",
        "FRUSTRACAO",
        "IRONIA",
        "ESPERANCA",
        "ANSIEDADE",
        "DESCONFIANCA",
        "APOIO",
        "NEUTRO",
    },
    "polaridade": {"POSITIVO", "NEGATIVO", "NEUTRO", "MISTO"},
    "intencao": {
        "ELOGIO",
        "CRITICA",
        "COBRANCA",
        "PROVOCACAO",
        "MEME_PIADA",
        "PERGUNTA",
        "PEDIDO",
        "APOIO",
        "INFORMACAO",
        "OUTRO",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera analise contextual da amostra Sao Paulo."
    )
    parser.add_argument("--official-posts", type=Path, default=DEFAULT_OFFICIAL_POSTS)
    parser.add_argument("--reactions", type=Path, default=DEFAULT_REACTIONS)
    parser.add_argument("--annotated", type=Path, default=DEFAULT_ANNOTATED)
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--comparison", type=Path, default=DEFAULT_COMPARISON)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--tables-dir", type=Path, default=DEFAULT_TABLES_DIR)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def value_counts_table(df: pd.DataFrame, group_column: str, value_column: str) -> pd.DataFrame:
    table = (
        df.groupby([group_column, value_column])
        .size()
        .reset_index(name="count")
        .sort_values([group_column, "count", value_column], ascending=[True, False, True])
    )
    return table


def write_table(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def markdown_count_lines(counter: Counter[str]) -> list[str]:
    if not counter:
        return ["- nenhum registro"]
    return [f"- `{label}`: {count}" for label, count in counter.most_common()]


def comparison_accuracy(comparison: pd.DataFrame) -> dict[str, tuple[int, int, float]]:
    metrics: dict[str, tuple[int, int, float]] = {}
    for column in LABEL_COLUMNS:
        llm_column = f"llm_{column}"
        match_column = f"match_{column}"
        evaluated = comparison[comparison[llm_column].astype(str).str.strip() != ""]
        matches = evaluated[evaluated[match_column].astype(str).str.upper() == "TRUE"]
        total = len(evaluated)
        accuracy = len(matches) / total if total else 0.0
        metrics[column] = (len(matches), total, accuracy)
    return metrics


def invalid_prediction_labels(predictions: list[dict[str, Any]]) -> list[dict[str, str]]:
    invalid: list[dict[str, str]] = []
    for record in predictions:
        reaction_id = str(record.get("reaction_id", ""))
        for column, allowed in ALLOWED_VALUES.items():
            value = str(record.get(column, "")).strip()
            if value and value not in allowed:
                invalid.append(
                    {
                        "reaction_id": reaction_id,
                        "field": column,
                        "value": value,
                    }
                )
    return invalid


def render_report(
    *,
    posts: pd.DataFrame,
    reactions: pd.DataFrame,
    annotated: pd.DataFrame,
    predictions: list[dict[str, Any]],
    comparison: pd.DataFrame,
    tables_dir: Path,
) -> str:
    post_type = posts["post_type_manual"].where(
        posts["post_type_manual"].astype(str).str.strip() != "",
        posts["post_type_llm"],
    )
    post_topic = posts["post_topic_manual"].where(
        posts["post_topic_manual"].astype(str).str.strip() != "",
        posts["post_topic_llm"],
    )

    invalid_labels = invalid_prediction_labels(predictions)
    invalid_by_field = Counter(item["field"] for item in invalid_labels)
    accuracy = comparison_accuracy(comparison)

    tables = {
        "manual_polaridade_por_tipo_post.csv": value_counts_table(
            annotated, "official_post_type", "polaridade"
        ),
        "manual_polaridade_por_assunto_post.csv": value_counts_table(
            annotated, "official_post_topic", "polaridade"
        ),
        "manual_tema_por_assunto_post.csv": value_counts_table(
            annotated, "official_post_topic", "tema"
        ),
        "manual_intencao_por_tipo_post.csv": value_counts_table(
            annotated, "official_post_type", "intencao"
        ),
    }
    for filename, table in tables.items():
        write_table(table, tables_dir / filename)

    lines = [
        "# Analise Contextual - Sao Paulo",
        "",
        "Relatorio gerado a partir da amostra piloto contextual.",
        "",
        "## Cobertura da Base",
        "",
        f"- posts oficiais coletados: {len(posts)}",
        f"- reacoes brutas coletadas: {len(reactions)}",
        f"- reacoes anotadas manualmente: {len(annotated)}",
        f"- predicoes LLM analisadas: {len(predictions)}",
        "",
        "## Tipos de Publicacao Oficial",
        "",
        *markdown_count_lines(Counter(post_type)),
        "",
        "## Assuntos da Publicacao Oficial",
        "",
        *markdown_count_lines(Counter(post_topic)),
        "",
        "## Polaridade Manual",
        "",
        *markdown_count_lines(Counter(annotated["polaridade"])),
        "",
        "## Temas Manuais das Reacoes",
        "",
        *markdown_count_lines(Counter(annotated["tema"])),
        "",
        "## Intencoes Manuais das Reacoes",
        "",
        *markdown_count_lines(Counter(annotated["intencao"])),
        "",
        "## Acuracia DeepSeek vs Manual",
        "",
    ]
    for column, (matches, total, acc) in accuracy.items():
        lines.append(f"- `{column}`: {matches}/{total} ({acc:.1%})")

    lines.extend(
        [
            "",
            "## Rotulos Invalidos do LLM",
            "",
            f"Total de rotulos fora da taxonomia: {len(invalid_labels)}",
            "",
            *markdown_count_lines(invalid_by_field),
            "",
        ]
    )
    if invalid_labels:
        lines.extend(["### Casos", ""])
        for item in invalid_labels:
            lines.append(
                f"- `{item['reaction_id']}`: campo `{item['field']}` recebeu `{item['value']}`"
            )
        lines.append("")

    lines.extend(
        [
            "## Tabelas Geradas",
            "",
        ]
    )
    display_tables_dir = tables_dir.as_posix()
    for filename in tables:
        lines.append(f"- `{display_tables_dir}/{filename}`")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    posts = pd.read_csv(args.official_posts, encoding="utf-8-sig").fillna("")
    reactions = pd.read_csv(args.reactions, encoding="utf-8-sig").fillna("")
    annotated = pd.read_csv(args.annotated, encoding="utf-8-sig").fillna("")
    comparison = pd.read_csv(args.comparison, encoding="utf-8-sig").fillna("")
    predictions = read_jsonl(args.predictions)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        render_report(
            posts=posts,
            reactions=reactions,
            annotated=annotated,
            predictions=predictions,
            comparison=comparison,
            tables_dir=args.tables_dir,
        ),
        encoding="utf-8",
    )

    print(f"Relatorio salvo em: {args.output}")
    print(f"Tabelas salvas em: {args.tables_dir}")


if __name__ == "__main__":
    main()
