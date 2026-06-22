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
- coletar um conjunto pequeno de posts oficiais do clube piloto;
- associar cada publicacao oficial a replies e quote tweets;
- ignorar retweets puros como texto de PLN, mantendo-os apenas como metrica;
- estruturar uma base bruta, processada e anotada;
- classificar tipo e assunto da publicacao oficial;
- classificar relevancia, tema, emocao, polaridade e intencao das reacoes;
- validar manualmente uma amostra das anotacoes;
- comparar anotacao automatica com referencia manual;
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
comparar reacoes a conteudos como partida, escalacao, resultado, bastidores,
produto oficial, categorias de base e futebol feminino.

## Mudanca de Escopo

O escopo anterior era baseado em buscas por arrobas oficiais de 10 clubes. O
novo escopo foca em um clube piloto, o Sao Paulo (`@SaoPauloFC`), com coleta de
publicacoes oficiais e reacoes diretamente associadas.

A base inicial de mencoes permanece preservada como historico e referencia, mas
nao e o centro da nova pipeline contextual.

## Descricao da PoC

A PoC e composta por:

- escolha do Sao Paulo como clube piloto;
- selecao de publicacoes oficiais recentes;
- coleta de replies por publicacao;
- coleta de quote tweets por publicacao;
- armazenamento bruto das publicacoes e reacoes;
- limpeza textual;
- classificacao de tipo e assunto dos posts oficiais;
- anotacao semantica com modelo pronto;
- validacao manual de amostra;
- analise comparativa por tipo e assunto de publicacao.

## Fonte de Dados

A fonte de dados e a API oficial do X/Twitter. O piloto usou
`/2/tweets/search/recent` para coletar posts oficiais recentes do Sao Paulo e
buscar replies e quote tweets associados.

O projeto adota a regra de salvar todos os registros retornados pela API, ja que
a cobranca ocorre pela chamada/retorno e descartar excedentes desperdicaria
dados pagos.

## Restricao de Custo da API

A API do X/Twitter tem custo relevante para o projeto. A coleta contextual deve
ser pequena, controlada e registrada.

No piloto do Sao Paulo, o custo observado foi:

- US$ 0.13 na primeira rodada;
- US$ 0.17 na segunda rodada;
- US$ 0.30 no total.

Esse custo gerou uma base com 10 posts oficiais e 60 reacoes brutas.

Antes de novas expansoes, deve ser feito um teste reduzido para confirmar:

- endpoint usado;
- volume retornado;
- custo estimado;
- formato das respostas;
- necessidade de ajustes na taxonomia.

## Uso de Modelos Prontos

Modelos prontos, como DeepSeek ou alternativas equivalentes, podem ser usados
como anotadores semanticos. O objetivo e obter rotulos iniciais consistentes para
relevancia, tema, emocao, polaridade e intencao comunicativa.

No piloto, a DeepSeek foi usada como anotador automatico e comparada com uma
amostra validada manualmente.

## Papel dos Modelos Classicos

Modelos classicos, como Naive Bayes e Regressao Logistica, poderao ser treinados
posteriormente para comparacao academica. Eles nao substituem a anotacao
contextual inicial, mas podem servir como baseline ou experimento complementar.

Nesta etapa, nenhum modelo classico foi treinado.

## Resultados Parciais do Piloto

O piloto atual do Sao Paulo possui:

- 10 posts oficiais coletados;
- 60 reacoes brutas;
- 30 reacoes anotadas manualmente;
- classificacao de tipo e assunto das publicacoes oficiais;
- anotacao automatica com DeepSeek;
- relatorio contextual inicial.

Na rodada `taxonomy_v3`, a comparacao entre DeepSeek e referencia manual
resultou em:

- `relevancia`: 24/30 (80.0%);
- `tema`: 14/30 (46.7%);
- `emocao`: 21/30 (70.0%);
- `polaridade`: 27/30 (90.0%);
- `intencao`: 18/30 (60.0%).

A principal dificuldade observada foi o campo `tema`, por exigir uma decisao
mais fina sobre o alvo da reacao. A polaridade foi o campo com melhor
desempenho.

## Entregaveis

- documentacao da pipeline contextual;
- dicionario de dados;
- taxonomia de classificacao;
- plano de coleta com teto de custo;
- arquivo YAML com taxonomia;
- scripts de coleta, anotacao, comparacao e analise;
- logs e resumos de coleta;
- base piloto anotada;
- relatorio de resultados do piloto;
- README atualizado com o estado atual do projeto.
