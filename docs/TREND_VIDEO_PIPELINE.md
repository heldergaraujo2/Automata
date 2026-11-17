# Tendência → roteiro → plano de vídeo

Fluxo implementado:
1. `automata.trend_strategy_cli` gera decisões de repost licenciado ou conteúdo original.
2. `automata.trend_scripts_cli` converte decisões em planos estruturados de vídeo.
3. Para repost autorizado, o plano mantém o endereço da mídia e créditos, com status de verificação pendente.
4. Para conteúdo próprio, o plano contém título, narração e cenas genéricas de roteiro, sem reutilizar vídeo ou áudio de terceiros.

Comando futuro:
```powershell
python -m automata.trend_scripts_cli --decisions output/trend_decisions.json
```

**Limitações:** ainda não há geração de vídeo final, locução, pesquisa de fatos
da tendência, personalização por IA, montagem FFmpeg desse novo fluxo,
verificação externa de licença, agendamento ou publicação. Os planos são
rascunhos para revisão; nenhum teste foi executado nesta etapa.
