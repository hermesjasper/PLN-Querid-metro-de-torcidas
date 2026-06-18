Estou em uma nova branch do projeto **PLN Queridômetro de Torcidas**. Antes de começar a implementar, inspecione a estrutura atual do repositório e me diga se há alguma decisão essencial faltando. Se faltar algo realmente necessário, faça perguntas objetivas antes de criar arquivos.

Contexto do projeto:

Este é um trabalho acadêmico de Processamento de Linguagem Natural do curso de Ciência de Dados. O projeto começou com uma base de tweets que mencionavam perfis oficiais de clubes, mas agora o escopo foi refinado.

Novo escopo:

O produto será uma PoC de análise contextualizada de publicações oficiais de um clube de futebol e das reações dos torcedores.

A unidade de análise principal será:

publicação oficial do clube
→ respostas e quote tweets associados
→ classificação semântica das reações

O objetivo é entender como torcedores reagem a diferentes tipos de publicação do clube, como partida, escalação, resultado, contratação, patrocínio, marketing, nota oficial, institucional, sócio-torcedor etc.

Importante:

Nesta etapa NÃO quero executar coleta nova da API do X/Twitter.
Quero apenas preparar o repositório para a nova pipeline contextual.

Também NÃO quero gastar chamadas de API agora.

O que precisa ser feito:

1. Inspecionar o repositório atual.
2. Preservar arquivos existentes.
3. Não apagar dados nem notebooks anteriores.
4. Criar a estrutura da nova pipeline contextual.
5. Atualizar documentação.
6. Criar arquivos de configuração e taxonomia.
7. Criar placeholders de scripts/classes quando fizer sentido, mas sem implementar coleta real ainda.
8. Caso alguma decisão crítica esteja faltando, perguntar antes de implementar.

Decisões já tomadas:

* O projeto será uma PoC.
* A API do X/Twitter é cara, então a próxima coleta terá teto de custo.
* A base nova será focada em um clube piloto.
* A coleta futura deve buscar tweets oficiais do clube e reações associadas.
* Retweets puros não serão tratados como texto de PLN, apenas como métrica de engajamento.
* Para PLN, o mais importante serão replies e quote tweets.
* Modelos prontos, inclusive GPT, poderão ser usados como anotadores semânticos.
* Modelos clássicos como Naive Bayes e Regressão Logística poderão ser treinados posteriormente para comparação.
* A análise exploratória será complementar. O centro do trabalho é PLN.

Crie ou atualize a seguinte estrutura, adaptando ao que já existir no repositório:

docs/
├── proposta_trabalho.md
├── pipeline_contextual.md
├── dicionario_dados.md
├── taxonomia_classificacao.md
└── plano_coleta.md

config/
└── taxonomy.yaml

data/
├── raw/
│   ├── initial_mentions/
│   └── contextual_collection/
├── processed/
├── annotated/
└── metadata/
└── collection_log.csv

src/
└── queridometro/
├── collectors/
│   └── contextual_x_collector.py
├── annotation/
│   └── llm_annotator.py
├── preprocessing/
│   └── text_cleaning.py
├── modeling/
│   └── classical_models.py
└── utils/
└── schemas.py

scripts/
├── prepare_contextual_structure.py
├── annotate_reactions.py
└── validate_annotations_sample.py

O que cada documento deve conter:

1. docs/proposta_trabalho.md

Atualizar a proposta do trabalho com:

* título do projeto;
* problema;
* objetivo geral;
* objetivos específicos;
* justificativa;
* mudança de escopo;
* descrição da PoC;
* fonte de dados;
* restrição de custo da API;
* uso de modelos prontos;
* papel dos modelos clássicos;
* entregáveis.

Título sugerido:

**PLN Queridômetro de Torcidas: análise semântica de reações a publicações oficiais de clubes de futebol**

2. docs/pipeline_contextual.md

Descrever a pipeline completa:

1. escolha do clube piloto;
2. coleta de tweets oficiais;
3. coleta de replies;
4. coleta de quote tweets;
5. armazenamento bruto;
6. pré-processamento textual;
7. classificação do tipo da publicação oficial;
8. classificação semântica das reações;
9. validação manual;
10. criação da base anotada;
11. treino opcional de modelos clássicos;
12. análise final por tipo de publicação.

Deixar claro que a coleta ainda não será executada nesta etapa.

3. docs/dicionario_dados.md

Criar o modelo de dados com três tabelas principais:

Tabela 1: official_posts.csv

Campos sugeridos:

* post_id
* club
* club_username
* official_text
* created_at
* lang
* like_count
* reply_count
* retweet_count
* quote_count
* collected_at
* post_type_llm
* post_type_manual

Tabela 2: post_reactions.csv

Campos sugeridos:

* reaction_id
* parent_post_id
* club
* reaction_type
* text
* created_at
* lang
* like_count
* reply_count
* retweet_count
* quote_count
* collected_at
* clean_text

Tabela 3: annotated_reactions.csv

Campos sugeridos:

* reaction_id
* parent_post_id
* club
* reaction_type
* clean_text
* relevancia
* tema
* emocao
* polaridade
* intencao
* confianca_modelo
* justificativa_curta
* validado_manual
* rotulo_corrigido

4. docs/taxonomia_classificacao.md

Criar a taxonomia de classificação.

Tipo de publicação oficial:

* PARTIDA
* ESCALACAO
* RESULTADO
* CONTRATACAO
* MERCADO_DA_BOLA
* PATROCINIO
* MARKETING
* NOTA_OFICIAL
* INSTITUCIONAL
* SOCIO_TORCEDOR
* PRODUTO_CAMISA
* BASTIDORES
* BASE
* OUTRO

Relevância da reação:

* RELEVANTE
* POUCO_INFORMATIVO
* NAO_RELEVANTE

Tema da reação:

* ELENCO
* TECNICO
* DIRETORIA
* ARBITRAGEM
* CONTRATACAO
* DESEMPENHO_EM_CAMPO
* TORCIDA
* RIVALIDADE
* PATROCINIO
* MARKETING
* INGRESSOS
* SOCIO_TORCEDOR
* COMUNICACAO_DO_CLUBE
* OUTRO

Emoção:

* ALEGRIA
* ORGULHO
* RAIVA
* FRUSTRACAO
* IRONIA
* ESPERANCA
* ANSIEDADE
* DESCONFIANCA
* APOIO
* NEUTRO

Polaridade:

* POSITIVO
* NEGATIVO
* NEUTRO
* MISTO

Intenção comunicativa:

* ELOGIO
* CRITICA
* COBRANCA
* PROVOCACAO
* MEME_PIADA
* PERGUNTA
* PEDIDO
* APOIO
* INFORMACAO
* OUTRO

Para cada categoria, incluir descrição curta e exemplos.

5. docs/plano_coleta.md

Criar plano de coleta futura com teto de custo.

Incluir:

* clube piloto: A DEFINIR;
* quantidade sugerida de publicações oficiais: 10 a 15;
* respostas por publicação: até 30;
* quotes por publicação: até 10;
* retweets puros: apenas como métrica agregada;
* teto aproximado de novos registros: 500 a 700;
* orçamento máximo adicional: R$ 25;
* necessidade de registrar cada coleta em collection_log.csv;
* recomendação de fazer teste pequeno antes da coleta completa.

6. config/taxonomy.yaml

Criar a mesma taxonomia em formato YAML para ser usada futuramente pelos scripts.

7. data/metadata/collection_log.csv

Criar arquivo com cabeçalho:

collection_id,date,club,endpoint,requested_limit,returned_count,estimated_cost,status,notes

8. src/queridometro/collectors/contextual_x_collector.py

Criar apenas estrutura/placeholder, sem executar chamadas reais.

O arquivo deve conter:

* docstring explicando o objetivo;
* funções planejadas;
* avisos sobre custo da API;
* placeholders para:

  * obter ID do usuário do clube;
  * buscar publicações oficiais;
  * buscar replies;
  * buscar quote tweets;
  * salvar logs de coleta;
* não fazer requisições reais ainda;
* não exigir token nesta etapa.

9. src/queridometro/annotation/llm_annotator.py

Criar estrutura para futura anotação com LLM.

Incluir:

* função placeholder para classificar publicação oficial;
* função placeholder para classificar reação;
* exemplo de formato JSON esperado;
* comentário de que o modelo pode ser GPT ou outro modelo pronto;
* não chamar API real ainda.

10. src/queridometro/utils/schemas.py

Criar dataclasses ou TypedDicts simples para:

* OfficialPost
* PostReaction
* AnnotatedReaction

11. README.md

Atualizar o README para refletir o novo escopo:

* explicar o produto;
* explicar a pipeline contextual;
* diferenciar base inicial de menções e nova base contextual;
* explicar restrição de custo;
* explicar que a próxima coleta será feita depois;
* mostrar estrutura do repositório;
* listar próximos passos.

12. Não implementar nesta etapa:

* coleta real da API;
* chamada real à API do GPT;
* treinamento real de modelos;
* notebooks finais;
* dashboards.

Nesta branch, o objetivo é preparar arquitetura, documentação e estrutura.

Ao final:

1. Liste os arquivos criados/alterados.
2. Explique o que mudou no repositório.
3. Diga quais decisões ainda precisam ser tomadas antes da coleta.
4. Sugira o próximo commit com mensagem:

git add .
git commit -m "docs: define contextual club reactions pipeline"

Se alguma decisão for indispensável antes de começar, pare e pergunte. Caso contrário, implemente com valores “A DEFINIR” onde necessário.
