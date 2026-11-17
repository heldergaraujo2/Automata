# Magalu/Pichau → redes sociais e marketplaces

O Automata passa a distinguir **divulgação afiliada** de **anúncio como vendedor**.

- Afiliados: produto com link de comissão pode gerar rascunho para redes
  sociais, com identificação publicitária. Não presume que esse link seja
  aceito como anúncio de loja no TikTok Shop ou Mercado Livre.
- Marketplace: publicação como vendedor requer autorização comercial,
  disponibilidade de estoque, entrega e conformidade com a plataforma.
- Descrições: somente título, descrição, preço de referência e características
  fornecidos como dados verificados. Não inventar desconto, estoque,
  avaliação, prazo de entrega ou garantia.
- Imagens: o campo `image_rights_verified` permite registrar a verificação,
  mas ainda não existe fluxo de download ou publicação de fotos.
- Cada destino recebe status: `pending_review`, `blocked` ou
  `needs_channel_policy_check`. Nenhum status publica automaticamente.

Implementado apenas o modelo de dados, roteamento, geração determinística
de rascunhos e testes escritos. **Não** foram integrados catálogos reais,
APIs Magalu/Pichau, Mercado Livre ou TikTok Shop, autenticação, preços em
tempo real, estoque ou vendas. Testes ainda não executados. Conexões reais
ficam para a etapa final no PC, conforme combinado.
