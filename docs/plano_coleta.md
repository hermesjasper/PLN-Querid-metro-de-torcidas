# Plano de Coleta Contextual

Este plano descreve a coleta futura da base contextual. Nenhuma coleta sera
executada nesta etapa.

## Clube Piloto

Sao Paulo (`@SaoPauloFC`)

## Endpoint do Teste Inicial

O teste inicial usa o endpoint oficial de busca recente:

```text
GET https://api.x.com/2/tweets/search/recent
```

Query planejada:

```text
from:SaoPauloFC -is:retweet
```

A API exige `max_results` entre 10 e 100. Portanto, uma chamada de teste deve
solicitar pelo menos 10 resultados.

Atualizacao operacional: como a API cobra pelos resultados retornados pela
chamada, nao devemos descartar posts retornados com sucesso. A partir de agora,
se a chamada solicitar 10 resultados e a API retornar 10, os 10 devem ser
salvos.

## Custo Observado no Teste

A operacao completa do teste contextual custou US$ 0.13 no Developer Console.
Ela incluiu:

- 1 busca de posts oficiais do Sao Paulo, com `max_results=10`;
- 2 buscas de replies, uma para cada um dos 2 primeiros posts oficiais;
- 2 buscas de quote tweets, uma para cada um dos 2 primeiros posts oficiais;
- 36 registros retornados e salvos no total, somando 10 posts oficiais e 26
  reacoes.

Esse custo deve ser usado como referencia empirica inicial antes de ampliar a
coleta.

A segunda rodada, com replies e quotes dos 8 posts oficiais restantes, custou
US$ 0.17 e retornou 34 novas reacoes. O custo total observado da base contextual
de teste ficou em US$ 0.30, com 10 posts oficiais e 60 reacoes.

## Plano de Anotacao Manual

Antes de chamar um LLM, foi gerada uma amostra manual com 30 reacoes em:

```text
data/annotated/manual_annotation_sample_sao_paulo.csv
```

A amostra foi balanceada com 15 replies e 15 quote tweets. O objetivo e validar
a taxonomia com dados reais antes de gastar chamadas em anotacao automatica.

Campos a preencher:

- `relevancia`;
- `tema`;
- `emocao`;
- `polaridade`;
- `intencao`;
- `validado_manual`;
- `rotulo_corrigido`, se necessario;
- `observacoes`, se necessario.

Depois do preenchimento, validar com:

```powershell
python scripts/validate_annotations_sample.py
```

## Plano para Respostas e Quotes

As buscas de reacoes devem partir de `official_posts.csv` ou do arquivo de teste
`official_posts_test_sao_paulo.csv`. Para cada `post_id` oficial:

- replies: usar `in_reply_to_tweet_id:<post_id> -from:SaoPauloFC -is:retweet`;
- quote tweets: usar `quotes_of_tweet_id:<post_id> -is:retweet`;
- salvar todos os retornos de cada chamada;
- registrar uma linha no `collection_log.csv` para cada busca executada;
- manter `parent_post_id` apontando para o `post_id` oficial;
- anonimizar autor e ID da reacao por hash.

## Escopo Inicial

- publicacoes oficiais: 10 a 15;
- replies por publicacao: ate 30;
- quote tweets por publicacao: ate 10;
- retweets puros: apenas como metrica agregada;
- teto aproximado de novos registros: 500 a 700;
- orcamento maximo adicional: R$ 25.

## Estrategia

1. Usar o Sao Paulo como clube piloto.
2. Fazer um teste pequeno com 2 publicacoes oficiais.
3. Conferir retorno real dos endpoints.
4. Estimar custo por endpoint e por execucao.
5. Registrar a coleta em `data/metadata/collection_log.csv`.
6. Executar coleta completa apenas se o custo estimado estiver dentro do teto.

## Registro Obrigatorio

Cada coleta futura deve gerar uma linha em:

```text
data/metadata/collection_log.csv
```

Cabecalho:

```csv
collection_id,date,club,endpoint,requested_limit,returned_count,estimated_cost,status,notes
```

## Criterios de Parada

- custo estimado acima de R$ 25;
- endpoint retornando campos insuficientes;
- volume muito baixo para analise;
- erro de autenticacao ou permissao;
- mudanca relevante nos limites ou regras da API.

## Observacoes

- A coleta deve preservar dados necessarios para analise contextual.
- IDs brutos devem ser avaliados antes de qualquer publicacao da base.
- O foco da PLN sera replies e quote tweets.
- Retweets devem permanecer como metrica de engajamento.
