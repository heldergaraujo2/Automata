# Integração de tendências virais — etapa 1

Criado importador de feed JSON fornecido por fonte autorizada. O módulo
classifica vídeos por engajamento, remove duplicatas pela URL de origem e
gera uma fila de revisão somente para URLs explicitamente aprovadas e
com evidência declarada de direitos e mídia HTTPS.

Exemplo de execução futura:
```powershell
python -m automata.viral_cli --feed input/viral_feed.json --approved-sources input/approved_sources.json
```

O arquivo `approved_sources.json` é uma lista JSON de URLs de origem.
A fila gerada é `output/viral_review.json` e **não** é enviada às redes.

A aprovação da URL e o campo de evidência não comprovam por si sós que a
licença é autêntica: uma revisão confiável deve verificar os direitos antes
da publicação. O módulo não extrai nem baixa vídeos do TikTok, não usa
scraping, não acessa contas e não faz postagem.

Próximos passos: selecionar e credenciar provedor oficial/autorizado de
dados de tendências, validar origem e licença de cada mídia, implementar
monitoramento incremental e conectar revisão humana à API oficial de
publicação com consentimento do titular.
