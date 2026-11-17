# Automata — mídias visuais com projetos existentes

## Projetos reutilizáveis

- **ComfyUI** (https://github.com/comfyanonymous/ComfyUI): plataforma
  open source de workflows visuais, execução local e API de fila.
  Pode servir de orquestrador para geração de imagens e, com modelos
  compatíveis, vídeo. A capacidade real depende do workflow, modelo,
  VRAM e licenças.
- **Stable Diffusion WebUI Forge**
  (https://github.com/lllyasviel/stable-diffusion-webui-forge):
  alternativa para geração de imagens locais. Avaliar requisitos e
  compatibilidade antes de escolher.
- **FFmpeg** (https://ffmpeg.org/): já usado no projeto para compor
  vídeos e poderá animar imagens autorizadas com zoom/pan, em vez
  de depender de geração pesada de vídeo por IA.

## Decisão

Priorizar **ComfyUI para imagens originais genéricas** e FFmpeg para
animação e composição. O vídeo do produto deve usar imagens/clipes
oficiais com permissão de uso ou capturas autorizadas e verificadas,
sem inventar aparência, características ou descontos.

O módulo `automata/visual_media_adapter.py` cria planos JSON com
prompts por cena e status `pending_verification`; não conecta à
API do ComfyUI, não baixa modelos e não produz mídia ainda.
A arquitetura deve aceitar mídias de produto fornecidas pelo
operador, enquanto os fundos genéricos podem ser gerados.

## Dependências a validar na fase local

- Windows, GPU e VRAM disponíveis, modelos compatíveis com a licença
  de uso comercial, workflow do ComfyUI, tempo por cena.
- Direitos das imagens de produtos, uso de marca e permissões do
  programa de afiliados.
- Qualidade, consistência, revisão humana e custos computacionais.

## Próximo desenvolvimento

Adaptador opcional para workflow JSON do ComfyUI, com validação
de saídas e bloqueio de publicação sem aprovação. Nenhuma execução
local, conexão ou publicação foi realizada.
