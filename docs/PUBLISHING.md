# Publicação e agendamento — implementação inicial

`automata/scheduler.py` identifica rascunhos aprovados com `scheduled_at` em ISO 8601 com fuso. Não executa publicações; apenas retorna arquivos elegíveis.

`automata/social.py` define o contrato para futuros conectores oficiais de redes sociais e bloqueia publicações enquanto não houver credenciais, permissões e revisão.

Fluxo planejado: rascunho -> revisão de conteúdo e direitos -> aprovação -> agendamento -> API oficial -> registro de ID da postagem -> métricas.

As integrações com Instagram, Facebook e TikTok **não estão conectadas**. Não usar cookies de navegador ou automações que violem os termos das plataformas. O agendador ainda não é um serviço 24/7.
