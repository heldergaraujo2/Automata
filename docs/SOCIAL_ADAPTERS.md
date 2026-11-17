# Adaptadores de publicação por plataforma

Interfaces criadas: InstagramAdapter, FacebookAdapter e TikTokAdapter.
Todas verificam plataforma, conta habilitada, aprovação, aviso de afiliado,
direitos declarados e URL HTTPS da mídia antes de preparar a operação.

**Nenhuma delas publica ainda.** O método publish lança NotImplementedError
intencionalmente, para não simular postagem real nem improvisar endpoints.

Próximos passos por provedor:
- Instagram: container de mídia, checagem de processamento, publicação de Reels,
  consulta de status, credenciais e permissões aprovadas.
- Facebook: upload e publicação de Reels em Página, status, token de Página.
- TikTok: inicialização de publicação/upload, transferência, consulta de status,
  auditoria do aplicativo e autorização de escopos.

Não confundir teste de preparação com teste de integração real. Tokens e
client secrets não devem entrar no repositório.
