# Produção vertical de tendências

Foi implementada a ponte entre os planos de vídeo de tendências e o compositor
FFmpeg já existente no repositório. Com dois vídeos locais fornecidos e direitos
de ambos verificados, produz um MP4 vertical 1080×1920: tendência em cima,
demonstração do produto embaixo, reprodução simultânea e duração máxima 60s.

O compositor atual exige durações próximas (diferença máxima 0,5s) e pode
encurtar o vídeo mais longo até a duração do menor. O áudio é priorizado do
vídeo do produto. Não há geração automática dos clipes originais ou voz.

Comando futuro (requer FFmpeg e um arquivo JSON de plano individual):
```powershell
python -m automata.trend_production_cli --plan input/plan.json --top input/top.mp4 --product input/product.mp4 --top-rights-verified --product-rights-verified --output output/final.mp4
```

As flags de direitos são declarações do operador, não verificação jurídica
automática. O vídeo gerado **não entra automaticamente no agendador**; falta
validação técnica, revisão, aprovação e integração com a fila. Nenhum teste
foi executado nesta etapa e nenhuma publicação real foi realizada.
