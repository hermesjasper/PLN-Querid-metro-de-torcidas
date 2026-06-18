"""Placeholders for future semantic annotation with a ready-made model.

The annotator may use GPT or another suitable LLM in a later stage. This module
does not call any external API and does not require credentials.
"""

from __future__ import annotations

from typing import Any


EXPECTED_REACTION_JSON = {
    "relevancia": "RELEVANTE",
    "tema": "DESEMPENHO_EM_CAMPO",
    "emocao": "FRUSTRACAO",
    "polaridade": "NEGATIVO",
    "intencao": "CRITICA",
    "confianca_modelo": 0.82,
    "justificativa_curta": "Critica o desempenho do time no contexto do jogo.",
}

EXPECTED_OFFICIAL_POST_JSON = {
    "post_type": "RESULTADO",
    "confianca_modelo": 0.9,
    "justificativa_curta": "O texto informa o placar final da partida.",
}


def classify_official_post(official_text: str) -> dict[str, Any]:
    """Placeholder for classifying the type of an official club post."""
    raise NotImplementedError(
        "Future step: call a configured LLM or local classifier for post type."
    )


def classify_reaction(clean_text: str, official_context: str) -> dict[str, Any]:
    """Placeholder for classifying a fan reaction with official post context."""
    raise NotImplementedError(
        "Future step: call a configured LLM or local classifier for reaction labels."
    )


def build_reaction_annotation_prompt(clean_text: str, official_context: str) -> str:
    """Build a future prompt template without sending it to any model."""
    return (
        "Classifique a reacao de torcedor abaixo usando a taxonomia do projeto.\n"
        f"Publicacao oficial: {official_context}\n"
        f"Reacao: {clean_text}\n"
        "Responda somente em JSON com relevancia, tema, emocao, polaridade, "
        "intencao, confianca_modelo e justificativa_curta."
    )
