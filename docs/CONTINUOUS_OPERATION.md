# Operação periódica — fundação

O serviço `automata.service` grava cada ciclo no SQLite, com início, fim, status e contadores. Executa uma vez por padrão; `--continuous` repete em intervalo mínimo de 60 segundos.

Exemplo futuro, em ambiente isolado:
```powershell
python -m automata.service --catalog examples/offers.example.json --interval 3600 --continuous
```

**Não execute com ofertas fictícias como se fossem reais.** Ainda não há integração de marketplace, API social, autenticação ou monitoramento externo.

Limitações: não há bloqueio entre processos; múltiplas instâncias podem conflitar. O ciclo pode recriar rascunhos com o mesmo ID. Falhas de infraestrutura encerram o processo; falta supervisor de reinício, heartbeat, alertas e retry exponencial. O loop não publica, compra, responde mensagens ou gasta dinheiro. Testes ainda não executados no PC do usuário.
