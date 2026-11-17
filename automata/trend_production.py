"""Bridge approved, locally supplied media to vertical FFmpeg composition.

No third-party downloads. Original trend media must be produced independently
or obtained with verified reuse rights before passing its local path.
"""
from dataclasses import dataclass
from pathlib import Path
from media.compose_split import compose
from .trend_scripts import VideoPlan

@dataclass(frozen=True)
class ProductionAssets:
    top_video: Path
    product_video: Path
    top_rights_verified: bool
    product_rights_verified: bool

def render_vertical(plan: VideoPlan, assets: ProductionAssets, output: Path) -> Path:
    if plan.strategy not in {"licensed_repost", "original_content"}:
        raise ValueError("Estratégia desconhecida")
    if not (assets.top_rights_verified and assets.product_rights_verified):
        raise PermissionError("Ambos os vídeos exigem direitos verificados")
    if plan.strategy == "original_content" and plan.status != "pending_original_media_creation":
        raise ValueError("Plano original em estado inválido")
    if plan.strategy == "licensed_repost" and plan.status != "pending_media_verification":
        raise ValueError("Plano de repost em estado inválido")
    compose(assets.top_video, assets.product_video, output, max_seconds=60.0)
    return output
