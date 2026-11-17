"""Connect affiliate campaign drafts to video briefs, rendering and review queue.

Rendering requires local, rights-cleared media; nothing is downloaded or posted.
"""
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from .trend_scripts import VideoPlan
from .trend_production import ProductionAssets, render_vertical
from .video_queue import queue_video

@dataclass(frozen=True)
class AffiliateVideoBrief:
    product_id: str
    channel: str
    caption: str
    affiliate_url: str
    scenes: tuple[str, ...]
    status: str = "awaiting_media"

def make_brief(campaign: dict) -> AffiliateVideoBrief:
    if campaign.get("status") != "pending_review":
        raise PermissionError("Campanha ainda não está elegível")
    for field in ("product_id", "channel", "caption", "affiliate_url"):
        if not isinstance(campaign.get(field), str) or not campaign[field].strip():
            raise ValueError(f"Campo ausente: {field}")
    if campaign["channel"] not in ("tiktok", "instagram", "facebook"):
        raise ValueError("Canal inválido")
    return AffiliateVideoBrief(
        campaign["product_id"], campaign["channel"], campaign["caption"],
        campaign["affiliate_url"],
        ("Abertura original sobre a tendência, sem copiar conteúdo protegido.",
         "Demonstração autorizada do produto com informações verificadas.",
         "Chamada para ação e aviso de publicidade."))

def export_briefs(campaigns: Path, output: Path) -> int:
    raw = json.loads(campaigns.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Esperada lista de campanhas")
    briefs = [asdict(make_brief(c)) for c in raw]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(briefs, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(briefs)

def render_and_queue(brief: AffiliateVideoBrief, assets: ProductionAssets,
                     output_video: Path, queue_directory: Path) -> Path:
    if brief.status != "awaiting_media":
        raise ValueError("Brief não elegível")
    if not assets.top_rights_verified or not assets.product_rights_verified:
        raise PermissionError("Mídia sem direitos confirmados")
    plan = VideoPlan(brief.affiliate_url, "original_content", brief.product_id,
                     "", brief.scenes, "", "pending_original_media_creation")
    rendered = render_vertical(plan, assets, output_video)
    return queue_video(rendered, brief.caption, queue_directory,
                       rights_verified=True, source_url=brief.affiliate_url)
