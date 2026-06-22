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

- `relevancia`: 23/30 (76.7%)
- `tema`: 13/30 (43.3%)
- `emocao`: 20/30 (66.7%)
- `polaridade`: 26/30 (86.7%)
- `intencao`: 19/30 (63.3%)

## Rotulos Invalidos do LLM

Total de rotulos fora da taxonomia: 3

- `emocao`: 2
- `intencao`: 1

### Casos

- `94b6a56826c71ce9`: campo `emocao` recebeu `COBRANCA`
- `d2e65593c02c294a`: campo `intencao` recebeu `IRONIA`
- `68cb447542e494b2`: campo `emocao` recebeu `CANSACO`

## Tabelas Geradas

- `data/processed/contextual_analysis_tables/manual_polaridade_por_tipo_post.csv`
- `data/processed/contextual_analysis_tables/manual_polaridade_por_assunto_post.csv`
- `data/processed/contextual_analysis_tables/manual_tema_por_assunto_post.csv`
- `data/processed/contextual_analysis_tables/manual_intencao_por_tipo_post.csv`
