# Mercado Livre Afiliados — levantamento oficial (17/11/2026)

## Confirmações nas páginas do próprio Mercado Livre

1. A Central de Afiliados e Criadores oferece seleção de produtos, geração
   de links, etiquetas, listas e métricas/receitas.
   https://www.mercadolivre.com.br/l/visite-o-portal-de-afiliados
2. O Gerador de Links do Portal funciona no computador; a Barra de Afiliados,
   depois de ativada, permite gerar links também pelo celular.
   https://www.mercadolivre.com.br/l/afiliados-gere-seus-links
3. Etiquetas permitem agrupar e analisar links. Sua criação é feita no
   computador, com até 30 caracteres alfanuméricos, sem espaços.
   Os links não são salvos automaticamente pelo programa.
   https://www.mercadolivre.com.br/l/organize-seus-links
4. A Central disponibiliza métricas e receitas. A receita de uma venda
   depende de recebimento do produto e ausência de cancelamento/devolução;
   a validação pode levar até 60 dias.
   https://www.mercadolivre.com.br/l/comece-a-recomendar
5. Os canais de divulgação têm restrições; consultar o checklist oficial.
   https://www.mercadolivre.com.br/l/checklist
6. A API pública de desenvolvedores possui OAuth e recursos gerais, mas
   **não foi identificado nesta pesquisa um endpoint público documentado
   especificamente para gerar links do Programa de Afiliados ou consultar
   suas comissões**. Não presumir que a API de vendedores faça isso.
   https://developers.mercadolivre.com.br/

## Decisão técnica

A integração segura, por enquanto, é **assistida pelo portal oficial**:
- selecionar produtos e obter links na Central ou Barra oficial;
- importar os links com referência de origem no registro local do Automata;
- sugerir etiquetas por canal (sem afirmar que foram criadas no portal);
- gerar rascunhos e acompanhar resultados via relatórios autorizados.

Não automatizar cliques no portal nem coletar cookies/tokens privados sem
confirmação de autorização e regras aplicáveis. Não construir links por
concatenação ou inferir parâmetros de rastreamento.

## O que falta

Confirmar adesão e elegibilidade da conta, acesso ao painel e recursos
disponíveis, se existe API/parceria formal para afiliados, termos e canais
permitidos. Depois implementar importação de relatórios e conciliação de
comissões. Não há conexão de conta nem testes reais.
