"""Generate the final Markdown report and figures for the Sao Paulo PoC."""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".tmp" / "matplotlib"))

import matplotlib.pyplot as plt
import pandas as pd


DOCS_DIR = PROJECT_ROOT / "docs"
FIGURES_DIR = PROJECT_ROOT / "data" / "processed" / "final_report_figures"
REPORT_PATH = DOCS_DIR / "relatorio_final.md"

OFFICIAL_POSTS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "official_posts_test_sao_paulo.csv"
)
REACTIONS = (
    PROJECT_ROOT / "data" / "raw" / "contextual_collection" / "post_reactions_test_sao_paulo.csv"
)
MANUAL_ANNOTATED = PROJECT_ROOT / "data" / "annotated" / "annotated_reactions_sao_paulo.csv"
EXPANDED_LLM = PROJECT_ROOT / "data" / "processed" / "expanded_llm_annotations_sao_paulo.csv"
COMPARISON = PROJECT_ROOT / "data" / "llm_outputs" / "llm_annotation_comparison_taxonomy_v3.csv"

LABEL_COLUMNS = ["relevancia", "tema", "emocao", "polaridade", "intencao"]


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig").fillna("")


def effective_post_context(posts: pd.DataFrame) -> pd.DataFrame:
    df = posts.copy()
    df["official_post_type"] = df["post_type_manual"].where(
        df["post_type_manual"].astype(str).str.strip() != "",
        df["post_type_llm"],
    )
    df["official_post_topic"] = df["post_topic_manual"].where(
        df["post_topic_manual"].astype(str).str.strip() != "",
        df["post_topic_llm"],
    )
    return df


def save_bar(
    series: pd.Series,
    path: Path,
    *,
    title: str,
    xlabel: str = "",
    ylabel: str = "Quantidade",
    color: str = "#2f6f9f",
    horizontal: bool = False,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 5))
    if horizontal:
        ax = series.sort_values().plot(kind="barh", color=color)
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
    else:
        ax = series.plot(kind="bar", color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=30, ha="right")
    ax.set_title(title)
    ax.grid(axis="x" if horizontal else "y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_stacked_bar(df: pd.DataFrame, path: Path, *, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 5.5))
    ax = df.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 5.5),
        color=["#2f6f9f", "#d1495b", "#edae49", "#66a182", "#8d6cab"],
    )
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("Quantidade")
    ax.grid(axis="y", alpha=0.25)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def comparison_accuracy(comparison: pd.DataFrame) -> pd.Series:
    values: dict[str, float] = {}
    for column in LABEL_COLUMNS:
        llm_column = f"llm_{column}"
        match_column = f"match_{column}"
        evaluated = comparison[comparison[llm_column].astype(str).str.strip() != ""]
        matches = evaluated[evaluated[match_column].astype(str).str.upper() == "TRUE"]
        values[column] = round((len(matches) / len(evaluated)) * 100, 1) if len(evaluated) else 0.0
    return pd.Series(values)


def generate_figures(
    posts: pd.DataFrame,
    reactions: pd.DataFrame,
    manual: pd.DataFrame,
    expanded: pd.DataFrame,
    comparison: pd.DataFrame,
) -> dict[str, Path]:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    figures = {
        "coverage": FIGURES_DIR / "fig_01_cobertura_base.png",
        "polarity": FIGURES_DIR / "fig_02_polaridade_expandida.png",
        "themes": FIGURES_DIR / "fig_03_temas_expandida.png",
        "accuracy": FIGURES_DIR / "fig_04_acuracia_deepseek_manual.png",
        "topic_polarity": FIGURES_DIR / "fig_05_polaridade_por_assunto.png",
    }

    coverage = pd.Series(
        {
            "Posts oficiais": len(posts),
            "Reacoes brutas": len(reactions),
            "Amostra manual": len(manual),
            "Amostra expandida LLM": len(expanded),
        }
    )
    save_bar(
        coverage,
        figures["coverage"],
        title="Cobertura da Base Contextual",
        color="#2f6f9f",
    )

    save_bar(
        expanded["polaridade"].value_counts(),
        figures["polarity"],
        title="Polaridade na Amostra Expandida (DeepSeek)",
        color="#d1495b",
    )

    save_bar(
        expanded["tema"].value_counts().head(10),
        figures["themes"],
        title="Temas Mais Frequentes na Amostra Expandida (DeepSeek)",
        color="#66a182",
        horizontal=True,
    )

    save_bar(
        comparison_accuracy(comparison),
        figures["accuracy"],
        title="Acuracia DeepSeek vs Referencia Manual",
        ylabel="Acuracia (%)",
        color="#edae49",
    )

    topic_polarity = (
        expanded.groupby(["official_post_topic", "polaridade"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )
    save_stacked_bar(
        topic_polarity,
        figures["topic_polarity"],
        title="Polaridade por Assunto do Post Oficial (DeepSeek)",
    )

    return figures


def count_lines(counter: Counter[str] | list[tuple[str, int]]) -> list[str]:
    items = counter.most_common() if isinstance(counter, Counter) else counter
    return [f"- `{label}`: {count}" for label, count in items]


def figure_link(path: Path, alt: str) -> str:
    relative = path.relative_to(DOCS_DIR).as_posix() if path.is_relative_to(DOCS_DIR) else f"../{path.relative_to(PROJECT_ROOT).as_posix()}"
    return f"![{alt}]({relative})"


def render_report(
    posts: pd.DataFrame,
    reactions: pd.DataFrame,
    manual: pd.DataFrame,
    expanded: pd.DataFrame,
    comparison: pd.DataFrame,
    figures: dict[str, Path],
) -> str:
    post_context = effective_post_context(posts)
    accuracy = comparison_accuracy(comparison)
    lines = [
        "# Relatorio Final - PLN Queridometro de Torcidas",
        "",
        "## Resumo",
        "",
        (
            "Este trabalho apresenta uma PoC de Processamento de Linguagem Natural "
            "para analisar reacoes de torcedores a publicacoes oficiais de clubes "
            "de futebol. A versao final usa o Sao Paulo como clube piloto e adota "
            "uma pipeline contextual: publicacao oficial, replies e quote tweets "
            "associados, anotacao semantica e analise agregada."
        ),
        "",
        "Nao foi incluido baseline classico nesta versao. A avaliacao ficou concentrada na comparacao entre anotacao manual e anotacao automatica com DeepSeek.",
        "",
        "## Problema e Objetivo",
        "",
        (
            "O problema investigado e como analisar, de forma contextualizada, "
            "as reacoes de torcedores a diferentes tipos de comunicacao oficial "
            "de um clube. O objetivo foi construir uma base contextual pequena, "
            "rastreavel e de baixo custo, capaz de sustentar analises sobre "
            "polaridade, tema, emocao e intencao comunicativa."
        ),
        "",
        "## Metodologia",
        "",
        "A metodologia foi organizada em seis etapas:",
        "",
        "1. Coleta de posts oficiais do `@SaoPauloFC` via endpoint `/2/tweets/search/recent`.",
        "2. Coleta de replies e quote tweets associados aos posts oficiais.",
        "3. Classificacao de tipo e assunto das publicacoes oficiais.",
        "4. Anotacao manual inicial de 30 reacoes.",
        "5. Anotacao automatica com DeepSeek.",
        "6. Analise comparativa e exploratoria dos resultados.",
        "",
        "## Base de Dados",
        "",
        f"- posts oficiais salvos: {len(posts)};",
        f"- reacoes brutas salvas: {len(reactions)};",
        f"- reacoes com validacao manual inicial: {len(manual)};",
        f"- reacoes na amostra expandida anotada por LLM: {len(expanded)}.",
        "",
        figure_link(figures["coverage"], "Cobertura da base contextual"),
        "",
        "## Custos Observados",
        "",
        "- piloto inicial X/Twitter: US$ 0.30;",
        "- expansao X/Twitter: US$ 0.0175;",
        "- expansao DeepSeek: US$ 0.01.",
        "",
        "Os custos reforcam a importancia de registrar cada chamada e salvar todos os registros retornados pela API.",
        "",
        "## Taxonomia",
        "",
        "A taxonomia final separa duas dimensoes do post oficial:",
        "",
        "- `official_post_type`: formato comunicacional, como `RESULTADO`, `ESCALACAO`, `BASTIDORES` ou `PRODUTO_CAMISA`;",
        "- `official_post_topic`: assunto/editoria, como `CATEGORIA_BASE`, `FUTEBOL_FEMININO`, `PRODUTO_OFICIAL` ou `FUTEBOL_PROFISSIONAL_MASCULINO`.",
        "",
        "As reacoes foram classificadas por `relevancia`, `tema`, `emocao`, `polaridade` e `intencao`.",
        "",
        "## Distribuicao dos Posts Oficiais",
        "",
        "Tipos de publicacao oficial:",
        "",
        *count_lines(Counter(post_context["official_post_type"])),
        "",
        "Assuntos das publicacoes oficiais:",
        "",
        *count_lines(Counter(post_context["official_post_topic"])),
        "",
        "## Resultados da Amostra Manual",
        "",
        "A amostra manual inicial apresentou forte predominancia negativa:",
        "",
        *count_lines(Counter(manual["polaridade"])),
        "",
        "Essa concentracao indica que o periodo coletado capturou uma torcida bastante critica em relacao ao clube.",
        "",
        "## Comparacao DeepSeek vs Manual",
        "",
        "A rodada `taxonomy_v3` usou validacao local de taxonomia e retry quando o modelo retornava rotulos invalidos. O resultado foi:",
        "",
        *[f"- `{field}`: {value:.1f}%" for field, value in accuracy.items()],
        "",
        figure_link(figures["accuracy"], "Acuracia DeepSeek vs referencia manual"),
        "",
        "A polaridade foi a dimensao mais estavel. O campo `tema` foi o mais dificil, pois exige decidir qual e o alvo principal da reacao quando ha sobreposicao entre elenco, desempenho, diretoria, base e comunicacao do clube.",
        "",
        "## Analise Expandida com DeepSeek",
        "",
        "A amostra expandida possui 150 reacoes, balanceadas entre replies e quotes:",
        "",
        *count_lines(Counter(expanded["reaction_type"])),
        "",
        "Distribuicao de polaridade na amostra expandida:",
        "",
        *count_lines(Counter(expanded["polaridade"])),
        "",
        figure_link(figures["polarity"], "Polaridade na amostra expandida"),
        "",
        "Temas mais frequentes na amostra expandida:",
        "",
        *count_lines(Counter(expanded["tema"]).most_common(10)),
        "",
        figure_link(figures["themes"], "Temas mais frequentes na amostra expandida"),
        "",
        "A amostra expandida mostra predominancia de reacoes negativas, mas tambem inclui volume relevante de reacoes positivas e neutras. Isso ajuda a observar diferencas entre posts de produto, institucional, categoria de base e futebol profissional.",
        "",
        figure_link(figures["topic_polarity"], "Polaridade por assunto do post oficial"),
        "",
        "## Discussao",
        "",
        (
            "Os resultados indicam que a abordagem contextual melhora a qualidade "
            "analitica em relacao a buscas soltas por mencoes. Ao associar cada "
            "reacao ao post oficial que a originou, torna-se possivel comparar "
            "como a torcida reage a formatos e assuntos diferentes."
        ),
        "",
        (
            "A DeepSeek apresentou bom desempenho para polaridade e relevancia, "
            "mas mostrou maior dificuldade no campo `tema`. Isso sugere que a "
            "taxonomia precisa de criterios de desempate mais explicitos quando "
            "a reacao mistura critica ao desempenho, cobranca de elenco, mencao "
            "a categorias de base e avaliacao da comunicacao do clube."
        ),
        "",
        "## Limitacoes",
        "",
        "- o estudo usa apenas um clube piloto;",
        "- a amostra manual validada ainda tem 30 reacoes;",
        "- a amostra expandida foi rotulada automaticamente e ainda precisa de revisao humana;",
        "- a coleta reflete uma janela recente especifica;",
        "- nao houve treinamento ou comparacao com modelos classicos nesta versao.",
        "",
        "## Conclusao",
        "",
        (
            "A PoC demonstra que e viavel construir uma pipeline contextual de "
            "baixo custo para analisar reacoes de torcedores. O projeto ja possui "
            "coleta rastreavel, taxonomia, anotacao manual inicial, anotacao LLM, "
            "analise de divergencias e graficos exploratorios. Para uma proxima "
            "etapa, a prioridade deve ser ampliar a validacao manual da amostra "
            "expandida e refinar os criterios do campo `tema`."
        ),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    posts = read_csv(OFFICIAL_POSTS)
    reactions = read_csv(REACTIONS)
    manual = read_csv(MANUAL_ANNOTATED)
    expanded = read_csv(EXPANDED_LLM)
    comparison = read_csv(COMPARISON)

    figures = generate_figures(posts, reactions, manual, expanded, comparison)
    REPORT_PATH.write_text(
        render_report(posts, reactions, manual, expanded, comparison, figures),
        encoding="utf-8",
    )

    print(f"Relatorio salvo em: {REPORT_PATH}")
    print(f"Figuras salvas em: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
