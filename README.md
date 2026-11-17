# Automata — Operação autônoma de afiliados de tecnologia

Projeto modular para pesquisar ofertas de tecnologia, selecionar mídias com licença comercial, compor vídeos verticais em tela dividida, preparar publicações e medir comissões. **Estado: fundação/MVP; nenhuma conta conectada, nenhuma publicação ou venda automatizada.**

## Objetivo
Meta inicial: R$ 1.000/mês de **lucro líquido**, sem promessa de retorno. Canais iniciais: Instagram; expansão condicionada às políticas de Facebook, TikTok e marketplaces. A IA opera localmente em Windows (Ryzen 5 7600X3D, 32 GB RAM, RX 6600 8 GB), com automações agendadas 24/7.

## Regra editorial fixa
- Vídeo viral autorizado **em cima**, demonstração autorizada do produto **embaixo**.
- Ambos iniciam juntos e rodam simultaneamente; duração final de até **60 segundos**, formato **1080×1920, 9:16**.
- Não cortar automaticamente conteúdo integral. Se durações forem incompatíveis, sinalizar para seleção de outro par ou aprovação de sincronização.
- Nunca presumir que vídeo público permite reutilização comercial. Guardar licença, origem e autorização de cada mídia.
- Anúncios e legendas devem identificar relações de afiliado; não inventar preços, descontos ou avaliações.

## Arquitetura proposta
1. `research`: pesquisa de tendências, produtos, preços e fontes autorizadas.
2. `rights`: validação de licenças, termos e comprovação de direitos.
3. `media`: composição determinística com FFmpeg/ffprobe.
4. `content`: legendas, descrições e revisão factual.
5. `publishing`: fila e APIs oficiais de redes sociais.
6. `analytics`: cliques, comissões pendentes/aprovadas, despesas e lucro.
7. `orchestration`: agendamento, retries, auditoria e aprovação de gastos.
8. `models`: Ollama local, sem dependência obrigatória de geração de vídeo.

## Componentes candidatos (não auditados/instalados)
- Ollama: https://github.com/ollama/ollama
- FFmpeg: https://github.com/FFmpeg/FFmpeg
- n8n: https://github.com/n8n-io/n8n (licença não é open source tradicional)
- Activepieces: https://github.com/activepieces/activepieces
- Postiz: https://github.com/gitroomhq/postiz-app
- changedetection.io: https://github.com/dgtlmoon/changedetection.io
- Chatwoot: https://github.com/chatwoot/chatwoot

Não incorporar código de terceiros antes de validar licença, segurança e manutenção. Preferir integração por APIs e contêineres separados a copiar código.

## Segurança e operação
- Tokens somente em variáveis de ambiente; nunca no Git.
- Aprovação humana para gastos, novas campanhas e alterações sensíveis.
- Respeitar APIs oficiais, limites de publicação e políticas de afiliados.
- Logs de auditoria, backups e reinício automático; nenhum acesso irrestrito ao Windows.
- Começar com publicações em modo rascunho até testes e permissões serem confirmados.

## Primeira entrega
Ferramenta local para juntar **dois vídeos autorizados** com FFmpeg e gerar um MP4 de até 60 s; validar resolução, duração, áudio e resultado antes de publicar. Ver `docs/ROADMAP.md`.
