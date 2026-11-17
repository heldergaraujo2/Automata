# Aprovação de licenças e aquisição de mídia — Automata

## Etapa implementada
O módulo `automata/media_acquisition.py` exige uma aprovação
explícita antes de baixar qualquer mídia: página de origem, referência
de licença, atribuição, identidade do revisor e declaração de
autorização para uso comercial.

A aprovação é **declaração humana**, não auditoria jurídica automática.
A licença pode impor condições adicionais (atribuição, alterações,
compartilhamento, direitos de imagem, marca, uso promocional). Essas
condições precisam ser analisadas antes da aprovação.

`acquire_media` está **bloqueado por padrão**. Quando autorizado na
fase final, limita arquivos a 100 MB, exige HTTPS, bloqueia
redirecionamentos, evita endereços de rede não públicos, baixa para
arquivo temporário e calcula SHA-256. O arquivo permanece com status
`downloaded_pending_content_validation`, não é automaticamente
marcado pronto para renderização.

## Limitações e próximas etapas
- A validação de rede é uma defesa parcial; DNS pode mudar entre
  resolução e conexão. Aplicar allowlist de domínios e verificação
  robusta do destino de conexão antes de uso real.
- Ainda falta validar assinatura/magic bytes, codecs, dimensões e
  integridade audiovisual, além de armazenamento de provas de licença.
- Falta ligar arquivos validados ao catálogo reutilizável e inserir
  créditos na publicação.
- A fonte já preparada no repositório é **Wikimedia Commons**, não
  Pexels. Pexels poderá ser integrado separadamente se houver API e
  autorização compatível com uso promocional.

Nenhuma busca, download, teste local ou publicação foi executada.
