# Autenticação social — fundação segura

Foi criado um gerador de solicitações OAuth com `state` aleatório e PKCE S256,
e um validador de retorno de `state`. Nenhum token é emitido, trocado,
armazenado ou publicado por esta implementação.

**Importante:** Meta e TikTok têm diferenças de OAuth, escopos, endpoints e
suporte a PKCE. O gerador genérico é uma fundação, não uma implementação pronta
para usar em qualquer plataforma. Antes de habilitar, criar adaptadores
específicos, confirmar documentação atual e requisitos de cada provedor.

Instagram: confirmar modalidade de Instagram API e conta profissional elegível.
Facebook: configurar aplicativo Meta, permissões de Página e revisão quando aplicável.
TikTok: configurar aplicativo TikTok for Developers, Login Kit/Content Posting API,
escopos aprovados, redirecionamento e revisão aplicável.

Para conexão real serão necessários aplicativos registrados, client IDs,
redirect URIs autorizadas, consentimento do titular, troca de códigos com
proteção CSRF, armazenamento seguro/renovação/revogação de tokens e testes.
Nunca colocar client secrets, access tokens ou refresh tokens no GitHub.
