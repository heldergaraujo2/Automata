# Automata — fonte concreta de mídia: Wikimedia Commons

**Fonte:** https://commons.wikimedia.org/

O módulo `automata/commons_media_source.py` prepara buscas na API
pública MediaWiki por arquivos de imagem e vídeo e normaliza metadados
de licença, atribuição e página de descrição.

A busca está **bloqueada por padrão** (`allow_network=False`) para
respeitar a decisão de adiar testes e conexões reais. Não exige conta
de afiliado. Os resultados são apenas candidatos, não mídias
aprovadas: `authorized_for_reuse=False` e `local_path=""`.

## Revisão obrigatória
- Confirmar licença e suas condições na página do arquivo, inclusive
  uso comercial, atribuição, compartilhamento pela mesma licença e
  restrições de marcas/pessoas quando aplicáveis.
- Verificar se a licença cobre o uso promocional pretendido.
- Só então obter o arquivo por meio permitido, preservar os créditos
  e registrar evidências de licença no catálogo.
- Não confundir arquivo público com autorização irrestrita.
- Não usar conteúdo genérico para simular características do produto.

## Próximo passo
Criar o processo de aprovação de licenças, aquisição autorizada e
verificação do arquivo local; conectar o catálogo à política de
reutilização e ao renderizador. Também poderá ser adicionado um
provedor de banco de vídeos com API oficial, caso suas condições de
uso e credenciais permitam.

Código e testes foram adicionados ao GitHub, sem execução de rede,
download, instalação ou publicação.
