# Estratégia de tendências — duas rotas

Decisão acordada:
- Com direitos de reutilização efetivamente verificados, aprovação e mídia autorizada: preparar repost do original com crédito ao criador.
- Sem direitos confirmados: preservar a tendência como referência e produzir **briefing de conteúdo novo e original**, sem copiar vídeo ou áudio de terceiros.

O comando `python -m automata.trend_strategy_cli --feed input/viral_feed.json`
gera `output/trend_decisions.json` com uma decisão por URL única.

Para habilitar uma rota de repost, fornecer listas JSON de URLs verificadas
(`--verified-rights`) e aprovadas (`--approved-reposts`). Essas listas são
registros declaratórios: a verificação da autenticidade das licenças ainda
precisa ser implementada.

O código **não gera o vídeo original**, não consulta TikTok em tempo real,
não baixa mídia e não publica em redes. Os briefings aguardam um gerador
de roteiros/mídia e revisão de originalidade antes de integração ao agendador.
Não há testes executados confirmados.
