# Descoberta → campanhas de afiliados

O Automata agora possui uma ponte offline entre a fila de produtos
(`affiliate_discovery`) e a criação de campanhas
(`affiliate_campaign_pipeline`).

Para cada produto único com campos preenchidos, prepara três rascunhos
de divulgação: TikTok, Instagram e Facebook. Cada rascunho contém
título, descrição, preço de referência, link de afiliado fornecido,
fonte da informação e data declarada de conferência. Os rascunhos
permanecem `pending_review`.

Produtos sem link de afiliado, descrição, preço ou evidências são
ignorados na exportação de campanhas e contabilizados como bloqueados.
O módulo recalcula os critérios mesmo se o arquivo de entrada disser
que o produto está pronto.

## Uso futuro no PC

```powershell
python -m automata.affiliate_discovery_cli --input input/affiliate_leads.json
python -m automata.affiliate_campaign_pipeline_cli --input output/affiliate_leads.json --output output/affiliate_campaigns.json
```

**Limites:** não pesquisa produtos na internet, não confirma a autenticidade
do link, não verifica preço em tempo real, não gera vídeo, não envia os
rascunhos automaticamente à fila de publicação e não chama APIs sociais.
Os testes foram adicionados mas ainda não executados. A integração
real com contas continua reservada para a fase final no computador.
