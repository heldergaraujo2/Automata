# Hospedagem e envio — preparação sem contas reais

Criados contratos de hospedagem e despachante de publicações agendadas para
Instagram, Facebook e TikTok. O despachante lê apenas rascunhos aprovados e
vencidos, com direitos declarados, e prepara tarefas para contas explicitamente
habilitadas. Cada tarefa exige URL HTTPS de vídeo hospedado.

**Não ocorre upload nem publicação real.** O provedor de hospedagem está
desabilitado intencionalmente; adaptadores de publicação também continuam
bloqueados. O despachante é dry-run e não chama APIs externas.

Pendente para o teste real no PC do usuário:
- escolher provedor de hospedagem, configurar autenticação e armazenamento;
- verificar licenças, disponibilidade das URLs e formato do vídeo;
- registrar apps Meta/TikTok, consentir OAuth e guardar tokens com segurança;
- implementar e validar fluxos oficiais de upload/publicação/status;
- lidar com limites de API, falhas, retries e idempotência;
- testar em ambiente controlado antes de liberar agendamento automático.

Nunca incluir credenciais ou vídeos privados no repositório GitHub.
