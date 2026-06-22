# Analise LLM Expandida - Sao Paulo

Relatorio exploratorio com rotulos automaticos da DeepSeek para a amostra expandida.

## Cobertura

- reacoes na amostra expandida: 150
- reacoes com predicao LLM: 150

## Tipo de Reacao

- `QUOTE`: 75
- `REPLY`: 75

## Tipo de Publicacao Oficial

- `OUTRO`: 75
- `BASTIDORES`: 28
- `PRODUTO_CAMISA`: 15
- `RESULTADO`: 12
- `PARTIDA`: 12
- `ESCALACAO`: 4
- `BASE`: 4

## Assunto da Publicacao Oficial

- `OUTRO`: 67
- `FUTEBOL_PROFISSIONAL_MASCULINO`: 27
- `CATEGORIA_BASE`: 20
- `INSTITUCIONAL`: 20
- `PRODUTO_OFICIAL`: 15
- `FUTEBOL_FEMININO`: 1

## Polaridade LLM

- `NEGATIVO`: 77
- `POSITIVO`: 39
- `NEUTRO`: 31
- `MISTO`: 3

## Temas LLM

- `OUTRO`: 32
- `ELENCO`: 28
- `COMUNICACAO_DO_CLUBE`: 19
- `DESEMPENHO_EM_CAMPO`: 17
- `DIRETORIA`: 14
- `CATEGORIA_BASE`: 13
- `PRODUTO_OFICIAL`: 10
- `RIVALIDADE`: 6
- `CONTRATACAO`: 5
- `TECNICO`: 2
- `TORCIDA`: 2
- `MARKETING`: 2

## Emocoes LLM

- `FRUSTRACAO`: 32
- `IRONIA`: 31
- `NEUTRO`: 25
- `RAIVA`: 19
- `ALEGRIA`: 19
- `ORGULHO`: 9
- `APOIO`: 7
- `DESCONFIANCA`: 4
- `ANSIEDADE`: 3
- `ESPERANCA`: 1

## Intencoes LLM

- `CRITICA`: 65
- `INFORMACAO`: 20
- `APOIO`: 18
- `ELOGIO`: 12
- `COBRANCA`: 8
- `MEME_PIADA`: 8
- `PROVOCACAO`: 7
- `OUTRO`: 5
- `PEDIDO`: 4
- `PERGUNTA`: 3

## Leitura Inicial

Esta analise ainda nao substitui validacao manual. Ela serve para explorar a base 5x maior e identificar padroes gerais antes de selecionar novos casos para revisao humana.

## Tabelas Geradas

- `data/processed/expanded_llm_analysis_tables/llm_polaridade_por_tipo_post.csv`
- `data/processed/expanded_llm_analysis_tables/llm_polaridade_por_assunto_post.csv`
- `data/processed/expanded_llm_analysis_tables/llm_tema_por_assunto_post.csv`
- `data/processed/expanded_llm_analysis_tables/llm_intencao_por_tipo_post.csv`
