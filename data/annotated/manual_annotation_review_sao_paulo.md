# Revisao da Amostra de Anotacao

Use este arquivo apenas para leitura. Preencha os rotulos no CSV:

`data/annotated/manual_annotation_sample_sao_paulo.csv`

## Dicionario de Alternativas

Use exatamente estes valores nas colunas de rotulagem do CSV.

### `relevancia`

`RELEVANTE`, `POUCO_INFORMATIVO`, `NAO_RELEVANTE`

### `tema`

`ELENCO`, `TECNICO`, `DIRETORIA`, `ARBITRAGEM`, `CONTRATACAO`, `DESEMPENHO_EM_CAMPO`, `TORCIDA`, `RIVALIDADE`, `PATROCINIO`, `PARCERIA_COMERCIAL`, `MARKETING`, `PRODUTO_OFICIAL`, `CATEGORIA_BASE`, `FUTEBOL_FEMININO`, `INGRESSOS`, `SOCIO_TORCEDOR`, `COMUNICACAO_DO_CLUBE`, `OUTRO`

### `emocao`

`ALEGRIA`, `ORGULHO`, `RAIVA`, `FRUSTRACAO`, `IRONIA`, `ESPERANCA`, `ANSIEDADE`, `DESCONFIANCA`, `APOIO`, `NEUTRO`

### `polaridade`

`POSITIVO`, `NEGATIVO`, `NEUTRO`, `MISTO`

### `intencao`

`ELOGIO`, `CRITICA`, `COBRANCA`, `PROVOCACAO`, `MEME_PIADA`, `PERGUNTA`, `PEDIDO`, `APOIO`, `INFORMACAO`, `OUTRO`

### `validado_manual`

`SIM`, `NAO`

### `rotulo_corrigido`

Campo livre. Use apenas se quiser registrar uma correcao, duvida ou rotulo alternativo.

### `observacoes`

Campo livre para comentarios curtos sobre ambiguidade, contexto ou dificuldade de classificacao.

## Linha 1

- `reaction_id`: `8105f42cfad58c93`
- `parent_post_id`: `2067261004287799628`
- `reaction_type`: `QUOTE`

**Post oficial:**

Estilo streetwear com a essência do Tricolor. 🔴⚪⚫ A nova Camisa Manga Longa São Paulo New Balance traz conforto, atitude e um visual marcante pra quem vive o SPFC em qualquer ocasião. 🔥 Garanta já a sua na SAO Store. 🛒 https://t.co/B5L6UKbU8u https://t.co/TE6d8Q4DMi

**Reacao:**

400 REAIS VAI SE FUDE https://t.co/WFBIczTeHG https://t.co/YFkTnuFY6n

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `PRODUTO_OFICIAL`
- emocao: `RAIVA`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 2

- `reaction_id`: `94b6a56826c71ce9`
- `parent_post_id`: `2067291309803503921`
- `reaction_type`: `QUOTE`

**Post oficial:**

Brasileiro Sub-20: Tricolor escalado para enfrentar o Juventude, às 15h, no CFAC Juventude, em Caxias do Sul (RS)! #MadeInCotia #VamosSãoPaulo 🇾🇪 https://t.co/qGVoAU099C

**Reacao:**

@WesleydeArajoG1 @SaoPauloFC Oito jogadores que já jogaram nos profissionais, obrigação ganhar e ganhar bem hoje! https://t.co/pIZ50ZKkDq

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DESEMPENHO_EM_CAMPO`
- emocao: `ESPERANCA`
- polaridade: `MISTO`
- intencao: `COBRANCA`
- validado_manual: `SIM`

## Linha 3

- `reaction_id`: `a8b7ed4e140d91f8`
- `parent_post_id`: `2067291309803503921`
- `reaction_type`: `QUOTE`

**Post oficial:**

Brasileiro Sub-20: Tricolor escalado para enfrentar o Juventude, às 15h, no CFAC Juventude, em Caxias do Sul (RS)! #MadeInCotia #VamosSãoPaulo 🇾🇪 https://t.co/qGVoAU099C

**Reacao:**

Nicolas voltou da viagem até a Copa e será titular. Isac no banco. https://t.co/Frr3dWRNub

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `ELENCO`
- emocao: `NEUTRO`
- polaridade: `NEUTRO`
- intencao: `INFORMACAO`
- validado_manual: `SIM`

## Linha 4

- `reaction_id`: `2aabaaa64cd5536e`
- `parent_post_id`: `2067298821130858794`
- `reaction_type`: `QUOTE`

**Post oficial:**

Brasileiro Sub-17: Tricolor escalado para enfrentar o Fluminense, às 15h, no CFA Laudo Natel, em São Paulo (SP)! #MadeInCotia #VamosSãoPaulo 🇾🇪 https://t.co/NR5QVPNdhF

**Reacao:**

Inacreditável, com mais um jogo em Cotia, novamente o São Paulo não transmite o confronto. E o pior que o clube não faz nem questão de explicar a razão pela qual não transmite o confronto. https://t.co/kN589ZZOQB

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `COMUNICACAO_DO_CLUBE`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 5

- `reaction_id`: `41ced19eed799552`
- `parent_post_id`: `2067306869010444494`
- `reaction_type`: `REPLY`

**Post oficial:**

Brasileiro Sub-20: Bola rolando! #JUVxSPFC #MadeInCotia #VamosSãoPaulo 🇾🇪 https://t.co/vvTRnqRkSi

**Reacao:**

@SaoPauloFC Transmissão?

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `COMUNICACAO_DO_CLUBE`
- emocao: `NEUTRO`
- polaridade: `NEUTRO`
- intencao: `PERGUNTA`
- validado_manual: `SIM`

## Linha 6

- `reaction_id`: `43a76c2fd290cacd`
- `parent_post_id`: `2067335082092708037`
- `reaction_type`: `QUOTE`

**Post oficial:**

Brasileiro Sub-17: Fim de jogo #SPFCxFLU (1x4) https://t.co/Fn0ETHCa7U

**Reacao:**

já já o menta desce pro sub-15 e aí vai poder pedir música no fantástico pq fodeu com 3 categorias diferentes 🤩 homem desgraçado e clube falido https://t.co/yTeCgRIIVI

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `TECNICO`
- emocao: `RAIVA`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 7

- `reaction_id`: `e79f7b3f1353d8d4`
- `parent_post_id`: `2067335082092708037`
- `reaction_type`: `QUOTE`

**Post oficial:**

Brasileiro Sub-17: Fim de jogo #SPFCxFLU (1x4) https://t.co/Fn0ETHCa7U

**Reacao:**

Que bom! https://t.co/3WzKDXFmH2

**Rotulos atuais:**

- relevancia: `POUCO_INFORMATIVO`
- tema: `OUTRO`
- emocao: `IRONIA`
- polaridade: `MISTO`
- intencao: `MEME_PIADA`
- validado_manual: `SIM`

## Linha 8

- `reaction_id`: `14d9e4415c8bda7e`
- `parent_post_id`: `2067338406628090101`
- `reaction_type`: `QUOTE`

**Post oficial:**

Brasileiro Sub-20: Fim de jogo #JUVxSPFC (1-0) https://t.co/7jnhqOZ4pm

**Reacao:**

Surreal. Com todos os profissionais e mesmo assim não vence. https://t.co/M1lv2aIQpp

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DESEMPENHO_EM_CAMPO`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 9

- `reaction_id`: `9c606c66fb5ad832`
- `parent_post_id`: `2067338406628090101`
- `reaction_type`: `QUOTE`

**Post oficial:**

Brasileiro Sub-20: Fim de jogo #JUVxSPFC (1-0) https://t.co/7jnhqOZ4pm

**Reacao:**

Estava dormindo ou com vergonha? https://t.co/gVUB0NMyA1

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `COMUNICACAO_DO_CLUBE`
- emocao: `IRONIA`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 10

- `reaction_id`: `abd8ac459484500a`
- `parent_post_id`: `2067338406628090101`
- `reaction_type`: `QUOTE`

**Post oficial:**

Brasileiro Sub-20: Fim de jogo #JUVxSPFC (1-0) https://t.co/7jnhqOZ4pm

**Reacao:**

E assim Cotia vai sendo destruída aos poucos. Com gestões danosas ao clube, além de trazer técnicos com trabalhos muito duvidosos, o São Paulo perde para o lanterna do Brasileirão Sub 20, Juventude, por 1 a 0. https://t.co/zhN8rZqrLu

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `CATEGORIA_BASE`
- emocao: `RAIVA`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 11

- `reaction_id`: `205deac3e67647f4`
- `parent_post_id`: `2067338406628090101`
- `reaction_type`: `REPLY`

**Post oficial:**

Brasileiro Sub-20: Fim de jogo #JUVxSPFC (1-0) https://t.co/7jnhqOZ4pm

**Reacao:**

@SaoPauloFC o SP conseguiu perder com 8 jogadores que integram o elenco profissional do clube que trabalho fantastico

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DESEMPENHO_EM_CAMPO`
- emocao: `IRONIA`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 12

- `reaction_id`: `9d812f849c805229`
- `parent_post_id`: `2067338406628090101`
- `reaction_type`: `REPLY`

**Post oficial:**

Brasileiro Sub-20: Fim de jogo #JUVxSPFC (1-0) https://t.co/7jnhqOZ4pm

**Reacao:**

@SaoPauloFC Misericórdia até aí estamos sofrendo ..... #ForaJulioBatista

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `TECNICO`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `COBRANCA`
- validado_manual: `SIM`

## Linha 13

- `reaction_id`: `d4a031d62491855d`
- `parent_post_id`: `2067338406628090101`
- `reaction_type`: `REPLY`

**Post oficial:**

Brasileiro Sub-20: Fim de jogo #JUVxSPFC (1-0) https://t.co/7jnhqOZ4pm

**Reacao:**

@SaoPauloFC Os dirigentes estão acabando com tudo mesmo.

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DIRETORIA`
- emocao: `RAIVA`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 14

- `reaction_id`: `f07bf7cb84585790`
- `parent_post_id`: `2067338406628090101`
- `reaction_type`: `REPLY`

**Post oficial:**

Brasileiro Sub-20: Fim de jogo #JUVxSPFC (1-0) https://t.co/7jnhqOZ4pm

**Reacao:**

@SaoPauloFC Alguém salva a base do SP

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `CATEGORIA_BASE`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `COBRANCA`
- validado_manual: `SIM`

## Linha 15

- `reaction_id`: `f75e1b7e1cfaa495`
- `parent_post_id`: `2067338406628090101`
- `reaction_type`: `REPLY`

**Post oficial:**

Brasileiro Sub-20: Fim de jogo #JUVxSPFC (1-0) https://t.co/7jnhqOZ4pm

**Reacao:**

@SaoPauloFC Meu Deus, perdemos em casa, fora de casa, qualquer adversário. Que dureza..é Sub tudo, só derrota.

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `CATEGORIA_BASE`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 16

- `reaction_id`: `41d7d5276e73ed44`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `QUOTE`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

ooh nojeira https://t.co/2mqcfEOsB9

**Rotulos atuais:**

- relevancia: `POUCO_INFORMATIVO`
- tema: `ELENCO`
- emocao: `RAIVA`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 17

- `reaction_id`: `4d4e4d68d36c3d1b`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `QUOTE`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

Os bagres voltaram https://t.co/OuG4vjvfyN

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `ELENCO`
- emocao: `IRONIA`
- polaridade: `NEGATIVO`
- intencao: `PROVOCACAO`
- validado_manual: `SIM`

## Linha 18

- `reaction_id`: `6ff6971602527469`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `QUOTE`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

imagina a maldição que não foi esse treino https://t.co/NQV2e04ayt

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `ELENCO`
- emocao: `IRONIA`
- polaridade: `NEGATIVO`
- intencao: `MEME_PIADA`
- validado_manual: `SIM`

## Linha 19

- `reaction_id`: `b44d57b0edd16647`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `QUOTE`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

MELHOR NÃO https://t.co/w16yM6NaSy

**Rotulos atuais:**

- relevancia: `POUCO_INFORMATIVO`
- tema: `OUTRO`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 20

- `reaction_id`: `c4331e3e53897974`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `QUOTE`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

Eu não esqueci https://t.co/7pI8HEDOFD https://t.co/wvX3e1Er85

**Rotulos atuais:**

- relevancia: `POUCO_INFORMATIVO`
- tema: `OUTRO`
- emocao: `DESCONFIANCA`
- polaridade: `NEGATIVO`
- intencao: `COBRANCA`
- validado_manual: `SIM`

## Linha 21

- `reaction_id`: `d2e65593c02c294a`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `QUOTE`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

Só copa agora tá pai. Daqui uns 20 dias me atualiza doq tá acontecendo https://t.co/Refhkq23HJ

**Rotulos atuais:**

- relevancia: `POUCO_INFORMATIVO`
- tema: `OUTRO`
- emocao: `NEUTRO`
- polaridade: `NEUTRO`
- intencao: `OUTRO`
- validado_manual: `SIM`

## Linha 22

- `reaction_id`: `0c603ef2d22dd120`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `REPLY`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

@SaoPauloFC Ninguém liga pra esse timeco

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `RIVALIDADE`
- emocao: `RAIVA`
- polaridade: `NEGATIVO`
- intencao: `PROVOCACAO`
- validado_manual: `SIM`

## Linha 23

- `reaction_id`: `68cb447542e494b2`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `REPLY`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

@SaoPauloFC Nossos Guerreiros! 😫🥱

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `ELENCO`
- emocao: `IRONIA`
- polaridade: `NEGATIVO`
- intencao: `MEME_PIADA`
- validado_manual: `SIM`

## Linha 24

- `reaction_id`: `6bfc8afc0dde956e`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `REPLY`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

@SaoPauloFC Meu sono melhorou, cabelo estava bom, pele mais leve fora o mental, era totalmente outro até ver esse Tweet. Terei que voltar a tomar paroxetina

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DESEMPENHO_EM_CAMPO`
- emocao: `IRONIA`
- polaridade: `NEGATIVO`
- intencao: `MEME_PIADA`
- validado_manual: `SIM`

## Linha 25

- `reaction_id`: `7fb5ad44f36b2247`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `REPLY`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

@SaoPauloFC 😥😥

**Rotulos atuais:**

- relevancia: `POUCO_INFORMATIVO`
- tema: `OUTRO`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `OUTRO`
- validado_manual: `SIM`

## Linha 26

- `reaction_id`: `80dbb51bd9a7553c`
- `parent_post_id`: `2067359047389487371`
- `reaction_type`: `REPLY`

**Post oficial:**

Reapresentação e início da intertemporada tricolor! #VamosSãoPaulo 🇾🇪 📸 Rubens Chiri / São Paulo FC https://t.co/q33LCeJ4ra

**Reacao:**

@SaoPauloFC Não precisa de descanso e nem de treinamento porque esse time não faz nada mesmo.

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DESEMPENHO_EM_CAMPO`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 27

- `reaction_id`: `04f0bd72e12726cb`
- `parent_post_id`: `2067383876234674418`
- `reaction_type`: `REPLY`

**Post oficial:**

As imagens do início da nossa intertemporada! #VamosSãoPaulo 🇾🇪 🎥 Gutierre Filmes https://t.co/eWa3yiY9j2

**Reacao:**

@SaoPauloFC Rui Costa já foi demitido? Já espancaram o Olten a caminho da barra funda pra servir de exemplo? Quantos ratos ainda estão vivos?

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DIRETORIA`
- emocao: `RAIVA`
- polaridade: `NEGATIVO`
- intencao: `COBRANCA`
- validado_manual: `SIM`

## Linha 28

- `reaction_id`: `2935259613b40931`
- `parent_post_id`: `2067383876234674418`
- `reaction_type`: `REPLY`

**Post oficial:**

As imagens do início da nossa intertemporada! #VamosSãoPaulo 🇾🇪 🎥 Gutierre Filmes https://t.co/eWa3yiY9j2

**Reacao:**

@SaoPauloFC Cadê as contratações porra e tem que mandar meio time pra rua

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `CONTRATACAO`
- emocao: `RAIVA`
- polaridade: `NEGATIVO`
- intencao: `COBRANCA`
- validado_manual: `SIM`

## Linha 29

- `reaction_id`: `35d587abe951df47`
- `parent_post_id`: `2067383876234674418`
- `reaction_type`: `REPLY`

**Post oficial:**

As imagens do início da nossa intertemporada! #VamosSãoPaulo 🇾🇪 🎥 Gutierre Filmes https://t.co/eWa3yiY9j2

**Reacao:**

@SaoPauloFC Ninguém aguenta mais esse clube.

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DESEMPENHO_EM_CAMPO`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`

## Linha 30

- `reaction_id`: `4e45a77d1086b8b7`
- `parent_post_id`: `2067383876234674418`
- `reaction_type`: `REPLY`

**Post oficial:**

As imagens do início da nossa intertemporada! #VamosSãoPaulo 🇾🇪 🎥 Gutierre Filmes https://t.co/eWa3yiY9j2

**Reacao:**

@SaoPauloFC Estou tão feliz vendo a copa. Não acredito que eu vou ter que assistir de novo esse time

**Rotulos atuais:**

- relevancia: `RELEVANTE`
- tema: `DESEMPENHO_EM_CAMPO`
- emocao: `FRUSTRACAO`
- polaridade: `NEGATIVO`
- intencao: `CRITICA`
- validado_manual: `SIM`
