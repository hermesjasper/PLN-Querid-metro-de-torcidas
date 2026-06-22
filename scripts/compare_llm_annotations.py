"""Compare future LLM annotation outputs against manual reference labels."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE = PROJECT_ROOT / "data" / "llm_inputs" / "manual_reference_labels.jsonl"
DEFAULT_PREDICTIONS = PROJECT_ROOT / "data" / "llm_outputs" / "reaction_annotation_predictions.jsonl"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "llm_outputs" / "llm_annotation_comparison.csv"
DEFAULT_SUMMARY = PROJECT_ROOT / "data" / "llm_outputs" / "llm_annotation_comparison_summary.md"

LABEL_COLUMNS = ["relevancia", "tema", "emocao", "polaridade", "intencao"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compara rotulos de LLM com a referencia manual."
    )
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"JSON invalido em {path}:{line_number}") from exc
    return records


def normalize_reaction_id(record: dict[str, Any]) -> str:
    reaction_id = record.get("reaction_id")
    if isinstance(reaction_id, str) and reaction_id:
        return reaction_id

    custom_id = record.get("custom_id")
    if isinstance(custom_id, str) and custom_id.startswith("reaction-"):
        return custom_id.removeprefix("reaction-")

    return ""


def extract_response_content(record: dict[str, Any]) -> Any:
    """Accept direct JSON labels or common API/batch response wrappers."""
    if any(column in record for column in LABEL_COLUMNS):
        return record

    response = record.get("response")
    if isinstance(response, dict):
        body = response.get("body")
        if isinstance(body, dict):
            choices = body.get("choices")
            if isinstance(choices, list) and choices:
                message = choices[0].get("message")
                if isinstance(message, dict):
                    return message.get("content", "")
        if "content" in response:
            return response["content"]

    if "content" in record:
        return record["content"]

    if "labels" in record:
        return record["labels"]

    return record


def parse_prediction_labels(record: dict[str, Any]) -> dict[str, str]:
    content = extract_response_content(record)
    if isinstance(content, dict):
        parsed = content
    elif isinstance(content, str):
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.removeprefix("json").strip()
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            reaction_id = normalize_reaction_id(record) or "desconhecido"
            raise ValueError(f"Resposta LLM invalida para {reaction_id}") from exc
    else:
        parsed = {}

    return {column: str(parsed.get(column, "")).strip() for column in LABEL_COLUMNS}


def load_manual_reference(path: Path) -> dict[str, dict[str, str]]:
    references: dict[str, dict[str, str]] = {}
    for record in read_jsonl(path):
        reaction_id = normalize_reaction_id(record)
        labels = record.get("manual_labels", {})
        if not reaction_id or not isinstance(labels, dict):
            continue
        references[reaction_id] = {
            column: str(labels.get(column, "")).strip() for column in LABEL_COLUMNS
        }
    return references


def load_predictions(path: Path) -> dict[str, dict[str, str]]:
    predictions: dict[str, dict[str, str]] = {}
    for record in read_jsonl(path):
        reaction_id = normalize_reaction_id(record)
        if not reaction_id:
            continue
        predictions[reaction_id] = parse_prediction_labels(record)
    return predictions


def build_comparison_rows(
    references: dict[str, dict[str, str]],
    predictions: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for reaction_id, manual_labels in sorted(references.items()):
        predicted_labels = predictions.get(reaction_id, {})
        row: dict[str, str] = {"reaction_id": reaction_id}
        for column in LABEL_COLUMNS:
            manual_value = manual_labels.get(column, "")
            predicted_value = predicted_labels.get(column, "")
            row[f"manual_{column}"] = manual_value
            row[f"llm_{column}"] = predicted_value
            row[f"match_{column}"] = str(manual_value == predicted_value).upper()
        rows.append(row)
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    fieldnames = ["reaction_id"]
    for column in LABEL_COLUMNS:
        fieldnames.extend([f"manual_{column}", f"llm_{column}", f"match_{column}"])

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_summary(rows: list[dict[str, str]], path: Path) -> None:
    lines = [
        "# Comparacao LLM vs Referencia Manual",
        "",
        f"Total de registros de referencia: {len(rows)}",
        "",
    ]

    rows_with_predictions = [
        row
        for row in rows
        if any(row.get(f"llm_{column}", "") for column in LABEL_COLUMNS)
    ]
    lines.extend(
        [
            f"Registros com predicao LLM: {len(rows_with_predictions)}",
            "",
            "## Acuracia por Campo",
            "",
        ]
    )

    for column in LABEL_COLUMNS:
        evaluated = [
            row
            for row in rows
            if row.get(f"llm_{column}", "")
        ]
        matches = [
            row
            for row in evaluated
            if row.get(f"match_{column}") == "TRUE"
        ]
        accuracy = (len(matches) / len(evaluated)) if evaluated else 0.0
        lines.append(
            f"- `{column}`: {len(matches)}/{len(evaluated)} "
            f"({accuracy:.1%})"
        )

    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    references = load_manual_reference(args.reference)
    predictions = load_predictions(args.predictions)
    rows = build_comparison_rows(references, predictions)
    write_csv(rows, args.output)
    render_summary(rows, args.summary)

    print(f"Referencias: {len(references)}")
    print(f"Predicoes: {len(predictions)}")
    print(f"Comparacao salva em: {args.output}")
    print(f"Resumo salvo em: {args.summary}")


if __name__ == "__main__":
    main()
