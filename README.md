# PLN Queridometro de Torcidas

Projeto academico de Processamento de Linguagem Natural para coleta, organizacao e analise de comentarios publicos sobre futebol brasileiro. A ideia central e construir uma base textual anonima para estudar sentimentos, ironias leves, provocacoes de torcida e padroes linguisticos ligados a clubes brasileiros.

O projeto foi preparado para trabalhar prioritariamente com comentarios publicos obtidos por APIs terceiras autorizadas para consulta ao X/Twitter, sempre respeitando limites eticos, termos de uso e restricoes tecnicas das plataformas. Tambem aceita CSVs externos anonimizados e mantem dados simulados apenas como recurso opcional para testar o pipeline quando nao houver credenciais disponiveis.

## Objetivo Academico

Este repositorio apoia um trabalho de PLN com foco em:

- coletar comentarios publicos sobre futebol brasileiro por APIs terceiras autorizadas;
- anonimizar dados textuais antes do armazenamento;
- limpar e normalizar textos curtos;
- explorar frequencia de termos, hashtags e expressoes;
- preparar datasets para classificacao de sentimentos;
- comparar tecnicas classicas e modernas de PLN.

Classes futuras previstas:

- positivo
- negativo
- neutro
- provocativo/ironico

## Pipeline de PLN

1. Definicao dos clubes e termos de busca.
2. Coleta por API terceira autorizada ou importacao manual de CSVs externos anonimizados.
3. Anonimizacao e armazenamento dos textos.
4. Limpeza textual: lowercase, URLs, mencoes, espacos e quebras de linha.
5. Exploracao inicial: amostras, frequencia de palavras e graficos.
6. Criacao de rotulos manuais.
7. Extracao de atributos com n-grams, TF-IDF e embeddings.
8. Treinamento de modelos classicos e modernos.
9. Avaliacao com metricas como acuracia, precisao, revocacao e F1-score.

## Tecnologias

- Python 3.11+
- pandas
- numpy
- scikit-learn
- nltk
- matplotlib
- jupyter
- python-dotenv
- requests
- beautifulsoup4
- playwright opcional
- pathlib

## Cuidados Eticos

Este projeto nao tenta burlar login, captcha, paywall, bloqueios, rate limits ou mecanismos de protecao do X/Twitter ou de qualquer outra plataforma. A coleta real deve acontecer apenas por APIs terceiras com permissao contratual/termos de uso compativeis com pesquisa academica, ou pela API oficial quando aplicavel. Segundo as politicas atuais do X/Twitter, scraping e automacao fora de canais permitidos podem gerar restricoes, bloqueios ou violar termos de uso.

O projeto evita armazenar informacoes pessoais identificaveis, como username, URL de perfil, ID de usuario, ID do post, foto de perfil, localizacao ou metadados que permitam rastrear autores. Mesmo que uma API retorne esses campos, o coletor salva apenas `text`, `search_term`, `source` e `collected_at`.

## Instalacao

Crie e ative o ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Copie o arquivo `.env.example` para `.env` se quiser ajustar configuracoes locais.

## Coleta via API Terceira

Configure um arquivo `.env` com as variaveis do provedor autorizado:

```env
TWITTER_PROVIDER_NAME=nome_do_provedor
TWITTER_API_BASE_URL=https://api.exemplo.com/search
TWITTER_API_KEY=sua_chave
TWITTER_API_QUERY_PARAM=query
TWITTER_API_ITEMS_PATH=data
TWITTER_API_TEXT_FIELD=text
TWITTER_API_AUTH_HEADER=Authorization
TWITTER_API_AUTH_PREFIX=Bearer
```

Execute:

```bash
python scripts/collect_public_posts.py
```

O arquivo anonimo sera salvo em `data/raw/twitter_public_comments.csv`. Ajuste `TWITTER_API_ITEMS_PATH` e `TWITTER_API_TEXT_FIELD` conforme o formato JSON do provedor escolhido.

### POC Oficial com API do X

Depois de configurar `X_BEARER_TOKEN` no `.env`, colete mencoes recentes aos
perfis oficiais dos 10 clubes definidos na POC:

```bash
python scripts/collect_x_club_mentions.py --tweets-per-club 100 --show-sample
```

O CSV consolidado sera salvo em `data/raw/club_mentions_x_api.csv`. A busca usa
apenas os arrobas oficiais:

```text
@SaoPauloFC @Corinthians @Palmeiras @Flamengo @VascodaGama
@FluminenseFC @Botafogo @SantosFC @Atletico @Cruzeiro
```

Principais colunas geradas:

- `club_name`, `club_handle`: clube alvo da busca.
- `search_query`: consulta enviada para a API, incluindo idioma e filtro de retweets.
- `tweet_id_hash`, `conversation_id_hash`, `author_id_hash`: identificadores anonimizados para deduplicacao e analise de rede.
- `created_at`, `lang`, `text`: data, idioma e texto do tweet para PLN.
- `reference_type`, `referenced_tweet_id_hash`: tipo de relacao quando o tweet referencia outro tweet, como reply, quote ou retweet.
- `mentioned_club_handles`: clubes da POC mencionados no texto.
- `mentioned_user_hashes`: outros usuarios mencionados, anonimizados.
- `retweet_count`, `reply_count`, `like_count`, `quote_count`, `bookmark_count`, `impression_count`: metricas publicas para engajamento.
- `source`, `collected_at`: origem da coleta e horario em que a coleta foi feita.

### POC do Extrator com Scraping

Tambem existe uma POC isolada usando `ntscraper`, biblioteca nao oficial baseada em instancias do Nitter. Ela nao usa API terceira, nao faz login e nao tenta burlar captcha, paywall, bloqueios ou limites. Use apenas para experimentacao academica pequena, pois instancias do Nitter podem ficar indisponiveis e o metodo pode quebrar por mudancas no X/Twitter.

```bash
python scripts/poc_twitter_api_extractor.py --term Flamengo --limit 10 --show-sample
```

O script salva apenas textos anonimizados em `data/raw/poc_ntscraper_comments.csv`.

```bash
python scripts/poc_twitter_api_extractor.py --term futebol --mode term --limit 20 --language pt
```

## Coleta Simulada Opcional

Gere comentarios ficticios em `data/raw/mock_comments.csv`:

```bash
python scripts/collect_mock_data.py
```

## Pre-processamento

Limpe os textos coletados e gere um CSV processado:

```bash
python scripts/preprocess_data.py --input data/raw/twitter_public_comments.csv --output data/processed/twitter_public_comments_clean.csv
```

Para testar com mock, rode `python scripts/preprocess_data.py`.

## Notebook

Abra o notebook de exploracao inicial:

```bash
jupyter notebook notebooks/01_exploracao_inicial.ipynb
```

Ele pode carregar a base real anonima ou a base simulada, mostrar amostras, calcular frequencia de palavras, gerar um grafico simples e reservar espaco para TF-IDF e classificacao futura.

## CSVs Externos

Arquivos externos podem ser adicionados manualmente em `data/raw/`. Recomenda-se que tenham, no minimo, uma coluna `text`. Antes de usar, remova qualquer campo pessoal ou identificavel.

## Estrutura

```text
data/                 Dados brutos, intermediarios e processados
docs/                 Proposta academica e documentacao
notebooks/            Analises exploratorias
scripts/              Entrypoints executaveis
src/queridometro/     Codigo-fonte modular do projeto
tests/                Testes futuros
```

## Proximos Passos

- criar um dataset rotulado manualmente;
- implementar TF-IDF com n-grams;
- treinar Naive Bayes e Regressao Logistica;
- avaliar modelos com F1-score por classe;
- comparar modelos classicos com Transformers em portugues;
- documentar limitacoes e vieses da base textual;
- expandir os testes automatizados.
