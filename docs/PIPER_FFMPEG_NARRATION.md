# Piper + FFmpeg — integração de narração local

O Automata já tem adaptador para o Piper gerar WAV de um roteiro
(`automata/local_narration.py`). Agora o adaptador
`automata/narrated_video_render.py` adiciona a narração ao vídeo
vertical existente e pode gravar legendas SRT no vídeo.

## Fluxo previsto
1. Gerar storyboard com texto de narração.
2. Preparar texto e SRT por cena.
3. Sintetizar WAV usando Piper instalado localmente e uma voz pt_BR
   licenciada para o uso pretendido.
4. Montar o vídeo dividido com clipes originais/licenciados.
5. Verificar que a duração do WAV cabe no vídeo.
6. Renderizar MP4 com narração e legendas, sem publicar.

**Limitações:** SRT é temporizado por cena e não sincronizado com
as palavras efetivamente faladas. A narração substitui o áudio
anterior do vídeo. A renderização requer FFmpeg com suporte ao filtro
subtitles/libass e arquivos de mídia reais. Vozes, modelos e
licenças não foram baixados nem validados. Os métodos de execução
estão bloqueados por padrão e dependem de autorização explícita
na fase final de testes locais.

## Próximas melhorias
- Medir áudio por cena e alinhar legendas por fala.
- Controlar volume/mixagem de áudio de fundo.
- Gerar mídias visuais originais automaticamente.
- Validar vídeo final e enviar para revisão antes do agendamento.

Nenhuma conta conectada, nenhuma publicação ou teste executado.
