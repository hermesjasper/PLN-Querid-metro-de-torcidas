"""Fill manual post-type labels for the Sao Paulo official-post sample."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OFFICIAL_POSTS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "official_posts_test_sao_paulo.csv"
)
DEFAULT_REACTIONS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "post_reactions_test_sao_paulo.csv"
)
DEFAULT_SUMMARY = PROJECT_ROOT / "data" / "metadata" / "sao_paulo_post_type_summary.md"

POST_TYPE_LABELS = {
    "2067383876234674418": "BASTIDORES",
    "2067359047389487371": "BASTIDORES",
    "2067338406628090101": "RESULTADO",
    "2067335082092708037": "RESULTADO",
    "2067306869010444494": "PARTIDA",
    "2067306489157501010": "PARTIDA",
    "2067298821130858794": "ESCALACAO",
    "2067291309803503921": "ESCALACAO",
    "2067273833451593965": "BASTIDORES",
    "2067261004287799628": "PRODUTO_CAMISA",
}

POST_TOPIC_LABELS = {
    "2067383876234674418": "FUTEBOL_PROFISSIONAL_MASCULINO",
    "2067359047389487371": "FUTEBOL_PROFISSIONAL_MASCULINO",
    "2067338406628090101": "CATEGORIA_BASE",
    "2067335082092708037": "CATEGORIA_BASE",
    "2067306869010444494": "CATEGORIA_BASE",
    "2067306489157501010": "CATEGORIA_BASE",
    "2067298821130858794": "CATEGORIA_BASE",
    "2067291309803503921": "CATEGORIA_BASE",
    "2067273833451593965": "FUTEBOL_FEMININO",
    "2067261004287799628": "PRODUTO_OFICIAL",
}

POST_TYPE_NOTES = {
    "BASTIDORES": "treino, rotina interna, reapresentacao ou preparacao",
    "RESULTADO": "fim de jogo ou placar divulgado",
    "PARTIDA": "post de acompanhamento de jogo em andamento",
    "ESCALACAO": "divulgacao de time escalado",
    "PRODUTO_CAMISA": "produto oficial ou camisa divulgada para venda",
}

POST_TOPIC_NOTES = {
    "FUTEBOL_PROFISSIONAL_MASCULINO": "elenco profissional masculino",
    "CATEGORIA_BASE": "categorias de base, como Sub-20 e Sub-17",
    "FUTEBOL_FEMININO": "futebol feminino",
    "PRODUTO_OFICIAL": "camisa, loja ou produto oficial",
    "PARCERIA_COMERCIAL": "patrocinador, marca parceira ou ativacao comercial",
    "INSTITUCIONAL": "historia, memoria, valores ou comunicados institucionais",
    "OUTRO": "assunto fora das categorias principais",
}


def infer_post_type(text: object) -> str:
    normalized = str(text).lower()
    if "fim de jogo" in normalized or "placar" in normalized:
        return "RESULTADO"
    if "escalado" in normalized or "escalação" in normalized or "escalacao" in normalized:
        return "ESCALACAO"
    if "bola rolando" in normalized or "hoje tem" in normalized:
        return "PARTIDA"
    if "camisa" in normalized or "sao store" in normalized or "garanta já" in normalized:
        return "PRODUTO_CAMISA"
    if "sócio" in normalized or "socio" in normalized:
        return "SOCIO_TORCEDOR"
    if "nota oficial" in normalized:
        return "NOTA_OFICIAL"
    if "patrocin" in normalized:
        return "PATROCINIO"
    if (
        "treino" in normalized
        or "intertemporada" in normalized
        or "reapresentação" in normalized
        or "reapresentacao" in normalized
        or "trabalhos" in normalized
        or "bastidores" in normalized
    ):
        return "BASTIDORES"
    if "sub-20" in normalized or "sub-17" in normalized or "madeincotia" in normalized:
        return "BASE"
    return "OUTRO"


def infer_post_topic(text: object) -> str:
    normalized = str(text).lower()
    if "feminino" in normalized:
        return "FUTEBOL_FEMININO"
    if "sub-20" in normalized or "sub-17" in normalized or "madeincotia" in normalized:
        return "CATEGORIA_BASE"
    if "camisa" in normalized or "sao store" in normalized or "garanta já" in normalized:
        return "PRODUTO_OFICIAL"
    if "patrocin" in normalized or "parceir" in normalized:
        return "PARCERIA_COMERCIAL"
    if "nota oficial" in normalized or "anivers" in normalized:
        return "INSTITUCIONAL"
    if "treino" in normalized or "intertemporada" in normalized or "reapresent" in normalized:
        return "FUTEBOL_PROFISSIONAL_MASCULINO"
    return "OUTRO"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preenche post_type_manual dos posts oficiais do Sao Paulo."
    )
    parser.add_argument("--official-posts", type=Path, default=DEFAULT_OFFICIAL_POSTS)
    parser.add_argument("--reactions", type=Path, default=DEFAULT_REACTIONS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def compact_text(value: object, max_length: int = 90) -> str:
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rstrip() + "..."


def fill_post_types(posts: pd.DataFrame) -> pd.DataFrame:
    typed = posts.copy()
    typed["post_id"] = typed["post_id"].astype(str)
    manual_labels = typed["post_id"].map(POST_TYPE_LABELS)
    typed["post_type_manual"] = manual_labels.fillna(typed.get("post_type_manual", ""))
    typed["post_type_llm"] = typed["post_type_llm"].where(
        typed["post_type_llm"].astype(str).str.strip() != "",
        typed["official_text"].map(infer_post_type),
    )
    if "post_topic_manual" not in typed:
        typed["post_topic_manual"] = ""
    if "post_topic_llm" not in typed:
        typed["post_topic_llm"] = ""
    topic_manual_labels = typed["post_id"].map(POST_TOPIC_LABELS)
    typed["post_topic_manual"] = topic_manual_labels.fillna(
        typed.get("post_topic_manual", "")
    )
    typed["post_topic_llm"] = typed["post_topic_llm"].where(
        typed["post_topic_llm"].astype(str).str.strip() != "",
        typed["official_text"].map(infer_post_topic),
    )

    effective_type = typed["post_type_manual"].where(
        typed["post_type_manual"].astype(str).str.strip() != "",
        typed["post_type_llm"],
    )
    missing = typed[effective_type.astype(str).str.strip() == ""]
    if not missing.empty:
        missing_ids = ", ".join(missing["post_id"].astype(str).tolist())
        raise ValueError(f"Posts sem classificacao: {missing_ids}")

    effective_topic = typed["post_topic_manual"].where(
        typed["post_topic_manual"].astype(str).str.strip() != "",
        typed["post_topic_llm"],
    )
    missing_topics = typed[effective_topic.astype(str).str.strip() == ""]
    if not missing_topics.empty:
        missing_ids = ", ".join(missing_topics["post_id"].astype(str).tolist())
        raise ValueError(f"Posts sem assunto: {missing_ids}")

    return typed


def render_summary(posts: pd.DataFrame, reactions: pd.DataFrame) -> str:
    reactions_by_post = (
        reactions.groupby(["parent_post_id", "reaction_type"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    reactions_by_post["parent_post_id"] = reactions_by_post["parent_post_id"].astype(str)

    summary_rows = posts.merge(
        reactions_by_post,
        left_on="post_id",
        right_on="parent_post_id",
        how="left",
    ).fillna(0)

    posts = posts.copy()
    posts["official_post_type"] = posts["post_type_manual"].where(
        posts["post_type_manual"].astype(str).str.strip() != "",
        posts["post_type_llm"],
    )
    posts["official_post_topic"] = posts["post_topic_manual"].where(
        posts["post_topic_manual"].astype(str).str.strip() != "",
        posts["post_topic_llm"],
    )

    type_counts = posts["official_post_type"].value_counts().sort_index()
    topic_counts = posts["official_post_topic"].value_counts().sort_index()
    reaction_type_counts = (
        summary_rows.assign(
            official_post_type=summary_rows["post_type_manual"].where(
                summary_rows["post_type_manual"].astype(str).str.strip() != "",
                summary_rows["post_type_llm"],
            )
        )
        .groupby("official_post_type")[["REPLY", "QUOTE"]]
        .sum()
        .astype(int)
        .sort_index()
    )
    topic_reaction_counts = (
        summary_rows.assign(
            official_post_topic=summary_rows["post_topic_manual"].where(
                summary_rows["post_topic_manual"].astype(str).str.strip() != "",
                summary_rows["post_topic_llm"],
            )
        )
        .groupby("official_post_topic")[["REPLY", "QUOTE"]]
        .sum()
        .astype(int)
        .sort_index()
    )

    lines = [
        "# Tipos de Publicacao Oficial - Sao Paulo",
        "",
        "Classificacao manual dos 10 posts oficiais usados na amostra contextual.",
        "",
        "## Criterio",
        "",
        (
            "Quando um post poderia receber mais de um rotulo, foi priorizado o "
            "formato comunicacional da publicacao para facilitar a analise das "
            "reacoes: resultado, escalacao, partida em andamento, bastidores ou produto."
        ),
        "",
        "## Distribuicao de Posts",
        "",
    ]
    for label, count in type_counts.items():
        lines.append(f"- `{label}`: {count}")

    lines.extend(["", "## Distribuicao de Assuntos", ""])
    for label, count in topic_counts.items():
        lines.append(f"- `{label}`: {count}")

    lines.extend(["", "## Reacoes por Tipo de Post", ""])
    for label, row in reaction_type_counts.iterrows():
        lines.append(
            f"- `{label}`: {int(row.get('REPLY', 0))} replies, "
            f"{int(row.get('QUOTE', 0))} quotes"
        )

    lines.extend(["", "## Reacoes por Assunto do Post", ""])
    for label, row in topic_reaction_counts.iterrows():
        lines.append(
            f"- `{label}`: {int(row.get('REPLY', 0))} replies, "
            f"{int(row.get('QUOTE', 0))} quotes"
        )

    lines.extend(["", "## Posts Classificados", ""])
    for _, row in posts.sort_values("created_at", ascending=False).iterrows():
        label = row["official_post_type"]
        topic = row["official_post_topic"]
        source = "manual" if str(row.get("post_type_manual", "")).strip() else "sugerido"
        topic_source = (
            "manual" if str(row.get("post_topic_manual", "")).strip() else "sugerido"
        )
        lines.append(
            f"- `{row['post_id']}` | tipo `{label}` ({source}) | "
            f"assunto `{topic}` ({topic_source}) | "
            f"{POST_TYPE_NOTES.get(label, '')}; {POST_TOPIC_NOTES.get(topic, '')}: "
            f"{compact_text(row['official_text'])}"
        )

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    posts = pd.read_csv(args.official_posts, encoding="utf-8-sig").fillna("")
    reactions = pd.read_csv(args.reactions, encoding="utf-8-sig").fillna("")

    typed_posts = fill_post_types(posts)
    typed_posts.to_csv(args.official_posts, index=False, encoding="utf-8-sig")

    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(render_summary(typed_posts, reactions), encoding="utf-8")

    print(f"Posts classificados: {len(typed_posts)}")
    print(f"CSV atualizado em: {args.official_posts}")
    print(f"Resumo salvo em: {args.summary}")


if __name__ == "__main__":
    main()
