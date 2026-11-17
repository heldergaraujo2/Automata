# Descoberta e validação de produtos afiliados

Nova etapa: importação de registros de produtos obtidos de fontes
autorizadas, classificação de informações faltantes e deduplicação.
Mercado Livre é a prioridade; Magalu, Pichau e TikTok Shop são possíveis
fontes futuras, conforme disponibilidade e regras de cada programa.

O sistema separa:
- `ready_for_draft`: URL original, link de afiliado, descrição, preço,
  fonte e data informados.
- `needs_verification`: algum dado obrigatório ausente ou inválido.

Exemplo de entrada em `input/affiliate_leads.json`:
```json
[
  {
    "program": "mercado_livre",
    "product_id": "EXEMPLO",
    "title": "Produto ilustrativo",
    "product_url": "https://example.org/produto",
    "affiliate_url": "",
    "verified_description": "",
    "price_brl": null,
    "evidence_source": "",
    "checked_at": ""
  }
]
```

Comando para quando chegarem os testes locais:
```powershell
python -m automata.affiliate_discovery_cli --input input/affiliate_leads.json
```

**Limitações importantes:** `ready_for_draft` significa apenas que os
campos foram preenchidos, não que o programa confirmou o link ou que
os dados foram verificados independentemente. Não há busca automática
em tempo real, scraping, geração oficial de links, acesso a contas,
publicação ou testes executados. A ligação dos registros aprovados
ao gerador de campanhas é o próximo passo. As conexões reais só
ocorrerão na etapa final no computador do usuário.
