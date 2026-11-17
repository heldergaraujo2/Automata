"""Deterministic original video storyboards for affiliate campaigns.

No AI/media service calls. Narration is a text script, not synthesized audio.
"""
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse

@dataclass(frozen=True)
class Scene:
    seconds: int
    visual_direction: str
    narration: str
    rights_requirement: str

@dataclass(frozen=True)
class Storyboard:
    product_id: str
    channel: str
    format: str
    resolution: str
    duration_seconds: int
    scenes: tuple[Scene, ...]
    affiliate_url: str
    status: str = "awaiting_media_and_voice"

def create_storyboard(campaign: dict) -> Storyboard:
    if campaign.get("status") != "pending_review":
        raise PermissionError("A campanha precisa estar pendente de revisão")
    for key in ("product_id", "channel", "affiliate_url", "caption"):
        if not isinstance(campaign.get(key), str) or not campaign[key].strip():
            raise ValueError(f"Campo obrigatório: {key}")
    if campaign["channel"] not in {"tiktok", "instagram", "facebook"}:
        raise ValueError("Rede social não suportada")
    url = urlparse(campaign["affiliate_url"])
    if url.scheme != "https" or not url.netloc or url.username or url.password:
        raise ValueError("Link HTTPS inválido")
    # Never assert unverified product specifications or discount claims.
    scenes = (
        Scene(6, "Abertura com imagem original sobre a necessidade do público",
              "Procurando uma opção para facilitar o seu dia a dia?",
              "original_or_licensed"),
        Scene(16, "Exibir demonstração autorizada do produto, sem inventar características",
              "Confira os detalhes do produto no anúncio original antes de comprar.",
              "original_or_licensed"),
        Scene(12, "Mostrar exemplos visuais próprios de uso, se verificáveis",
              "Compare as informações e veja se esta opção atende ao que você procura.",
              "original_or_licensed"),
        Scene(6, "Tela final com identificação publicitária e indicação do link",
              "Acesse o link de afiliado para conferir o preço atualizado. Publicidade.",
              "original_or_licensed"),
    )
    return Storyboard(campaign["product_id"], campaign["channel"],
                      "split_screen", "1080x1920", 40, scenes,
                      campaign["affiliate_url"])

def export_storyboards(campaigns: Path, destination: Path) -> int:
    records = json.loads(campaigns.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("Campanhas devem ser uma lista")
    boards = [asdict(create_storyboard(item)) for item in records]
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(boards, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(boards)
