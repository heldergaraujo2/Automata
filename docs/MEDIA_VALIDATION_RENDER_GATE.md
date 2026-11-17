# Automata — validação de arquivos antes de renderizar

Os módulos `automata/media_file_validation.py` e `automata/media_render_gate.py`
preparam a verificação de mídias antes da produção.

Com execução explicitamente habilitada na fase final, o verificador calcula
SHA-256 real, compara com o hash registrado e usa FFprobe para verificar
stream visual, dimensões mínimas e duração de vídeos (até 60 segundos).
O portão exige aprovação de direitos e validação de todos os arquivos.

**Status:** implementação no GitHub, testes escritos e não executados.
A verificação não atesta licença juridicamente, qualidade visual nem
decodificação integral. A integração direta com o renderizador FFmpeg
ainda está pendente, assim como testes de ponta a ponta.
Nenhum download, FFprobe, FFmpeg ou publicação foi executado.
