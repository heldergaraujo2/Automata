# Automata — relatórios de comissões (sem contas)

Módulo offline de importação de CSV, pensado para receber futuramente
exportações autorizadas de programas de afiliados. Não exige criar contas
agora, não usa APIs e não gera pagamentos.

## Formato interno do CSV
Colunas obrigatórias:
`program,transaction_id,product_id,campaign_tag,status,sale_amount_brl,commission_amount_brl,occurred_at`.

Status: `pending` (pendente), `approved` (aprovada),
`paid` (paga), `cancelled` (cancelada), `refunded` (devolvida).

Os valores são BRL com ponto decimal, como `12.50`. O importador
valida valores, recusa transações duplicadas e gera JSON com totais
por status. **Só soma `paid` como valor pago**; aprovado e pendente
não são dinheiro recebido. Os valores do CSV são declarações da fonte,
não são independentemente verificados.

## Exemplo de uso futuro no PC
```powershell
python -m automata.affiliate_commissions_cli --input input/commissions.csv --output output/affiliate_commissions.json
```

O CSV de exemplo para desenvolvimento é fictício; nunca representa
ganhos reais. Layouts oficiais do Mercado Livre e de outros parceiros
podem exigir adaptadores específicos quando houver acesso autorizado.

## Próximos passos
- Adaptadores para layouts reais de relatórios, conforme documentação e
  exportações disponíveis.
- Histórico de atualizações de status, conciliação sem contagem dupla.
- Indicadores por campanha, canal e produto; dashboard.
- Posteriormente, integração autorizada com contas e testes finais no PC.

Não há conexões, publicações ou testes executados nesta etapa.
