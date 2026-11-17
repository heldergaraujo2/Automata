# Narração local: reutilizar projetos existentes

## Projetos encontrados (17/11/2026)

**Piper TTS**: motor local rápido, com vozes pt_BR como Faber,
Jeff, Cadu e Edresson. O repositório histórico rhasspy/piper está
arquivado; consultar a distribuição atual antes da instalação.
- https://github.com/rhasspy/piper
- https://github.com/rhasspy/piper/blob/master/VOICES.md
- https://piperhub.org/pt/guides/

**Kokoro TTS**: alternativa local com português brasileiro, incluindo
vozes pf_dora e pm_alex. Avaliar qualidade e requisitos no Windows.
- https://github.com/hexgrad/kokoro
- https://github.com/TuriaArt/Kokoro-TTS-Local-TU

## Decisão

Usar **Piper como primeiro adaptador** pela simplicidade e execução
offline; manter Kokoro como candidato para qualidade de voz.
Nenhum motor foi copiado, instalado, executado ou validado em hardware.
A licença de cada voz deve ser conferida antes de uso comercial.

`automata.local_narration` prepara texto, legendas SRT aproximadas
por cena e uma interface para executar o Piper **somente quando
allow_execution=True** na etapa final de testes locais. Não há
alinhamento real com áudio: o tempo das legendas é o tempo previsto
de cada cena. Sincronização fina exige áudio gerado e alinhamento
posterior, por exemplo via ferramenta de transcrição/alinhamento.

A próxima etapa é encaixar o WAV real no FFmpeg, comparar a duração
com as cenas e renderizar com legendas, sem publicar automaticamente.
