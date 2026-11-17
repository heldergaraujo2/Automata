# Automata — catálogo de mídias autorizadas

A ponte `automata/media_catalog_bridge.py` recebe registros
estruturados de mídias adquiridas e **declaradas como inspecionadas**,
exige evidências de origem/licença/atribuição, SHA-256 e revisão humana,
e os converte em candidatos ao catálogo de reutilização.

O planejador consulta o catálogo e prefere vídeo existente, depois
imagem existente; solicita ComfyUI apenas para cena genérica sem
mídia aprovada e com geração explicitamente permitida. Para produto,
exige mídia real do produto correto.

## Limites e segurança
- `content_verified` e `approved_for_commercial_use` são
  **declarações**, não verificação independente do arquivo ou licença.
- O módulo não abre arquivos, não calcula hash real, não confere
  codecs/duração nem executa downloads. A saída é marcada
  `planning_only_files_not_verified`.
- Antes de renderizar, a fase de execução deverá verificar existência,
  hash SHA-256, tipo real, dimensões, codecs, duração e permissões.
- Registrar créditos e obrigações específicas da licença na
  publicação; nem toda licença é adequada a publicidade.
- Não há geração, conexão a contas, testes reais ou publicação.

## Próximo passo
Adicionar verificador local de arquivos com FFprobe e SHA-256,
com execução bloqueada até a fase final; integrar o resultado à
montagem de vídeos e à fila de revisão.
