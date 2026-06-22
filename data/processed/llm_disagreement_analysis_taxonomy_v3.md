# Analise de Divergencias LLM vs Manual

Relatorio focado nos casos em que a DeepSeek `taxonomy_v3` discordou da referencia manual.

Total de divergencias por campo: 46

## Divergencias por Campo

- `tema`: 16
- `intencao`: 12
- `emocao`: 9
- `relevancia`: 6
- `polaridade`: 3

## Divergencias por Assunto do Post

- `FUTEBOL_PROFISSIONAL_MASCULINO`: 27
- `CATEGORIA_BASE`: 19

## Divergencias por Tipo de Post

- `BASTIDORES`: 27
- `RESULTADO`: 14
- `ESCALACAO`: 4
- `PARTIDA`: 1

## Pares de Divergencia em Tema

- `DESEMPENHO_EM_CAMPO -> CATEGORIA_BASE`: 2
- `COMUNICACAO_DO_CLUBE -> CATEGORIA_BASE`: 2
- `OUTRO -> DESEMPENHO_EM_CAMPO`: 2
- `RIVALIDADE -> DESEMPENHO_EM_CAMPO`: 1
- `DESEMPENHO_EM_CAMPO -> OUTRO`: 1
- `DESEMPENHO_EM_CAMPO -> COMUNICACAO_DO_CLUBE`: 1
- `ELENCO -> DESEMPENHO_EM_CAMPO`: 1
- `TECNICO -> CATEGORIA_BASE`: 1
- `ELENCO -> CATEGORIA_BASE`: 1
- `OUTRO -> ELENCO`: 1
- `OUTRO -> COMUNICACAO_DO_CLUBE`: 1
- `OUTRO -> CATEGORIA_BASE`: 1
- `CATEGORIA_BASE -> DESEMPENHO_EM_CAMPO`: 1

## Casos de Tema para Revisao

### `0c603ef2d22dd120`

- assunto do post: `FUTEBOL_PROFISSIONAL_MASCULINO`
- tipo do post: `BASTIDORES`
- manual: `RIVALIDADE`
- llm: `DESEMPENHO_EM_CAMPO`
- texto: @SaoPauloFC Ninguém liga pra esse timeco

### `14d9e4415c8bda7e`

- assunto do post: `CATEGORIA_BASE`
- tipo do post: `RESULTADO`
- manual: `DESEMPENHO_EM_CAMPO`
- llm: `CATEGORIA_BASE`
- texto: Surreal. Com todos os profissionais e mesmo assim não vence. https://t.co/M1lv2aIQpp

### `35d587abe951df47`

- assunto do post: `FUTEBOL_PROFISSIONAL_MASCULINO`
- tipo do post: `BASTIDORES`
- manual: `DESEMPENHO_EM_CAMPO`
- llm: `OUTRO`
- texto: @SaoPauloFC Ninguém aguenta mais esse clube.

### `41ced19eed799552`

- assunto do post: `CATEGORIA_BASE`
- tipo do post: `PARTIDA`
- manual: `COMUNICACAO_DO_CLUBE`
- llm: `CATEGORIA_BASE`
- texto: @SaoPauloFC Transmissão?

### `6bfc8afc0dde956e`

- assunto do post: `FUTEBOL_PROFISSIONAL_MASCULINO`
- tipo do post: `BASTIDORES`
- manual: `DESEMPENHO_EM_CAMPO`
- llm: `COMUNICACAO_DO_CLUBE`
- texto: @SaoPauloFC Meu sono melhorou, cabelo estava bom, pele mais leve fora o mental, era totalmente outro até ver esse Tweet. Terei que voltar a tomar paroxetina

### `6ff6971602527469`

- assunto do post: `FUTEBOL_PROFISSIONAL_MASCULINO`
- tipo do post: `BASTIDORES`
- manual: `ELENCO`
- llm: `DESEMPENHO_EM_CAMPO`
- texto: imagina a maldição que não foi esse treino https://t.co/NQV2e04ayt

### `7fb5ad44f36b2247`

- assunto do post: `FUTEBOL_PROFISSIONAL_MASCULINO`
- tipo do post: `BASTIDORES`
- manual: `OUTRO`
- llm: `DESEMPENHO_EM_CAMPO`
- texto: @SaoPauloFC 😥😥

### `94b6a56826c71ce9`

- assunto do post: `CATEGORIA_BASE`
- tipo do post: `ESCALACAO`
- manual: `DESEMPENHO_EM_CAMPO`
- llm: `CATEGORIA_BASE`
- texto: @WesleydeArajoG1 @SaoPauloFC Oito jogadores que já jogaram nos profissionais, obrigação ganhar e ganhar bem hoje! https://t.co/pIZ50ZKkDq

### `9c606c66fb5ad832`

- assunto do post: `CATEGORIA_BASE`
- tipo do post: `RESULTADO`
- manual: `COMUNICACAO_DO_CLUBE`
- llm: `CATEGORIA_BASE`
- texto: Estava dormindo ou com vergonha? https://t.co/gVUB0NMyA1

### `9d812f849c805229`

- assunto do post: `CATEGORIA_BASE`
- tipo do post: `RESULTADO`
- manual: `TECNICO`
- llm: `CATEGORIA_BASE`
- texto: @SaoPauloFC Misericórdia até aí estamos sofrendo ..... #ForaJulioBatista

### `a8b7ed4e140d91f8`

- assunto do post: `CATEGORIA_BASE`
- tipo do post: `ESCALACAO`
- manual: `ELENCO`
- llm: `CATEGORIA_BASE`
- texto: Nicolas voltou da viagem até a Copa e será titular. Isac no banco. https://t.co/Frr3dWRNub

### `b44d57b0edd16647`

- assunto do post: `FUTEBOL_PROFISSIONAL_MASCULINO`
- tipo do post: `BASTIDORES`
- manual: `OUTRO`
- llm: `ELENCO`
- texto: MELHOR NÃO https://t.co/w16yM6NaSy

### `c4331e3e53897974`

- assunto do post: `FUTEBOL_PROFISSIONAL_MASCULINO`
- tipo do post: `BASTIDORES`
- manual: `OUTRO`
- llm: `DESEMPENHO_EM_CAMPO`
- texto: Eu não esqueci https://t.co/7pI8HEDOFD https://t.co/wvX3e1Er85

### `d2e65593c02c294a`

- assunto do post: `FUTEBOL_PROFISSIONAL_MASCULINO`
- tipo do post: `BASTIDORES`
- manual: `OUTRO`
- llm: `COMUNICACAO_DO_CLUBE`
- texto: Só copa agora tá pai. Daqui uns 20 dias me atualiza doq tá acontecendo https://t.co/Refhkq23HJ

### `e79f7b3f1353d8d4`

- assunto do post: `CATEGORIA_BASE`
- tipo do post: `RESULTADO`
- manual: `OUTRO`
- llm: `CATEGORIA_BASE`
- texto: Que bom! https://t.co/3WzKDXFmH2

### `f75e1b7e1cfaa495`

- assunto do post: `CATEGORIA_BASE`
- tipo do post: `RESULTADO`
- manual: `CATEGORIA_BASE`
- llm: `DESEMPENHO_EM_CAMPO`
- texto: @SaoPauloFC Meu Deus, perdemos em casa, fora de casa, qualquer adversário. Que dureza..é Sub tudo, só derrota.

## Leitura Inicial

As divergencias em `tema` se concentram em casos em que a reacao mistura alvo esportivo, contexto da base e critica institucional. Isso sugere que a taxonomia precisa de criterios de desempate mais explicitos para decidir entre `CATEGORIA_BASE`, `DESEMPENHO_EM_CAMPO`, `ELENCO`, `DIRETORIA` e `COMUNICACAO_DO_CLUBE`.
