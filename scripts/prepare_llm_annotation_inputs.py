"""Prepare offline LLM annotation inputs without calling any model API."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    PROJECT_ROOT / "data" / "annotated" / "manual_annotation_sample_sao_paulo.csv"
)
DEFAULT_OFFICIAL_POSTS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "official_posts_test_sao_paulo.csv"
)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "llm_inputs"

TAXONOMY = {
    "relevancia": ["RELEVANTE", "POUCO_INFORMATIVO", "NAO_RELEVANTE"],
    "tema": [
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
    ],
    "emocao": [
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
    ],
    "polaridade": ["POSITIVO", "NEGATIVO", "NEUTRO", "MISTO"],
    "intencao": [
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
    ],
}


SYSTEM_PROMPT = """Voce e um anotador semantico para um projeto academico de PLN sobre reacoes de torcedores a publicacoes oficiais de clubes de futebol.

Classifique a reacao considerando o contexto da publicacao oficial.
Use somente os rotulos permitidos.
Nao invente rotulos novos.
Nao use valores de uma coluna em outra coluna.
Exemplos de erro: COBRANCA e intencao, nao emocao; IRONIA e emocao, nao intencao.
Responda somente em JSON valido, sem markdown, sem comentarios extras.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera prompts JSONL para anotacao futura via LLM."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--official-posts", type=Path, default=DEFAULT_OFFICIAL_POSTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--include-unvalidated",
        action="store_true",
        help="Inclui linhas ainda nao validadas manualmente.",
    )
    parser.add_argument(
        "--prompts-file",
        default="reaction_annotation_prompts.jsonl",
        help="Nome do arquivo JSONL de prompts.",
    )
    parser.add_argument(
        "--reference-file",
        default="manual_reference_labels.jsonl",
        help="Nome do arquivo JSONL de referencia manual.",
    )
    parser.add_argument(
        "--template-file",
        default="reaction_annotation_prompt_template.md",
        help="Nome do arquivo Markdown com template do prompt.",
    )
    return parser.parse_args()


def compact_text(value: object) -> str:
    return str(value).replace("\r", " ").replace("\n", " ").strip()


def build_user_prompt(row: pd.Series) -> str:
    taxonomy_text = "\n".join(
        f"- {column}: {', '.join(values)}" for column, values in TAXONOMY.items()
    )
    return f"""Taxonomia permitida:
{taxonomy_text}

Publicacao oficial do clube:
{compact_text(row['official_text'])}

Tipo da publicacao oficial:
{compact_text(row.get('official_post_type', ''))}

Assunto da publicacao oficial:
{compact_text(row.get('official_post_topic', ''))}

Tipo de reacao:
{compact_text(row['reaction_type'])}

Reacao do torcedor:
{compact_text(row['clean_text'])}

Retorne exatamente este formato:
{{
  "relevancia": "...",
  "tema": "...",
  "emocao": "...",
  "polaridade": "...",
  "intencao": "...",
  "confianca_modelo": 0.0,
  "justificativa_curta": "..."
}}
"""


def build_prompt_record(row: pd.Series) -> dict[str, object]:
    return {
        "custom_id": f"reaction-{row['reaction_id']}",
        "reaction_id": compact_text(row["reaction_id"]),
        "parent_post_id": compact_text(row["parent_post_id"]),
        "club": compact_text(row["club"]),
        "official_post_type": compact_text(row.get("official_post_type", "")),
        "official_post_topic": compact_text(row.get("official_post_topic", "")),
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(row)},
        ],
    }


def build_manual_reference_record(row: pd.Series) -> dict[str, object]:
    return {
        "reaction_id": compact_text(row["reaction_id"]),
        "parent_post_id": compact_text(row["parent_post_id"]),
        "official_post_type": compact_text(row.get("official_post_type", "")),
        "official_post_topic": compact_text(row.get("official_post_topic", "")),
        "manual_labels": {
            "relevancia": compact_text(row["relevancia"]),
            "tema": compact_text(row["tema"]),
            "emocao": compact_text(row["emocao"]),
            "polaridade": compact_text(row["polaridade"]),
            "intencao": compact_text(row["intencao"]),
            "justificativa_curta": compact_text(row["justificativa_curta"]),
        },
    }


def write_jsonl(records: list[dict[str, object]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_prompt_template(path: Path) -> None:
    lines = [
        "# Template de Prompt para Anotacao LLM",
        "",
        "Este arquivo e apenas preparatorio. Nenhuma API e chamada por este script.",
        "",
        "## System Prompt",
        "",
        "```text",
        SYSTEM_PROMPT.strip(),
        "```",
        "",
        "## Saida Esperada",
        "",
        "```json",
        json.dumps(
            {
                "relevancia": "RELEVANTE",
                "tema": "DESEMPENHO_EM_CAMPO",
                "emocao": "FRUSTRACAO",
                "polaridade": "NEGATIVO",
                "intencao": "CRITICA",
                "confianca_modelo": 0.82,
                "justificativa_curta": "Critica o desempenho do time no contexto da publicacao.",
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "## Rotulos Permitidos",
        "",
    ]
    for column, values in TAXONOMY.items():
        lines.append(f"- `{column}`: " + ", ".join(f"`{value}`" for value in values))
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


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
    ).fillna("")


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input, encoding="utf-8-sig").fillna("")
    official_posts = pd.read_csv(args.official_posts, encoding="utf-8-sig").fillna("")
    df = add_official_post_type(df, official_posts)
    if args.include_unvalidated:
        selected_rows = df.copy()
    else:
        selected_rows = df[df["validado_manual"].astype(str).str.upper() == "SIM"].copy()

    prompt_records = [build_prompt_record(row) for _, row in selected_rows.iterrows()]
    reference_records = [
        build_manual_reference_record(row)
        for _, row in selected_rows.iterrows()
        if str(row.get("validado_manual", "")).upper() == "SIM"
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(prompt_records, args.output_dir / args.prompts_file)
    write_jsonl(reference_records, args.output_dir / args.reference_file)
    write_prompt_template(args.output_dir / args.template_file)

    print(f"Prompts gerados: {len(prompt_records)}")
    print(f"Referencias manuais geradas: {len(reference_records)}")
    print(f"Diretorio: {args.output_dir}")


if __name__ == "__main__":
    main()
