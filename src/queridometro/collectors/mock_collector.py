"""Mock data collector for football comments.

The generated data is fictional and suitable for local experimentation,
classroom demonstrations and pipeline tests without depending on real scraping.
"""

from __future__ import annotations

import random
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from queridometro.config import RAW_DATA_DIR, SEARCH_TERMS

COMMENT_TEMPLATES = [
    "Hoje o {club} jogou muito, deu gosto de ver #futebol",
    "O {club} precisa melhorar essa defesa urgentemente",
    "Torcida do {club} cantou o jogo inteiro, que atmosfera bonita",
    "La vem o {club} me fazer sofrer de novo rs",
    "Se esse meio-campo do {club} encaixar, ninguem segura",
    "O juiz complicou, mas o {club} tambem perdeu gol demais",
    "Grande vitoria do {club}, time mostrou raca",
    "O {club} teve posse, teve chance, mas faltou capricho",
    "Parabens ao {club}, partida muito consistente",
    "Meu {club} e especialista em testar a paciencia da torcida",
    "Que fase do {club}, parece roteiro repetido toda rodada",
    "O ataque do {club} hoje estava inspirado",
    "Defender esse empate do {club} exige muita criatividade",
    "O {club} ganhou e a corneta vai dormir triste hoje",
    "Impressionante como o {club} transforma jogo facil em drama",
    "O {club} mereceu o resultado, jogou com intensidade",
    "A torcida do {club} merece mais organizacao dentro de campo",
    "Que golaço do {club}, daqueles para rever varias vezes",
    "O {club} entrou desligado e pagou caro",
    "Resultado justo para o {club}, jogo equilibrado demais",
]


def generate_mock_comments(
    search_terms: list[str] | None = None,
    comments_per_term: int = 12,
) -> pd.DataFrame:
    """Generate fictional comments for the configured football clubs."""
    terms = search_terms or SEARCH_TERMS
    collected_at = datetime.now(UTC).isoformat(timespec="seconds")
    rows: list[dict[str, str]] = []

    for term in terms:
        for _ in range(comments_per_term):
            template = random.choice(COMMENT_TEMPLATES)
            rows.append(
                {
                    "text": template.format(club=term),
                    "search_term": term,
                    "source": "mock",
                    "collected_at": collected_at,
                }
            )

    random.shuffle(rows)
    return pd.DataFrame(rows)


def save_mock_comments(output_path: Path | None = None) -> Path:
    """Generate and save mock comments as CSV."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    destination = output_path or RAW_DATA_DIR / "mock_comments.csv"
    df = generate_mock_comments()
    df.to_csv(destination, index=False, encoding="utf-8")
    return destination

