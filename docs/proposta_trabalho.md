# PLN Queridometro de Torcidas

## Introducao

O futebol brasileiro mobiliza comunidades intensas, criativas e altamente participativas nas redes sociais. Comentarios sobre jogos, clubes, tecnicos e jogadores formam um material rico para estudos de Processamento de Linguagem Natural, especialmente por conter opinioes, humor, ironia, provocacoes e expressoes regionais.

## Problema

Como coletar, organizar e analisar comentarios textuais sobre futebol brasileiro de forma etica e anonima, permitindo a identificacao de sentimentos e padroes linguisticos associados a torcidas?

## Justificativa

O projeto permite aplicar tecnicas classicas e modernas de PLN em um dominio culturalmente relevante. Alem disso, incentiva discussoes sobre privacidade, anonimização, vieses de dados, limites de scraping e uso responsavel de informacoes publicas.

## Objetivo Geral

Construir um pipeline academico de PLN para analisar comentarios publicos ou simulados sobre futebol brasileiro, com foco em sentimentos e padroes de linguagem de torcidas.

## Objetivos Especificos

- gerar uma base inicial de comentarios ficticios realistas;
- aceitar CSVs externos anonimizados;
- limpar e normalizar textos curtos;
- explorar frequencias de palavras, hashtags e expressoes;
- preparar dados para rotulagem manual;
- treinar modelos classicos de classificacao;
- comparar abordagens classicas com modelos modernos baseados em Transformers.

## Metodologia

O trabalho sera conduzido em etapas. Primeiro, sera criada uma base simulada para validar a estrutura do pipeline. Em seguida, os textos serao limpos e normalizados. Depois, serao feitas analises exploratorias com frequencias e visualizacoes simples. Na etapa seguinte, uma amostra podera ser rotulada manualmente em classes de sentimento. Por fim, modelos de classificacao serao treinados e comparados.

## Fontes de Dados

- comentarios publicos coletados por APIs terceiras autorizadas e compativeis com pesquisa academica;
- dados simulados gerados pelo proprio projeto apenas para testes locais do pipeline;
- CSVs externos adicionados manualmente;
- fontes publicas acessiveis sem login ou restricoes, apenas de forma experimental;
- APIs oficiais, caso estejam disponiveis e permitidas.

## Cuidados Eticos

O projeto nao deve coletar ou armazenar dados pessoais identificaveis, como username, ID de usuario, ID de post, URL de perfil, foto de perfil ou localizacao. Tambem nao deve tentar burlar login, captcha, paywall, bloqueios, rate limits ou mecanismos de protecao. Em relacao ao X/Twitter, scraping e automacao fora de canais permitidos podem gerar restricoes ou violar termos de uso; por isso, o fluxo prioritario sera baseado em APIs terceiras autorizadas, API oficial quando aplicavel e arquivos CSV anonimizados.

## Tecnicas de PLN Previstas

- regex para limpeza e normalizacao;
- tokenizacao;
- n-grams;
- frequencia de termos;
- TF-IDF;
- vetorizacao para classificacao;
- embeddings e Transformers em etapa futura.

## Modelos Previstos

- Naive Bayes;
- Regressao Logistica;
- modelos baseados em Transformers para portugues.

## Metricas Previstas

- acuracia;
- precisao;
- revocacao;
- F1-score;
- matriz de confusao;
- comparacao por classe.

## Cronograma Resumido

| Etapa | Descricao |
| --- | --- |
| 1 | Estruturacao do repositorio e geracao de dados simulados |
| 2 | Pre-processamento e exploracao inicial |
| 3 | Rotulagem manual de amostras |
| 4 | Implementacao de TF-IDF e modelos classicos |
| 5 | Avaliacao dos modelos |
| 6 | Comparacao com abordagem moderna |
| 7 | Escrita do relatorio final |
