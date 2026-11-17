# Saída FFmpeg → revisão → agendamento

O novo `automata.video_queue` recebe um MP4 já renderizado e cria um
rascunho JSON em `output/drafts`, no formato compatível com o agendador
existente. Inicialmente o status é `pending_review` e a data é vazia.

Após aprovação explícita, `approve_and_schedule` define o status
`approved` e um horário com fuso. Só então `scheduler.due_drafts`
pode selecionar o registro como vencido. Nenhuma API externa é chamada.

Exemplo de inclusão de vídeo final:
```powershell
python -m automata.video_queue_cli --video output/final.mp4 --caption "Publicidade | Link de afiliado" --rights-verified
```

Limitações: o sinalizador de direitos é declaratório, não verificação
independente de licença. A checagem de arquivo não valida codecs, resolução,
duração ou conteúdo. Ainda não há upload para hospedagem HTTPS, tokens,
publicação real, retry, deduplicação entre ciclos ou métricas de postagem.
A aprovação é feita via função Python, não por painel. Os testes
adicionados ainda não foram executados.
