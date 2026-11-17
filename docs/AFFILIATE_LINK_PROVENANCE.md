# Prioridade: origem e validação de links de afiliados

Um vídeo sem um link de comissão válido pode gerar visualizações, mas não
necessariamente receita atribuída. Por isso a próxima dependência crítica
é registrar a origem dos links antes de automatizar mídia em escala.

Novo módulo `automata.affiliate_link_registry`:
- recebe uma lista offline de produtos e evidências de links;
- associa por programa + ID do produto;
- exige URL HTTPS e referência de origem;
- só aplica o link quando `confirmed_by_operator` é verdadeiro;
- registra `verification_level=operator_attested`, sem alegar
  verificação independente pelo programa;
- impede sobrescrever links divergentes silenciosamente.

O resultado pode alimentar `affiliate_discovery` e, em seguida,
`affiliate_campaign_pipeline`. Os campos extras de proveniência
não devem ser tratados como validação externa.

**Pendente:** confirmar meios oficiais de geração e atribuição de links,
permissões de API e regras do Mercado Livre; importar catálogos reais,
validar preço e disponibilidade, conectar contas apenas na fase final
no PC. Não houve teste executado nem acesso a contas.
