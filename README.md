# PLN Queridometro de Torcidas

PoC academica de Processamento de Linguagem Natural para analisar reacoes de
torcedores a publicacoes oficiais de clubes de futebol.

O projeto comecou com uma base inicial de mencoes a perfis oficiais, mas o
escopo atual foi refinado para uma pipeline contextual:

```text
publicacao oficial do clube
-> replies e quote tweets associados
-> classificacao semantica das reacoes
```

Nesta branch, o projeto evoluiu da preparacao estrutural para um piloto
contextual com o Sao Paulo. Ja existe uma base pequena coletada, uma amostra
anotada manualmente, uma rodada de anotacao com DeepSeek e uma primeira analise
comparativa.

## Produto

O produto esperado e uma base contextual que permita responder perguntas como:

- quais tipos de publicacao oficial geram mais reacoes negativas ou positivas;
- quais temas aparecem em replies e quote tweets;
- quando a torcida elogia, critica, cobra, ironiza ou apoia;
- como reacoes mudam entre posts de partida, escalacao, resultado, contratacao,
  marketing, nota oficial e outros tipos.

## Base Inicial de Mencoes

A base inicial permanece preservada como historico do projeto:

```text
data/raw/club_mentions_x_api.csv
data/raw/palmeiras_tweets.csv
```

Ela foi criada por buscas a arrobas oficiais de clubes. Essa base e util para
exploracao geral, mas nao e o centro da nova pipeline contextual.

## Nova Pipeline Contextual

A nova coleta sera focada no clube piloto Sao Paulo (`@SaoPauloFC`) e deve
seguir o plano documentado em:

```text
docs/pipeline_contextual.md
docs/plano_coleta.md
```

Fluxo previsto:

1. escolher clube piloto;
2. coletar 10 a 15 publicacoes oficiais;
3. coletar ate 30 replies por publicacao;
4. coletar ate 10 quote tweets por publicacao;
5. armazenar dados brutos;
6. limpar textos;
7. classificar o tipo da publicacao oficial;
8. classificar semanticamente as reacoes;
9. validar manualmente uma amostra;
10. criar base anotada;
11. treinar modelos classicos apenas em etapa futura;
12. analisar resultados por tipo de publicacao.

## Restricao de Custo

A API do X/Twitter tem custo relevante. A proxima coleta deve ter teto de custo
e registro obrigatorio em:

```text
data/metadata/collection_log.csv
```

Plano inicial:

- clube piloto: Sao Paulo (`@SaoPauloFC`);
- publicacoes oficiais: 10 a 15;
- replies por publicacao: ate 30;
- quotes por publicacao: ate 10;
- retweets puros: apenas metrica agregada;
- teto aproximado de novos registros: 500 a 700;
- orcamento maximo adicional: R$ 25.

Custo observado no teste contextual completo: **US$ 0.13**. Esse valor cobriu 1
busca de posts oficiais, 2 buscas de replies e 2 buscas de quote tweets,
resultando em 10 posts oficiais e 26 reacoes salvas.

A segunda rodada, coletando replies e quotes dos 8 posts oficiais restantes,
custou **US$ 0.17** e adicionou 34 reacoes. Custo total observado da base
contextual de teste: **US$ 0.30**, com 10 posts oficiais e 60 reacoes.

Antes da coleta completa, deve ser feito um teste pequeno para validar endpoint,
retorno, custo e formato dos dados. O teste inicial autorizado usa:

```text
GET https://api.x.com/2/tweets/search/recent
query=from:SaoPauloFC -is:retweet
```

Por regra do endpoint, `max_results` precisa ficar entre 10 e 100. Como a API
cobra pelos retornos da chamada, a pipeline agora salva todos os posts
retornados e nao descarta excedentes.

Para buscar reacoes dos posts oficiais salvos, a pipeline usa:

```text
in_reply_to_tweet_id:<post_id> -from:SaoPauloFC -is:retweet
quotes_of_tweet_id:<post_id> -is:retweet
```

## Taxonomia

A taxonomia de classificacao esta documentada em:

```text
docs/taxonomia_classificacao.md
config/taxonomy.yaml
```

Ela cobre:

- tipo de publicacao oficial;
- relevancia da reacao;
- tema;
- emocao;
- polaridade;
- intencao comunicativa.

## Estrutura do Repositorio

```text
config/
  taxonomy.yaml
data/
  raw/
    initial_mentions/
    contextual_collection/
  processed/
  annotated/
    manual_annotation_sample_sao_paulo.csv
  metadata/
    collection_log.csv
docs/
  proposta_trabalho.md
  pipeline_contextual.md
  dicionario_dados.md
  taxonomia_classificacao.md
  plano_coleta.md
  resultados_piloto_sao_paulo.md
  spec_pipeline_contextual.md
scripts/
  prepare_contextual_structure.py
  annotate_reactions.py
  validate_annotations_sample.py
  prepare_manual_annotation_sample.py
  collect_x_club_mentions.py
  poc_twitter_api_extractor.py
  test_collect_sao_paulo_official_posts.py
  collect_sao_paulo_contextual_reactions.py
src/
  queridometro/
    collectors/contextual_x_collector.py
    annotation/llm_annotator.py
    preprocessing/text_cleaning.py
    modeling/classical_models.py
    utils/schemas.py
```

## Instalacao

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Configure o token localmente apenas quando a etapa de coleta for autorizada:

```env
X_BEARER_TOKEN=seu_token
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sua_chave_deepseek
DEEPSEEK_MODEL=deepseek-v4-flash
OPENAI_API_KEY=sua_chave_openai
OPENAI_MODEL=gpt-5.5
```

O arquivo `.env` nao deve ser versionado.

## Estado Atual

- piloto contextual do Sao Paulo coletado;
- 10 posts oficiais e 60 reacoes brutas salvas;
- 30 reacoes anotadas manualmente;
- classificacao de tipo e assunto das publicacoes oficiais;
- anotacao LLM com DeepSeek;
- comparacao DeepSeek vs referencia manual;
- relatorio contextual piloto gerado.

Ainda nao ha treinamento de modelos classicos, notebooks finais ou dashboard.

## Anotacao Manual

A primeira amostra de anotacao manual foi gerada em:

```text
data/annotated/manual_annotation_sample_sao_paulo.csv
```

Ela contem 30 reacoes, balanceadas entre replies e quote tweets:

```text
REPLY: 15
QUOTE: 15
```

As colunas de rotulagem devem ser preenchidas manualmente com base na taxonomia:

```text
relevancia
tema
emocao
polaridade
intencao
validado_manual
rotulo_corrigido
observacoes
```

Para validar os rotulos preenchidos:

```powershell
python scripts/validate_annotations_sample.py
```

Para ler a amostra com mais conforto antes de preencher o CSV:

```powershell
python scripts/export_manual_annotation_review.py
```

Depois da validacao manual, a base anotada inicial pode ser gerada com:

```powershell
python scripts/build_annotated_reactions_dataset.py
```

Saidas:

```text
data/annotated/annotated_reactions_sao_paulo.csv
data/annotated/annotation_summary_sao_paulo.md
```

Para preparar entradas offline para uma futura anotacao via LLM, sem chamar API:

```powershell
python scripts/prepare_llm_annotation_inputs.py
```

Saidas:

```text
data/llm_inputs/reaction_annotation_prompts.jsonl
data/llm_inputs/manual_reference_labels.jsonl
data/llm_inputs/reaction_annotation_prompt_template.md
```

Quando houver respostas do LLM em JSONL, salve em:

```text
data/llm_outputs/reaction_annotation_predictions.jsonl
```

Para gerar respostas com LLM, o provedor padrao do projeto e a DeepSeek, usando
formato compativel com o SDK da OpenAI:

```powershell
python scripts/run_llm_annotation.py --limit 3 --dry-run
python scripts/run_llm_annotation.py --limit 3
```

Tambem e possivel escolher explicitamente o provedor:

```powershell
python scripts/run_llm_annotation.py --provider deepseek --limit 3
python scripts/run_llm_annotation.py --provider openai --limit 3
```

E compare com a referencia manual:

```powershell
python scripts/compare_llm_annotations.py
```

Saidas:

```text
data/llm_outputs/llm_annotation_comparison.csv
data/llm_outputs/llm_annotation_comparison_summary.md
```

Rodada final recomendada da PoC:

```powershell
python scripts/run_llm_annotation.py --limit 30 --max-retries 2 --output data/llm_outputs/reaction_annotation_predictions_taxonomy_v3.jsonl
python scripts/compare_llm_annotations.py --predictions data/llm_outputs/reaction_annotation_predictions_taxonomy_v3.jsonl --output data/llm_outputs/llm_annotation_comparison_taxonomy_v3.csv --summary data/llm_outputs/llm_annotation_comparison_summary_taxonomy_v3.md
python scripts/analyze_contextual_results.py --predictions data/llm_outputs/reaction_annotation_predictions_taxonomy_v3.jsonl --comparison data/llm_outputs/llm_annotation_comparison_taxonomy_v3.csv --output data/processed/contextual_analysis_sao_paulo_taxonomy_v3.md --tables-dir data/processed/contextual_analysis_tables_v3
```

Resumo da rodada `taxonomy_v3`:

```text
relevancia: 24/30 (80.0%)
tema: 14/30 (46.7%)
emocao: 21/30 (70.0%)
polaridade: 27/30 (90.0%)
intencao: 18/30 (60.0%)
```

O documento principal dos resultados esta em:

```text
docs/resultados_piloto_sao_paulo.md
```

### Custo da Anotacao LLM

Segundo a pagina oficial de precos da DeepSeek, o modelo `deepseek-v4-flash`
cobra por tokens de entrada e saida. Em 22/06/2026, os valores publicados eram:

- input cache miss: US$ 0.14 por 1M tokens;
- output: US$ 0.28 por 1M tokens.

Com a amostra atual de 30 reacoes, o custo esperado deve ficar bem abaixo de
US$ 2, mesmo considerando prompts longos e respostas em JSON. Ainda assim, a
execucao deve comecar com `--limit 3` para validar formato, custo e estabilidade
antes de processar todos os registros.

## Proximos Passos

1. Revisar divergencias entre DeepSeek e anotacao manual.
2. Refinar criterios do campo `tema`.
3. Expandir a coleta do Sao Paulo para mais posts oficiais.
4. Repetir a pipeline em outros clubes.
5. Preparar baseline com modelos classicos.
6. Consolidar graficos e tabelas para o relatorio final.
