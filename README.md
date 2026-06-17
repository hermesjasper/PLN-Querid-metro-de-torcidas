# Queridometro de Torcidas

PoC academica de Processamento de Linguagem Natural para analisar mencoes no
X/Twitter aos perfis oficiais de grandes clubes brasileiros.

O objetivo e construir uma base inicial de tweets recentes para estudar
sentimento, engajamento, linguagem de torcida e relacoes de mencao entre clubes
e usuarios, preservando cuidado etico no armazenamento dos dados.

## Base Coletada

A coleta principal usa a API oficial do X, endpoint de busca recente, pesquisando
somente os arrobas oficiais dos clubes:

```text
@SaoPauloFC
@Corinthians
@Palmeiras
@Flamengo
@VascodaGama
@FluminenseFC
@Botafogo
@SantosFC
@Atletico
@Cruzeiro
```

O resultado consolidado esta em:

```text
data/raw/club_mentions_x_api.csv
```

Tambem foi mantido o primeiro teste bem-sucedido:

```text
data/raw/palmeiras_tweets.csv
```

## Colunas Principais

O CSV consolidado foi pensado para analises de texto, sentimento, engajamento e
rede:

- `club_name`, `club_handle`: clube usado como alvo da busca.
- `search_query`: consulta enviada para a API.
- `tweet_id_hash`, `conversation_id_hash`, `author_id_hash`: identificadores anonimizados.
- `created_at`, `lang`, `text`: data, idioma e texto do tweet.
- `reference_type`, `referenced_tweet_id_hash`: relacao com outro tweet, quando existir.
- `mentioned_club_handles`: clubes da PoC mencionados no texto.
- `mentioned_user_hashes`: outros usuarios mencionados, anonimizados.
- `retweet_count`, `reply_count`, `like_count`, `quote_count`, `bookmark_count`, `impression_count`: metricas publicas de engajamento.
- `public_metrics_json`: metricas originais em JSON.
- `source`, `collected_at`: origem e momento da coleta.

## Cuidados Eticos

O projeto nao salva IDs brutos de tweets, conversas ou autores. Esses campos sao
convertidos para hashes estaveis, permitindo deduplicacao e analise de rede sem
expor diretamente identificadores pessoais.

O arquivo `.env` nao deve ser versionado. Use `.env.example` como modelo e
configure localmente o token da API:

```env
X_BEARER_TOKEN=seu_token
```

## Instalacao

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Como Coletar Novamente

Execute a coleta consolidada:

```powershell
python scripts/collect_x_club_mentions.py --tweets-per-club 100 --show-sample
```

O script salva o resultado em:

```text
data/raw/club_mentions_x_api.csv
```

Para rodar apenas o teste simples de uma busca:

```powershell
python first_test_poc.py --term Palmeiras --limit 5
```

## Analises Previstas

- limpeza e normalizacao dos textos;
- analise exploratoria por clube;
- frequencia de termos, hashtags e mencoes;
- sentimento por clube;
- comparacao de engajamento;
- rede de mencoes entre clubes e usuarios anonimizados;
- rotulagem manual de amostras;
- treinamento futuro de classificadores de sentimento.

## Arquivos Centrais

```text
first_test_poc.py
scripts/collect_x_club_mentions.py
data/raw/palmeiras_tweets.csv
data/raw/club_mentions_x_api.csv
docs/proposta_trabalho.md
```
