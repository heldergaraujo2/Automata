"""Optional local Ollama copy assistant; never invent product facts."""
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from .core import Offer

def suggest_caption(offer: Offer, endpoint: str | None = None, model: str | None = None) -> str:
    offer.validate()
    endpoint = endpoint or os.environ.get("AUTOMATA_OLLAMA_URL", "http://127.0.0.1:11434")
    model = model or os.environ.get("AUTOMATA_OLLAMA_MODEL", "qwen3:8b")
    parsed = urlparse(endpoint)
    if parsed.scheme != "http" or parsed.hostname not in ("localhost", "127.0.0.1") or parsed.port != 11434:
        raise ValueError("Somente Ollama local na porta 11434 é permitido nesta versão")
    prompt = (
        "Escreva em português brasileiro uma legenda curta de divulgação. "
        "Use APENAS os fatos fornecidos. Não invente descontos, avaliações, "
        "escassez, benefícios, preços ou promessas. Não altere o link. "
        "Identifique explicitamente publicidade e link de afiliado. "
        f"Produto: {offer.title}\nDescrição verificada: {offer.description}\n"
        f"Preço informado: R$ {offer.price_brl:.2f}\n"
        f"Link: {offer.affiliate_url}\n"
    )
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}}).encode()
    req = Request(endpoint.rstrip("/") + "/api/generate", data=payload,
                  headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=120) as response:
        result = json.load(response)
    suggestion = result.get("response", "").strip()
    if not suggestion:
        raise ValueError("Modelo retornou resposta vazia")
    # AI suggestions are untrusted and require human/factual review before publication.
    return suggestion
