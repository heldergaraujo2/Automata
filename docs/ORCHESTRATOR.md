# Orquestrador inicial

Comando (quando houver ambiente de testes):
```powershell
python -m automata.runner --catalog examples/offers.example.json
```

O ciclo valida ofertas, cria descrições determinísticas, tenta compor vídeos **somente quando os dois caminhos e registros de autorização são fornecidos**, cria rascunhos e registra resultados. Falhas de uma oferta são isoladas das demais.

Ainda não é um agente autônomo 24/7: falta scheduler persistente, conectores oficiais de produtos/redes, monitoramento, revisão de direitos e de fatos, aprovação e integração com Ollama. A saída é uma fila local, não publicações reais.

Segredos não devem ser gravados no catálogo ou em logs. Não colocar dados reais de clientes nos exemplos.
