# Dicionario de Dados

Este documento descreve o modelo de dados previsto para a pipeline contextual.
Os arquivos abaixo ainda representam estrutura planejada para a proxima etapa.

## `official_posts.csv`

Publicacoes oficiais do clube piloto.

| Campo | Tipo sugerido | Descricao |
| --- | --- | --- |
| `post_id` | string | ID operacional da publicacao oficial no X, necessario para buscar replies e quotes. |
| `post_id_hash` | string | Hash estavel do ID da publicacao oficial. |
| `conversation_id` | string | ID da conversa associada ao post oficial. |
| `club` | string | Nome do clube piloto. |
| `club_username` | string | Arroba oficial do clube. |
| `official_text` | string | Texto da publicacao oficial. |
| `created_at` | datetime | Data e hora de publicacao. |
| `lang` | string | Idioma detectado. |
| `like_count` | integer | Numero de curtidas. |
| `reply_count` | integer | Numero de replies. |
| `retweet_count` | integer | Numero de retweets. |
| `quote_count` | integer | Numero de quote tweets. |
| `collected_at` | datetime | Data e hora da coleta. |
| `post_type_llm` | string | Tipo de post sugerido por modelo pronto. |
| `post_type_manual` | string | Tipo de post validado ou corrigido manualmente. |
| `post_topic_llm` | string | Assunto/editoria do post sugerido por regra ou modelo. |
| `post_topic_manual` | string | Assunto/editoria do post validado ou corrigido manualmente. |

## `post_reactions.csv`

Replies e quote tweets associados a publicacoes oficiais.

| Campo | Tipo sugerido | Descricao |
| --- | --- | --- |
| `reaction_id` | string | Identificador anonimizado da reacao. |
| `source_reaction_id_hash` | string | Hash estavel do ID original da reacao. |
| `parent_post_id` | string | Identificador da publicacao oficial relacionada. |
| `club` | string | Clube piloto associado. |
| `reaction_type` | string | Tipo de reacao: `REPLY` ou `QUOTE`. |
| `author_id_hash` | string | Hash estavel do autor da reacao. |
| `text` | string | Texto bruto da reacao. |
| `created_at` | datetime | Data e hora da reacao. |
| `lang` | string | Idioma detectado. |
| `like_count` | integer | Numero de curtidas. |
| `reply_count` | integer | Numero de replies da reacao. |
| `retweet_count` | integer | Numero de retweets da reacao. |
| `quote_count` | integer | Numero de quotes da reacao. |
| `collected_at` | datetime | Data e hora da coleta. |
| `clean_text` | string | Texto limpo para PLN. |

## `annotated_reactions.csv`

Base anotada para analise semantica e treinamento futuro.

| Campo | Tipo sugerido | Descricao |
| --- | --- | --- |
| `reaction_id` | string | Identificador da reacao anotada. |
| `parent_post_id` | string | Publicacao oficial relacionada. |
| `club` | string | Clube piloto associado. |
| `official_post_type` | string | Tipo manual ou sugerido da publicacao oficial associada a reacao. |
| `official_post_topic` | string | Assunto/editoria manual ou sugerido da publicacao oficial associada a reacao. |
| `reaction_type` | string | `REPLY` ou `QUOTE`. |
| `clean_text` | string | Texto limpo da reacao. |
| `relevancia` | string | Nivel de relevancia da reacao. |
| `tema` | string | Tema principal da reacao. |
| `emocao` | string | Emocao predominante. |
| `polaridade` | string | Polaridade geral. |
| `intencao` | string | Intencao comunicativa principal. |
| `confianca_modelo` | float | Confianca atribuida pelo anotador automatico. |
| `justificativa_curta` | string | Breve justificativa do rotulo. |
| `validado_manual` | boolean | Indica se houve validacao humana. |
| `rotulo_corrigido` | string | Campo livre para correcao manual quando necessaria. |

## Observacoes

- IDs brutos de usuarios nao devem ser publicados sem avaliacao etica.
- O `post_id` de publicacoes oficiais do clube e mantido como campo operacional
  para permitir a busca de replies e quote tweets.
- IDs de autores e de reacoes de torcedores devem ser anonimizados por hash.
- Retweets puros devem ser mantidos como metrica, nao como texto de PLN.
- Campos de texto devem preservar conteudo suficiente para interpretacao
  contextual.
