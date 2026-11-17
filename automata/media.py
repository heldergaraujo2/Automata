"""Bridge the existing FFmpeg split-screen composer into the affiliate workflow."""
from pathlib import Path
from media.compose_split import compose
from .core import Offer
from .rights import authorized_media

def render_offer(offer: Offer, directory: Path) -> Path | None:
    if not authorized_media(offer):
        return None
    viral, product = Path(offer.media_viral), Path(offer.media_product)
    if not viral.is_file() or not product.is_file():
        raise FileNotFoundError("Vídeos autorizados não encontrados no computador")
    directory.mkdir(parents=True, exist_ok=True)
    safe_id = "".join(c for c in offer.id if c.isalnum() or c in "-_")
    if not safe_id:
        raise ValueError("ID de produto inválido")
    target = directory / f"{safe_id}.mp4"
    compose(viral, product, target)
    return target
