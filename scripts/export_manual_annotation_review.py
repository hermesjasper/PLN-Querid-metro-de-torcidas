"""Export the manual annotation sample to a readable Markdown review file."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    PROJECT_ROOT / "data" / "annotated" / "manual_annotation_sample_sao_paulo.csv"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "annotated" / "manual_annotation_review_sao_paulo.md"
)

LABEL_DICTIONARY = {
    "relevancia": [
        "RELEVANTE",
        "POUCO_INFORMATIVO",
        "NAO_RELEVANTE",
    ],
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
    "polaridade": [
        "POSITIVO",
        "NEGATIVO",
        "NEUTRO",
        "MISTO",
    ],
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
    "validado_manual": [
        "SIM",
        "NAO",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exporta a amostra de anotacao manual para Markdown."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def safe_text(value: object) -> str:
    return str(value).replace("\r", " ").replace("\n", " ").strip()


def build_label_dictionary_lines() -> list[str]:
    lines = [
        "## Dicionario de Alternativas",
        "",
        "Use exatamente estes valores nas colunas de rotulagem do CSV.",
        "",
    ]
    for column, values in LABEL_DICTIONARY.items():
        lines.extend(
            [
                f"### `{column}`",
                "",
                ", ".join(f"`{value}`" for value in values),
                "",
            ]
        )

    lines.extend(
        [
            "### `rotulo_corrigido`",
            "",
            "Campo livre. Use apenas se quiser registrar uma correcao, duvida ou "
            "rotulo alternativo.",
            "",
            "### `observacoes`",
            "",
            "Campo livre para comentarios curtos sobre ambiguidade, contexto ou "
            "dificuldade de classificacao.",
            "",
        ]
    )
    return lines


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input, encoding="utf-8-sig").fillna("")

    lines: list[str] = [
        "# Revisao da Amostra de Anotacao",
        "",
        "Use este arquivo apenas para leitura. Preencha os rotulos no CSV:",
        "",
        "`data/annotated/manual_annotation_sample_sao_paulo.csv`",
        "",
        *build_label_dictionary_lines(),
    ]

    for index, row in df.reset_index(drop=True).iterrows():
        lines.extend(
            [
                f"## Linha {index + 1}",
                "",
                f"- `reaction_id`: `{safe_text(row['reaction_id'])}`",
                f"- `parent_post_id`: `{safe_text(row['parent_post_id'])}`",
                f"- `reaction_type`: `{safe_text(row['reaction_type'])}`",
                "",
                "**Post oficial:**",
                "",
                safe_text(row["official_text"]),
                "",
                "**Reacao:**",
                "",
                safe_text(row["clean_text"]),
                "",
                "**Rotulos atuais:**",
                "",
                f"- relevancia: `{safe_text(row['relevancia'])}`",
                f"- tema: `{safe_text(row['tema'])}`",
                f"- emocao: `{safe_text(row['emocao'])}`",
                f"- polaridade: `{safe_text(row['polaridade'])}`",
                f"- intencao: `{safe_text(row['intencao'])}`",
                f"- validado_manual: `{safe_text(row['validado_manual'])}`",
                "",
            ]
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown salvo em: {args.output}")
    print(f"Linhas exportadas: {len(df)}")


if __name__ == "__main__":
    main()
