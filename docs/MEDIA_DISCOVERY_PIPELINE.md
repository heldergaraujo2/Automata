# Automata — descoberta de mídia, reutilização primeiro

A nova ponte `automata/media_discovery.py` recebe candidatos de
vídeos/imagens descobertos por futuros provedores autorizados,
normaliza os metadados, rejeita itens sem permissão confirmada
e passa mídias aprovadas para a política `media_reuse_policy`.

## Contrato de entrada
Cada candidato informa `asset_id`, `scene_key`, `kind` (video/image),
`source_url`, `provider`, `license_reference`,
`authorized_for_reuse`, `local_path` e opcional `product_id`.

A autorização é uma declaração fornecida pela fonte/operador e
**não é uma verificação jurídica automática**. O caminho local é
declarado, mas a existência e integridade do arquivo ainda precisam
ser validadas antes de renderizar.

## Ordem
1. Preferir vídeo licenciado já disponível.
2. Preferir imagem licenciada se não houver vídeo.
3. Para produtos, exigir mídia real autorizada e do produto correto.
4. Para cenas genéricas sem mídia aprovada, solicitar geração
   somente quando explicitamente permitida.
5. Caso contrário, manter pendência de material.

## Limites desta etapa
Ainda **não** há busca online executável, download automático,
integração de API de banco de vídeos, comprovação independente de
licenças ou conexão com contas. O módulo conecta **resultados
estruturados de descoberta** ao decisor de reutilização; uma API
de busca real e seu contrato/licenciamento serão implementados
separadamente. Não confundir um link público com autorização de
republicação. Nenhum teste foi executado.
