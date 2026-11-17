# Automata — integração preparada com ComfyUI

ComfyUI: https://github.com/comfyanonymous/ComfyUI

O adaptador `automata/comfyui_adapter.py` aceita um workflow exportado
do ComfyUI em **API format JSON**, altera o texto de um nó
`CLIPTextEncode` escolhido e prepara submissão à rota local
`POST /prompt`. Por padrão, a submissão é bloqueada e não há
nenhuma conexão ou geração real.

## Restrições
- Endpoint somente HTTP localhost/127.0.0.1 com porta explícita.
- Workflow deve ter nós com `class_type` e `inputs`.
- O ID do nó de prompt precisa ser configurado para o workflow real.
- A resposta `prompt_id` indica fila, **não geração concluída**.
- O adaptador não baixa modelos, não acompanha `/history`, não
  recupera imagens nem verifica direitos ou qualidade.
- Não enviar dados sensíveis nos prompts. Usar apenas fundos
  genéricos; fotos do produto devem vir de fonte autorizada.
- Verificar licença do ComfyUI, de cada modelo e dos ativos para
  uso comercial antes da execução.
- O acesso local só será habilitado na etapa final de testes no PC.

## Próximas etapas
Implementar polling de histórico e validação de saída, conversão
de imagens em cenas animadas com FFmpeg, e conexão entre storyboard,
Piper, ComfyUI e fila de revisão. A compatibilidade Windows + GPU AMD
RX 6600 permanece não validada.
