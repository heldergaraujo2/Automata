# Automata — quatro etapas integradas

1. **Portão de mídias:** verificar autorização declarada, SHA-256 e metadados FFprobe de ambos os vídeos antes da renderização.
2. **Montagem:** usar o renderizador vertical split-screen existente; opcionalmente adicionar narração WAV e legendas SRT pelo adaptador FFmpeg.
3. **Revisão:** colocar o MP4 final na fila `pending_review`; nenhuma publicação ou agendamento automático.
4. **Validação preparada:** testes unitários de bloqueio, tipos de entrada, legendas sem narração, campos obrigatórios e planejamento sem efeitos colaterais.

Implementação central: `automata/verified_video_workflow.py`.
Testes: `tests/test_verified_video_workflow.py`.

## Limites explícitos
- Nenhum teste foi executado; integração funcional não comprovada.
- A composição existente exige **dois vídeos**; imagens estáticas precisam ser convertidas antes. A montagem não cria automaticamente cenas ou efeitos adicionais.
- A voz precisa ser um WAV já existente; a síntese Piper continua em módulo separado.
- A validação de arquivo verifica hash e metadados, não qualidade visual ou validade jurídica da licença.
- O renderizador legado ainda pode ser chamado diretamente por outros módulos: a obrigatoriedade global do portão não foi garantida.
- A execução é bloqueada por padrão (`allow_execution=False`), sem contas, downloads, publicação ou uso do PC do usuário.
- Antes de executar localmente, avaliar segurança de caminhos, saída existente, limpeza de intermediários, sincronização das legendas e testes de integração.

Progresso estimado após este ciclo: aproximadamente 45% do escopo total, **não** medição de testes aprovados.
