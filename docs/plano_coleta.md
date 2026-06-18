# Plano de Coleta Contextual

Este plano descreve a coleta futura da base contextual. Nenhuma coleta sera
executada nesta etapa.

## Clube Piloto

`A DEFINIR`

## Escopo Inicial

- publicacoes oficiais: 10 a 15;
- replies por publicacao: ate 30;
- quote tweets por publicacao: ate 10;
- retweets puros: apenas como metrica agregada;
- teto aproximado de novos registros: 500 a 700;
- orcamento maximo adicional: R$ 25.

## Estrategia

1. Escolher o clube piloto.
2. Fazer um teste pequeno com 1 ou 2 publicacoes oficiais.
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
