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

Nesta branch, o objetivo e preparar arquitetura, documentacao, taxonomia,
schemas e placeholders. Nenhuma nova coleta da API do X/Twitter sera executada
nesta etapa, nenhuma chamada a GPT ou outro LLM sera feita e nenhum modelo sera
treinado.

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
  metadata/
    collection_log.csv
docs/
  proposta_trabalho.md
  pipeline_contextual.md
  dicionario_dados.md
  taxonomia_classificacao.md
  plano_coleta.md
  spec_pipeline_contextual.md
scripts/
  prepare_contextual_structure.py
  annotate_reactions.py
  validate_annotations_sample.py
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
```

O arquivo `.env` nao deve ser versionado.

## O Que Nao Esta Implementado Nesta Etapa

- coleta real da API do X/Twitter;
- chamada real a GPT ou outro LLM;
- treinamento de modelos;
- notebooks finais;
- dashboards.

## Proximos Passos

1. Conferir o CSV e o log do teste pequeno com Sao Paulo.
2. Estimar custo real da coleta contextual completa.
3. Confirmar endpoint para replies e quote tweets.
4. Executar coleta piloto reduzida de reacoes.
5. Revisar amostra e ajustar taxonomia.
6. Implementar anotacao semantica com modelo pronto.
7. Validar manualmente uma amostra.
8. Preparar comparacao futura com modelos classicos.
