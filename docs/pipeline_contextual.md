# Pipeline Contextual

Esta pipeline prepara a nova PoC do Queridometro de Torcidas, centrada em
publicacoes oficiais de um clube piloto e nas reacoes associadas.

Nesta etapa, a coleta real ainda nao sera executada. O objetivo e deixar a
arquitetura, os documentos, os schemas e os placeholders prontos para a proxima
fase.

## Unidade de Analise

```text
publicacao oficial do clube
-> replies e quote tweets associados
-> classificacao semantica das reacoes
```

Retweets puros nao serao usados como texto de PLN. Eles serao tratados apenas
como metrica de engajamento.

## Etapas

1. Escolha do clube piloto

   Definir um clube inicial para reduzir custo, escopo e complexidade da coleta.
   Valor atual: Sao Paulo (`@SaoPauloFC`).

2. Coleta de tweets oficiais

   Buscar publicacoes feitas pelo perfil oficial do clube piloto. A sugestao
   inicial e coletar 10 a 15 publicacoes oficiais. O primeiro teste controlado
   usa `/2/tweets/search/recent` com `from:SaoPauloFC -is:retweet`. Como a API
   cobra pelos retornos da chamada, todos os posts retornados devem ser salvos.

3. Coleta de replies

   Para cada publicacao oficial, buscar replies associadas. A sugestao inicial e
   limitar a ate 30 replies por publicacao. O teste usa o operador
   `in_reply_to_tweet_id:<post_id>`.

4. Coleta de quote tweets

   Para cada publicacao oficial, buscar quote tweets associados. A sugestao
   inicial e limitar a ate 10 quotes por publicacao. O teste usa o operador
   `quotes_of_tweet_id:<post_id>`.

5. Armazenamento bruto

   Persistir dados brutos em `data/raw/contextual_collection/`, separando
   publicacoes oficiais e reacoes.

6. Pre-processamento textual

   Normalizar espacos, quebras de linha, URLs e ruido textual. A limpeza deve
   preservar o texto suficiente para interpretacao semantica.

7. Classificacao do tipo da publicacao oficial

   Classificar cada post oficial em categorias como `PARTIDA`, `ESCALACAO`,
   `RESULTADO`, `CONTRATACAO`, `MARKETING`, `NOTA_OFICIAL` ou `OUTRO`.

8. Classificacao semantica das reacoes

   Classificar replies e quote tweets por relevancia, tema, emocao, polaridade e
   intencao comunicativa.

9. Validacao manual

   Revisar uma amostra das anotacoes para medir consistencia, corrigir rotulos e
   ajustar a taxonomia.

10. Criacao da base anotada

    Consolidar os dados anotados em `data/annotated/annotated_reactions.csv`.

11. Treino opcional de modelos classicos

    Em etapa futura, treinar modelos como Naive Bayes e Regressao Logistica para
    comparacao com as anotacoes geradas por modelo pronto.

12. Analise final por tipo de publicacao

    Comparar sentimentos, temas e intencoes das reacoes por tipo de post oficial.

## Saidas Esperadas

- `data/raw/contextual_collection/official_posts.csv`
- `data/raw/contextual_collection/post_reactions.csv`
- `data/processed/post_reactions_clean.csv`
- `data/annotated/annotated_reactions.csv`
- `data/metadata/collection_log.csv`

## Restricoes Nesta Etapa

- executar apenas o teste pequeno autorizado de 2 posts oficiais do Sao Paulo;
- nao fazer chamadas reais a GPT ou outro LLM;
- nao treinar modelos;
- nao criar dashboards;
- nao apagar arquivos existentes.
