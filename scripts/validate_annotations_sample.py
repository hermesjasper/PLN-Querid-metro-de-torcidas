"""Validate manual annotation labels against the project taxonomy."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    PROJECT_ROOT / "data" / "annotated" / "manual_annotation_sample_sao_paulo.csv"
)

ALLOWED_VALUES = {
    "relevancia": {"", "RELEVANTE", "POUCO_INFORMATIVO", "NAO_RELEVANTE"},
    "tema": {
        "",
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
        "",
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
    "polaridade": {"", "POSITIVO", "NEGATIVO", "NEUTRO", "MISTO"},
    "intencao": {
        "",
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
    "validado_manual": {"", "SIM", "NAO"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida rotulos de uma amostra anotada manualmente."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input, encoding="utf-8-sig").fillna("")
    errors: list[str] = []

    for column, allowed in ALLOWED_VALUES.items():
        if column not in df.columns:
            errors.append(f"Coluna ausente: {column}")
            continue

        invalid_values = sorted(set(df[column].astype(str)) - allowed)
        if invalid_values:
            errors.append(f"{column}: valores invalidos {invalid_values}")

    if errors:
        for error in errors:
            print(f"ERRO: {error}")
        raise SystemExit(1)

    annotated_rows = int((df["validado_manual"].astype(str) == "SIM").sum())
    print(f"Amostra valida: {len(df)} linhas")
    print(f"Linhas validadas manualmente: {annotated_rows}")


if __name__ == "__main__":
    main()
