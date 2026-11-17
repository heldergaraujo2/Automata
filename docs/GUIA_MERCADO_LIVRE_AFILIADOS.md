# Automata — guia de uso do Mercado Livre Afiliados

## 1. Objetivo

O Automata é um **divulgador afiliado**, não um vendedor no Mercado Livre.
A pessoa compra na loja ou anúncio de terceiros, e o programa de afiliados
pode pagar comissão por compras qualificadas conforme seus termos.
O Automata não recebe pedidos, não administra estoque e não promete vendas.

## 2. O que já está preparado no GitHub

- Modelo de produto com título, descrição, preço e URL de indicação.
- Geração de rascunhos publicitários para TikTok, Instagram e Facebook.
- Identificação de publicidade e link de afiliado.
- Registro de fonte e data das informações fornecidas.
- Preparação de até três rascunhos por produto, sem publicação automática.
- Separação entre vídeos de tendência autorizados e conteúdo original.

**Estado real:** os módulos estão escritos, mas não foram testados; não há
acesso ao Mercado Livre, integração com catálogo, criação de links de afiliado
por API, acompanhamento de vendas, publicação real ou conexão de contas.

## 3. Como será o uso no teste real, no PC

1. Entrar na sua conta do Mercado Livre e confirmar participação e elegibilidade
   no programa de afiliados, seus termos, canais permitidos e forma de gerar links.
2. Gerar ou obter um link de afiliado **pelo mecanismo oficial autorizado**.
   Não basta copiar a URL comum do produto.
3. Conferir preço, características e disponibilidade no anúncio original.
4. Registrar os dados verificados no formato de entrada (exemplo abaixo).
5. O Automata prepara legendas para redes sociais e coloca os rascunhos
   em revisão; não cria anúncios de vendedor.
6. Depois da revisão e das conexões oficiais, habilitar gradualmente
   a publicação e acompanhar cliques/comissões pelos relatórios disponíveis.
7. Atualizar ou retirar conteúdo se o preço, estoque ou regras mudarem.

## 4. Exemplo de entrada para o programa

Salvar como `input/mercado_livre_products.json`:

```json
[
  {
    "item_id": "MLB-EXEMPLO",
    "title": "Produto demonstrativo",
    "description": "Descrição confirmada no anúncio original",
    "price_brl": 199.0,
    "product_url": "https://exemplo.com/produto",
    "affiliate_url": "https://exemplo.com/link-de-afiliado",
    "evidence_source": "Anúncio original conferido pelo operador",
    "checked_at": "2026-11-17T12:00:00-03:00"
  }
]
```

Os links acima são ilustrativos, **não** são links reais de afiliado.

Quando chegar a fase de testes no computador, executar:

```powershell
python -m automata.mercado_livre_affiliates_cli --input input/mercado_livre_products.json --output output/mercado_livre_campaigns.json
```

O arquivo de saída conterá três rascunhos por produto. Isso não faz
publicações nem gera comissões por si só.

## 5. Como ganhar comissão — e limites

A comissão depende de elegibilidade, categoria, atribuição de compra,
eventuais cancelamentos e regras vigentes do programa. O Automata não deve
inventar percentuais ou garantir conversões. Taxas só entram em projeções
quando forem confirmadas pelo programa.

É necessário conferir se a divulgação em cada canal e o uso de imagens,
marcas e materiais são autorizados. O TikTok Shop pode operar sob regras
diferentes do TikTok como rede social; não presumir integração automática.

## 6. Próximas implementações

- Confirmar documentação oficial e acesso técnico autorizado do programa.
- Criar importador seguro de produtos e links oficiais, com atualização de preços.
- Integrar checagens de validade dos dados, deduplicação e histórico.
- Ligar campanhas ao gerador de vídeos e à fila de revisão/agendamento.
- Conectar contas somente na etapa final de testes reais no PC.
- Validar permissões, métricas e atribuição de comissões.

**Regra permanente:** nenhuma senha, token ou cookie de conta deve ser
enviado ao GitHub. Não habilitar publicações reais sem autorização.
