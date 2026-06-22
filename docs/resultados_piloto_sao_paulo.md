# Resultados do Piloto Sao Paulo

Este documento resume o estado atual da PoC contextual usando o Sao Paulo
como clube piloto.

## Base Coletada

A coleta contextual piloto usou publicacoes oficiais do perfil `@SaoPauloFC` e
suas reacoes diretamente associadas.

Resumo da base:

- posts oficiais coletados: 10;
- reacoes brutas coletadas: 60;
- reacoes anotadas manualmente: 30;
- predicoes LLM analisadas: 30.

As reacoes incluem replies e quote tweets. Retweets puros permanecem apenas
como metrica agregada, nao como texto analisado.

## Custo Observado

O custo total observado na API do X/Twitter para a base contextual piloto foi
de US$ 0.30:

- US$ 0.13 na primeira rodada;
- US$ 0.17 na segunda rodada.

A regra adotada a partir do teste foi salvar todos os registros retornados pela
API, mesmo quando a chamada retorna mais dados que o minimo esperado, para nao
desperdicar registros cobrados.

## Tipo e Assunto das Publicacoes

Os posts oficiais foram classificados em duas dimensoes:

- `official_post_type`: formato comunicacional da publicacao;
- `official_post_topic`: assunto ou editoria do post.

Tipos de publicacao oficial:

- `BASTIDORES`: 3;
- `RESULTADO`: 2;
- `PARTIDA`: 2;
- `ESCALACAO`: 2;
- `PRODUTO_CAMISA`: 1.

Assuntos das publicacoes oficiais:

- `CATEGORIA_BASE`: 6;
- `FUTEBOL_PROFISSIONAL_MASCULINO`: 2;
- `FUTEBOL_FEMININO`: 1;
- `PRODUTO_OFICIAL`: 1.

Essa separacao foi necessaria porque um mesmo post pode ter formato de
`RESULTADO`, por exemplo, mas tratar da `CATEGORIA_BASE`.

## Anotacao Manual

A amostra manual possui 30 reacoes. A distribuicao dos rotulos manuais indica
predominio de reacoes negativas:

- `NEGATIVO`: 25;
- `NEUTRO`: 3;
- `MISTO`: 2.

Temas mais frequentes:

- `DESEMPENHO_EM_CAMPO`: 7;
- `ELENCO`: 5;
- `OUTRO`: 5;
- `COMUNICACAO_DO_CLUBE`: 3;
- `CATEGORIA_BASE`: 3.

Intencoes mais frequentes:

- `CRITICA`: 14;
- `COBRANCA`: 6;
- `MEME_PIADA`: 4.

## Anotacao com DeepSeek

Foi usada a DeepSeek como anotador automatico, com saida em JSON e validacao
local de taxonomia. A rodada final documentada e `taxonomy_v3`, que adicionou
validacao automatica e retry quando o modelo retornava rotulos invalidos.

Arquivos principais:

```text
data/llm_outputs/reaction_annotation_predictions_taxonomy_v3.jsonl
data/llm_outputs/llm_annotation_comparison_taxonomy_v3.csv
data/llm_outputs/llm_annotation_comparison_summary_taxonomy_v3.md
data/processed/contextual_analysis_sao_paulo_taxonomy_v3.md
```

Resultado da comparacao DeepSeek vs referencia manual:

- `relevancia`: 24/30 (80.0%);
- `tema`: 14/30 (46.7%);
- `emocao`: 21/30 (70.0%);
- `polaridade`: 27/30 (90.0%);
- `intencao`: 18/30 (60.0%).

Na rodada `taxonomy_v3`, nao houve rotulos fora da taxonomia.

## Leitura dos Resultados

A polaridade foi a dimensao mais estavel para o LLM. Isso sugere que o modelo
identifica bem se a reacao e negativa, neutra ou mista, especialmente em textos
curtos e carregados de avaliacao emocional.

O campo `tema` foi o mais dificil. Isso era esperado, porque tema exige decidir
qual e o alvo principal da reacao: elenco, desempenho, diretoria, base,
comunicacao do clube, produto oficial etc. Em muitos casos, a reacao mistura
mais de um alvo.

A intencao teve desempenho intermediario. O modelo identifica bem criticas e
cobrancas em muitos casos, mas ainda pode confundir ironia, piada e critica
direta.

## Limitacoes

- A amostra manual ainda e pequena, com 30 reacoes.
- O piloto usa apenas um clube.
- A coleta veio de uma janela recente da API, portanto reflete um contexto
  especifico do momento.
- A base tem forte predominancia de sentimento negativo.
- A validacao manual foi feita para continuidade da PoC e ainda pode ser
  revisada em uma etapa posterior.

## Proximos Passos

1. Revisar manualmente os casos em que o LLM discordou da referencia.
2. Ajustar criterios de `tema`, que foi a dimensao com menor acordo.
3. Expandir a coleta do Sao Paulo para mais posts oficiais.
4. Repetir a pipeline para outros clubes.
5. Criar uma base maior para testar modelos classicos como baseline.
6. Produzir graficos e tabelas finais para o relatorio academico.
