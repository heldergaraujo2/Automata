# Agentes e limites

## Agente pesquisador
Recebe dados de fontes autorizadas, documenta origem, preço, validade e disponibilidade. Não realiza scraping proibido nem inventa links de afiliados.

## Agente redator
O módulo `automata/llm.py` oferece uma interface opcional para Ollama local (porta 11434). Saídas são sugestões não verificadas; não publicá-las sem revisão factual. O pipeline atual continua usando legendas determinísticas.

## Agente de vídeo
O compositor recebe dois arquivos locais com direitos documentados, viral em cima e produto embaixo, até 60 s, simultaneamente. Não gera nem baixa vídeos de terceiros.

## Agente de publicação
A fila atual gera apenas rascunhos JSON. Futuras integrações com Meta/TikTok exigirão autenticação oficial, consentimento e limites de uso.

## Agente financeiro
O ledger CSV conta apenas comissões aprovadas e despesas efetivas. Comissão pendente não é lucro. Gastos dependem de aprovação humana.

## Orquestrador
`automata/pipeline.py` coordena catálogo, conteúdo, mídia e rascunhos. Ainda não existe execução contínua ou integração com contas reais.

## Próximos conectores
Adaptadores oficiais de afiliados, APIs sociais, tendências, atendimento, scheduler e monitoramento. Cada adaptador deve ter testes e ser isolado do núcleo.
