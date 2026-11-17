# Automata — pendências antes da operação real

## Implementado em código, ainda sem validação por execução
- Estruturas de ofertas, catálogo e conteúdo de afiliados.
- Importação offline de produtos e links; deduplicação e bloqueios de dados.
- Campanhas de redes sociais com transparência publicitária.
- Roteiros/briefings para vídeos, separação entre tendências autorizadas e
  conteúdo original.
- Ponte para FFmpeg vertical 1080×1920, até 60 segundos, e fila de revisão.
- Agendamento local e preparação em dry-run de postagens sociais.
- Contratos iniciais de hospedagem e conectores, sem publicar.

## Principais faltas, em ordem sugerida
1. **Descoberta real e autorizada de produtos:** verificar fontes e APIs
   permitidas para Mercado Livre, Magalu, Pichau e TikTok Shop; sincronizar
   preços, estoque, dados e disponibilidade sem inventar fatos.
2. **Links de afiliado:** integração permitida com os programas, verificação
   de elegibilidade e atribuição; nunca substituir link comum por suposto
   link afiliado.
3. **Produção automática de mídia:** gerar cenas e narração originais,
   selecionar material licenciado, validar originalidade e direitos,
   criar vídeos finais sem intervenção manual.
4. **Orquestração robusta:** unir descoberta, campanhas, produção, fila e
   publicação com persistência, retries, idempotência, limites e logs.
5. **APIs sociais e hospedagem:** implementar upload autorizado, OAuth,
   status, aprovação, erros e limites para TikTok, Instagram e Facebook.
6. **Métricas reais:** importar cliques, conversões, comissões confirmadas,
   custos e ROI; dashboard e otimização baseados em dados verificáveis.
7. **Segurança e conformidade:** armazenamento seguro de tokens, política
   de conteúdo, privacidade, identificação de publicidade, direitos de mídia.
8. **Testes:** CI e testes locais completos, testes de integração e,
   apenas ao final no PC do usuário, conexão de contas e publicação controlada.

## Regra acordada
Não conectar contas, não publicar, não usar credenciais reais nem executar
testes no PC do usuário até a fase final de validação. A existência de
arquivos de testes no GitHub não comprova que foram executados ou passaram.

## Guia operacional
Consultar `docs/GUIA_MERCADO_LIVRE_AFILIADOS.md` para a preparação
do Mercado Livre Afiliados no teste real.
