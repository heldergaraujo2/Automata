# Automata — campanhas de afiliados → vídeos → fila

O fluxo de código agora conecta:
1. Descoberta e validação offline de produtos.
2. Geração de rascunhos de campanhas para redes sociais.
3. Preparação de briefings de vídeos promocionais.
4. Renderização FFmpeg de dois vídeos locais autorizados, em formato
   1080×1920 (tendência em cima, produto embaixo), até 60 segundos.
5. Inclusão do MP4 na fila `pending_review`, sem agendamento ou publicação
   automática antes da aprovação.

`automata.affiliate_video_pipeline.export_briefs` converte campanhas
em briefings; `render_and_queue` chama o compositor e gera rascunho.

**Limites atuais:** não gera mídia a partir do texto; precisa receber os
dois clipes já prontos e com direitos verificados. Não busca produtos,
não cria links oficiais, não conecta contas, não hospeda vídeos, não publica
em redes e não acompanha vendas reais. Os testes foram escritos, mas não
executados, conforme combinado.
