# Automata — preparação automática de roteiros de vídeos

Esta etapa cria storyboards estruturados a partir de campanhas afiliadas,
com quatro cenas, textos de narração, orientação visual e direitos de mídia
exigidos. Padrão: vídeo vertical 1080×1920, tela dividida, 40 segundos,
com limite geral de até 60 segundos.

A parte superior deve conter vídeo original de tendência ou material
licenciado; a parte inferior mostra o produto com mídia autorizada.
O roteiro não afirma descontos, benefícios ou especificações não
verificadas e inclui identificação publicitária.

Entrada: `output/affiliate_campaigns.json`. Saída:
`output/affiliate_storyboards.json`.

Uso futuro no computador:
```powershell
python -m automata.affiliate_video_storyboard_cli --input output/affiliate_campaigns.json --output output/affiliate_storyboards.json
```

**Importante:** esta implementação produz roteiro e texto de narração,
não gera voz sintetizada, clipes ou MP4 por si só. A montagem FFmpeg
existente depende de duas mídias locais com direitos confirmados.
Nenhuma conta foi conectada, nenhum vídeo foi publicado e os testes
foram escritos, mas não executados.

Próximas etapas: adaptador de TTS local, preparação de cenas com
recursos originais/licenciados, sincronização de áudio/legendas,
orquestração da renderização e validação do vídeo final.
