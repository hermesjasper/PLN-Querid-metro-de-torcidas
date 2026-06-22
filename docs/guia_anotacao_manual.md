# Guia de Anotacao Manual

Este guia orienta o preenchimento de
`data/annotated/manual_annotation_sample_sao_paulo.csv`.

O objetivo desta etapa e validar se a taxonomia funciona em dados reais antes de
usar GPT ou outro modelo pronto como anotador automatico.

## Como Anotar

Para cada linha, leia:

1. `official_text`: publicacao oficial do Sao Paulo.
2. `clean_text`: reacao do torcedor.
3. `reaction_type`: `REPLY` ou `QUOTE`.

Depois preencha:

- `relevancia`
- `tema`
- `emocao`
- `polaridade`
- `intencao`
- `validado_manual`
- `rotulo_corrigido`, se necessario
- `observacoes`, se necessario

Use apenas os rotulos definidos em `docs/taxonomia_classificacao.md`.

## Regras Praticas

### Relevancia

- `RELEVANTE`: comentario interpretavel sobre clube, post, jogo, elenco,
  diretoria, torcida ou contexto.
- `POUCO_INFORMATIVO`: comentario relacionado, mas curto ou pouco analitico,
  como "vamos", "boa", "kkkk".
- `NAO_RELEVANTE`: spam, propaganda, texto sem relacao clara ou impossivel de
  interpretar.

### Tema

Escolha o tema principal da reacao. Se houver mais de um tema, marque aquele que
mais explica a mensagem.

Exemplos:

- critica a jogadores ou elenco: `ELENCO`;
- critica ao treinador: `TECNICO`;
- critica a gestao: `DIRETORIA`;
- comentario sobre desempenho do time: `DESEMPENHO_EM_CAMPO`;
- provocacao a rivais: `RIVALIDADE`;
- comentario sobre a forma de comunicacao do clube: `COMUNICACAO_DO_CLUBE`.

### Emocao

Marque a emocao predominante, nao necessariamente todas as emocoes possiveis.

Exemplos:

- "nao aguento mais esse time": `FRUSTRACAO`;
- xingamento direto: `RAIVA`;
- sarcasmo: `IRONIA`;
- incentivo ao time: `APOIO`;
- sem emocao clara: `NEUTRO`.

### Polaridade

- `POSITIVO`: avaliacao favoravel.
- `NEGATIVO`: avaliacao desfavoravel.
- `NEUTRO`: sem avaliacao clara.
- `MISTO`: contem elementos positivos e negativos.

### Intencao

Marque o objetivo comunicativo principal:

- `ELOGIO`: reconhecimento positivo.
- `CRITICA`: desaprovacao.
- `COBRANCA`: exigencia de acao.
- `PROVOCACAO`: cutucada, rivalidade ou provocacao.
- `MEME_PIADA`: humor ou brincadeira.
- `PERGUNTA`: pergunta direta.
- `PEDIDO`: solicitacao.
- `APOIO`: incentivo.
- `INFORMACAO`: dado ou correcao factual.
- `OUTRO`: quando nada se encaixa bem.

## Campo `validado_manual`

Use:

- `SIM` quando a linha estiver revisada.
- `NAO` enquanto estiver pendente.

## Validacao

Depois de preencher, rode:

```powershell
python scripts/validate_annotations_sample.py
```

O validador confere se os rotulos existem na taxonomia e quantas linhas ja foram
marcadas como `SIM`.
