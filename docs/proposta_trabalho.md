# PLN Queridometro de Torcidas

## Titulo

PLN Queridometro de Torcidas: analise semantica de reacoes a publicacoes
oficiais de clubes de futebol.

## Problema

Como analisar, de forma contextualizada, as reacoes de torcedores a diferentes
tipos de publicacoes oficiais de um clube de futebol, preservando limite de
custo, rastreabilidade da coleta e cuidado etico com dados de redes sociais?

## Objetivo Geral

Construir uma PoC academica de PLN para relacionar publicacoes oficiais de um
clube piloto com replies e quote tweets associados, classificando semanticamente
as reacoes dos torcedores.

## Objetivos Especificos

- definir uma pipeline contextual centrada em publicacoes oficiais;
- coletar futuramente um conjunto pequeno de posts oficiais do clube piloto;
- associar cada publicacao oficial a replies e quote tweets;
- ignorar retweets puros como texto de PLN, mantendo-os apenas como metrica;
- estruturar uma base bruta, processada e anotada;
- classificar o tipo da publicacao oficial;
- classificar relevancia, tema, emocao, polaridade e intencao das reacoes;
- validar manualmente uma amostra das anotacoes;
- preparar base para comparacao futura com modelos classicos.

## Justificativa

A base inicial do projeto coletou mencoes a perfis oficiais de clubes. Essa
abordagem e util para exploracao geral, mas mistura contextos diferentes e nao
responde diretamente a pergunta central sobre como torcedores reagem a tipos
especificos de comunicacao do clube.

A nova PoC melhora o desenho metodologico ao usar uma unidade de analise
contextual:

```text
publicacao oficial do clube
-> replies e quote tweets associados
-> classificacao semantica das reacoes
```

Com isso, as analises deixam de observar apenas mencoes soltas e passam a
comparar reacoes a conteudos como partida, escalacao, resultado, contratacao,
patrocinio, marketing, nota oficial, institucional e socio-torcedor.

## Mudanca de Escopo

O escopo anterior era baseado em buscas por arrobas oficiais de 10 clubes. O
novo escopo passa a focar em um clube piloto, ainda a definir, com coleta futura
de publicacoes oficiais e reacoes diretamente associadas.

A base inicial de mencoes permanece preservada como historico e referencia, mas
nao sera o centro da nova pipeline contextual.

## Descricao da PoC

A PoC sera composta por:

- escolha de um clube piloto;
- selecao de 10 a 15 publicacoes oficiais recentes;
- coleta futura de ate 30 replies por publicacao;
- coleta futura de ate 10 quote tweets por publicacao;
- armazenamento bruto das publicacoes e reacoes;
- limpeza textual;
- anotacao semantica com modelo pronto, como GPT ou outro LLM;
- validacao manual de amostra;
- analise comparativa por tipo de publicacao.

## Fonte de Dados

A fonte prevista e a API oficial do X/Twitter. Nesta etapa, nenhuma nova coleta
sera executada. A estrutura sera preparada para coleta posterior com teto de
custo e registro em log.

## Restricao de Custo da API

A API do X/Twitter tem custo relevante para o projeto. A coleta contextual deve
ser pequena, controlada e registrada. O teto inicial sugerido para novos dados e
de R$ 25, com aproximadamente 500 a 700 novos registros no maximo.

Antes da coleta completa, deve ser feito um teste reduzido para confirmar:

- endpoint usado;
- volume retornado;
- custo estimado;
- formato das respostas;
- necessidade de ajustes na taxonomia.

## Uso de Modelos Prontos

Modelos prontos, incluindo GPT ou alternativas equivalentes, poderao ser usados
como anotadores semanticos. O objetivo e obter rotulos iniciais consistentes para
relevancia, tema, emocao, polaridade e intencao comunicativa.

Nesta etapa, nao havera chamadas reais a APIs de LLM.

## Papel dos Modelos Classicos

Modelos classicos, como Naive Bayes e Regressao Logistica, poderao ser treinados
posteriormente para comparacao academica. Eles nao substituem a anotacao
contextual inicial, mas podem servir como baseline ou experimento complementar.

Nesta etapa, nenhum modelo sera treinado.

## Entregaveis

- documentacao da pipeline contextual;
- dicionario de dados;
- taxonomia de classificacao;
- plano de coleta com teto de custo;
- arquivo YAML com taxonomia;
- schemas para os principais objetos de dados;
- placeholders de coleta, anotacao e modelagem;
- log de coleta vazio com cabecalho;
- README atualizado com o novo escopo.
