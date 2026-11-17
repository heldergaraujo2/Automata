# Compositor de vídeos

Requisitos: Python 3.11+ e FFmpeg/ffprobe no PATH.

Exemplo:

```powershell
python media/compose_split.py --viral "C:\videos\viral.mp4" --product "C:\videos\produto.mp4" --output "C:\videos\final.mp4"
```

O vídeo viral aparece em cima e o produto embaixo. Ambos começam em t=0 e tocam simultaneamente. Resolução de saída 1080×1920; duração até 60 segundos. Usa áudio do vídeo do produto quando disponível. Os vídeos devem ter durações próximas (tolerância 0,5 s), sem cortes automáticos.

**Limitações iniciais:** corte central para preencher cada metade pode esconder detalhes; arquivos com rotação/metadados incomuns precisam de teste; não há inspeção de direitos de uso automatizada. Não publicar sem confirmar licenças e revisar o MP4.
