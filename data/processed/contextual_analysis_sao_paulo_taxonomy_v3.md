# Analise Contextual - Sao Paulo

Relatorio gerado a partir da amostra piloto contextual.

## Cobertura da Base

- posts oficiais coletados: 10
- reacoes brutas coletadas: 60
- reacoes anotadas manualmente: 30
- predicoes LLM analisadas: 30

## Tipos de Publicacao Oficial

- `BASTIDORES`: 3
- `RESULTADO`: 2
- `PARTIDA`: 2
- `ESCALACAO`: 2
- `PRODUTO_CAMISA`: 1

## Assuntos da Publicacao Oficial

- `CATEGORIA_BASE`: 6
- `FUTEBOL_PROFISSIONAL_MASCULINO`: 2
- `FUTEBOL_FEMININO`: 1
- `PRODUTO_OFICIAL`: 1

## Polaridade Manual

- `NEGATIVO`: 25
- `NEUTRO`: 3
- `MISTO`: 2

## Temas Manuais das Reacoes

- `DESEMPENHO_EM_CAMPO`: 7
- `ELENCO`: 5
- `OUTRO`: 5
- `COMUNICACAO_DO_CLUBE`: 3
- `CATEGORIA_BASE`: 3
- `TECNICO`: 2
- `DIRETORIA`: 2
- `PRODUTO_OFICIAL`: 1
- `RIVALIDADE`: 1
- `CONTRATACAO`: 1

## Intencoes Manuais das Reacoes

- `CRITICA`: 14
- `COBRANCA`: 6
- `MEME_PIADA`: 4
- `PROVOCACAO`: 2
- `OUTRO`: 2
- `INFORMACAO`: 1
- `PERGUNTA`: 1

## Acuracia DeepSeek vs Manual

- `relevancia`: 24/30 (80.0%)
- `tema`: 14/30 (46.7%)
- `emocao`: 21/30 (70.0%)
- `polaridade`: 27/30 (90.0%)
- `intencao`: 18/30 (60.0%)

## Rotulos Invalidos do LLM

Total de rotulos fora da taxonomia: 0

- nenhum registro

## Tabelas Geradas

- `data/processed/contextual_analysis_tables_v3/manual_polaridade_por_tipo_post.csv`
- `data/processed/contextual_analysis_tables_v3/manual_polaridade_por_assunto_post.csv`
- `data/processed/contextual_analysis_tables_v3/manual_tema_por_assunto_post.csv`
- `data/processed/contextual_analysis_tables_v3/manual_intencao_por_tipo_post.csv`
