# Instagram, Facebook e TikTok — integração oficial

Os três provedores possuem agora um contrato comum para conta, vídeo e legenda.
O código **não realiza chamadas de publicação** e não autentica contas. Isso evita
simular uma integração que ainda não foi autorizada.

## Instagram
Planejar publicação de Reels via Instagram Graph API, conforme elegibilidade
da conta profissional, permissões, app Meta aprovado e mídia hospedada em URL
acessível pela plataforma. Confirmar endpoints e versão no momento da integração.

## Facebook
Planejar publicação de vídeo/Reels em Página por Graph API com permissões de
Página e token válido. Não presumir permissão para perfis pessoais.

## TikTok
Planejar uso de Content Posting API, sujeito a autorização OAuth, revisão do app,
escopos, restrições de publicação e requisitos de upload.

## Preparação necessária
1. IDs de contas autorizadas e aplicativo de desenvolvedor correspondente.
2. Tokens mantidos apenas em variáveis de ambiente ou cofre de segredos.
3. URLs de mídia acessíveis e direitos de reutilização documentados.
4. Aprovação de conteúdo, divulgação de publicidade e confirmação de regras de afiliados.
5. Testes em ambiente autorizado e observabilidade antes de ativar publicações.

A configuração de exemplo deixa todas as contas desabilitadas. Nunca gravar tokens no GitHub.
