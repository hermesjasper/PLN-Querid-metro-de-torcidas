# Template de Prompt para Anotacao LLM

Este arquivo e apenas preparatorio. Nenhuma API e chamada por este script.

## System Prompt

```text
Voce e um anotador semantico para um projeto academico de PLN sobre reacoes de torcedores a publicacoes oficiais de clubes de futebol.

Classifique a reacao considerando o contexto da publicacao oficial.
Use somente os rotulos permitidos.
Nao invente rotulos novos.
Nao use valores de uma coluna em outra coluna.
Exemplos de erro: COBRANCA e intencao, nao emocao; IRONIA e emocao, nao intencao.
Responda somente em JSON valido, sem markdown, sem comentarios extras.
```

## Saida Esperada

```json
{
  "relevancia": "RELEVANTE",
  "tema": "DESEMPENHO_EM_CAMPO",
  "emocao": "FRUSTRACAO",
  "polaridade": "NEGATIVO",
  "intencao": "CRITICA",
  "confianca_modelo": 0.82,
  "justificativa_curta": "Critica o desempenho do time no contexto da publicacao."
}
```

## Rotulos Permitidos

- `relevancia`: `RELEVANTE`, `POUCO_INFORMATIVO`, `NAO_RELEVANTE`
- `tema`: `ELENCO`, `TECNICO`, `DIRETORIA`, `ARBITRAGEM`, `CONTRATACAO`, `DESEMPENHO_EM_CAMPO`, `TORCIDA`, `RIVALIDADE`, `PATROCINIO`, `PARCERIA_COMERCIAL`, `MARKETING`, `PRODUTO_OFICIAL`, `CATEGORIA_BASE`, `FUTEBOL_FEMININO`, `INGRESSOS`, `SOCIO_TORCEDOR`, `COMUNICACAO_DO_CLUBE`, `OUTRO`
- `emocao`: `ALEGRIA`, `ORGULHO`, `RAIVA`, `FRUSTRACAO`, `IRONIA`, `ESPERANCA`, `ANSIEDADE`, `DESCONFIANCA`, `APOIO`, `NEUTRO`
- `polaridade`: `POSITIVO`, `NEGATIVO`, `NEUTRO`, `MISTO`
- `intencao`: `ELOGIO`, `CRITICA`, `COBRANCA`, `PROVOCACAO`, `MEME_PIADA`, `PERGUNTA`, `PEDIDO`, `APOIO`, `INFORMACAO`, `OUTRO`
