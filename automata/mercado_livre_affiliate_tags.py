"""Offline campaign labels for Mercado Livre affiliate tracking.

Tags are suggestions only: operator must create/assign them in official portal.
"""
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class TaggedCampaign:
    product_id: str
    channel: str
    tag_suggestion: str
    affiliate_url: str
    status: str = "pending_official_tag_assignment"

def suggest_tag(product_id: str, channel: str) -> str:
    if channel not in ("tiktok", "instagram", "facebook"):
        raise ValueError("Canal inválido")
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", product_id).lower()
    if not cleaned:
        raise ValueError("ID de produto inválido")
    # Mercado Livre labels: up to 30 alphanumeric characters, no spaces.
    return (channel + cleaned)[:30]

def prepare_tagged_campaign(campaign: dict) -> TaggedCampaign:
    if campaign.get("status") != "pending_review":
        raise PermissionError("Campanha não revisável")
    if not campaign.get("affiliate_url", "").startswith("https://"):
        raise ValueError("Link de afiliado ausente")
    return TaggedCampaign(
        product_id=campaign["product_id"], channel=campaign["channel"],
        tag_suggestion=suggest_tag(campaign["product_id"], campaign["channel"]),
        affiliate_url=campaign["affiliate_url"])
