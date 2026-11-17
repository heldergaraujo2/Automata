# Automata — política de reaproveitamento de mídia

**Regra principal:** usar vídeos e imagens existentes e autorizados;
geração por IA somente quando não houver mídia adequada.

## Ordem de decisão
1. Buscar no catálogo de mídia local um vídeo aprovado, adequado à cena.
2. Se não houver vídeo, buscar imagem aprovada e adequada.
3. Para cenas de produto, exigir material real e autorizado do produto
   correto. Nunca gerar uma imagem que finja representar o produto.
4. Para cenas genéricas, se não houver mídia aprovada e a geração
   estiver explicitamente permitida, solicitar geração pelo ComfyUI.
5. Caso contrário, marcar a cena como pendente de material.

O módulo `automata/media_reuse_policy.py` implementa essa decisão
a partir de um manifesto de mídias fornecido ao sistema. Não faz
busca na internet, download, análise semântica, geração nem execução.
A integração com a descoberta de mídias externas autorizadas e
com a fila ComfyUI ainda precisa ser construída.

**Direitos autorais:** encontrar um vídeo publicamente não significa
ter permissão para reutilizá-lo. Exigir licença, autorização ou outra
base válida; créditos por si só não substituem permissão. Respeitar
regras das plataformas e programas de afiliados.

**Custo:** evitar renderizações e geração desnecessárias; preferir
reutilização e adaptar a montagem com FFmpeg.

**Status:** código e testes adicionados ao GitHub, testes não
executados, sem conexões a contas ou publicações.
