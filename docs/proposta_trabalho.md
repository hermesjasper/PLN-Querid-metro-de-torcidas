# Proposta de Trabalho

## Titulo

Queridometro de Torcidas: analise de sentimento e rede em mencoes a clubes
brasileiros no X/Twitter.

## Tema

O projeto investiga comentarios publicos relacionados a grandes clubes do
futebol brasileiro, usando tecnicas de Processamento de Linguagem Natural para
analisar linguagem, sentimento, engajamento e padroes de mencao.

## Problema

Como coletar e organizar uma base textual recente sobre clubes brasileiros no
X/Twitter, preservando cuidados eticos, para permitir analises de sentimento e
rede entre torcidas?

## Objetivo Geral

Construir uma PoC de coleta e analise de tweets recentes que mencionam os perfis
oficiais de 10 clubes brasileiros.

## Objetivos Especificos

- coletar tweets recentes pela API oficial do X;
- pesquisar somente os arrobas oficiais dos clubes selecionados;
- consolidar aproximadamente 100 tweets por clube;
- preservar texto, data, idioma e metricas publicas;
- anonimizar IDs de tweet, conversa e autor;
- preparar a base para analises de sentimento;
- preparar campos uteis para analise de rede de mencoes;
- documentar limites, vieses e cuidados eticos da coleta.

## Clubes Selecionados

```text
@SaoPauloFC
@Corinthians
@Palmeiras
@Flamengo
@VascodaGama
@FluminenseFC
@Botafogo
@SantosFC
@Atletico
@Cruzeiro
```

## Fonte de Dados

A fonte principal e a API oficial do X/Twitter, usando o endpoint de busca
recente. A busca usa o arroba oficial de cada clube, filtro de idioma em
portugues e, por padrao, exclui retweets.

## Estrutura da Base

O principal arquivo gerado e:

```text
data/raw/club_mentions_x_api.csv
```

Campos mais relevantes:

- `club_name` e `club_handle`: clube alvo da busca;
- `text`: conteudo textual para PLN;
- `created_at` e `lang`: metadados temporais e idioma;
- `author_id_hash`, `tweet_id_hash`, `conversation_id_hash`: IDs anonimizados;
- `mentioned_club_handles`: clubes mencionados no texto;
- `mentioned_user_hashes`: usuarios mencionados de forma anonima;
- metricas de engajamento: curtidas, respostas, retweets, quotes, bookmarks e impressoes.

## Metodologia

1. Configurar credencial local da API oficial do X.
2. Executar o coletor para os 10 arrobas definidos.
3. Salvar a base em CSV com encoding UTF-8.
4. Validar volume, colunas, nulos e distribuicao por clube.
5. Limpar e normalizar os textos.
6. Explorar frequencia de termos e mencoes.
7. Aplicar ou rotular sentimento.
8. Construir uma rede de mencoes com identificadores anonimizados.
9. Comparar resultados entre clubes.

## Cuidados Eticos

O trabalho evita armazenar identificadores pessoais brutos. IDs de autores,
tweets e conversas sao convertidos em hashes. O projeto tambem nao usa scraping,
login automatizado, captcha bypass, paywall bypass ou qualquer mecanismo para
burlar restricoes da plataforma.

## Analises Previstas

- distribuicao de tweets por clube;
- termos mais frequentes;
- sentimento por clube;
- relacao entre sentimento e engajamento;
- mencoes cruzadas entre clubes;
- usuarios anonimizados mais conectados na amostra;
- deteccao de respostas, quotes e conversas recorrentes.

## Limitacoes

A busca recente da API representa uma janela curta de tempo e pode refletir
eventos momentaneos, como jogos, polemicas ou noticias. A amostra tambem depende
do plano de API, dos limites de requisicao e do volume retornado pelo endpoint.

## Resultado Esperado

Ao final, espera-se ter uma base inicial organizada, documentada e adequada para
experimentos de PLN e analise de redes sobre torcidas brasileiras no X/Twitter.
