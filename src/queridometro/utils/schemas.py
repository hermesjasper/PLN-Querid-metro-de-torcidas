"""Typed schemas for the contextual club reactions pipeline."""

from __future__ import annotations

from typing import TypedDict


class OfficialPost(TypedDict, total=False):
    post_id: str
    club: str
    club_username: str
    official_text: str
    created_at: str
    lang: str
    like_count: int
    reply_count: int
    retweet_count: int
    quote_count: int
    collected_at: str
    post_type_llm: str
    post_type_manual: str


class PostReaction(TypedDict, total=False):
    reaction_id: str
    parent_post_id: str
    club: str
    reaction_type: str
    text: str
    created_at: str
    lang: str
    like_count: int
    reply_count: int
    retweet_count: int
    quote_count: int
    collected_at: str
    clean_text: str


class AnnotatedReaction(TypedDict, total=False):
    reaction_id: str
    parent_post_id: str
    club: str
    reaction_type: str
    clean_text: str
    relevancia: str
    tema: str
    emocao: str
    polaridade: str
    intencao: str
    confianca_modelo: float
    justificativa_curta: str
    validado_manual: bool
    rotulo_corrigido: str
