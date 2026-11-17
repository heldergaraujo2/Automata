"""Convert complete offline affiliate leads to review-only social campaigns.

This module neither verifies external program enrollment nor publishes posts.
"""
import json
from pathlib import Path
from .affiliate_discovery import ProductLead, assess_lead
from .affiliate_only import AffiliateItem, prepare_affiliate_promotion

CHANNELS = ("tiktok", "instagram", "facebook")

def campaign_from_lead(lead: ProductLead) -> list[dict]:
    assessment = assess_lead(lead)
    if assessment["status"] != "ready_for_draft":
        return []
    item = AffiliateItem(
        id=lead.product_id, program=lead.program, title=lead.title,
        verified_description=lead.verified_description,
        affiliate_url=lead.affiliate_url, price_brl=lead.price_brl)
    drafts = []
    for channel in CHANNELS:
        draft = prepare_affiliate_promotion(item, channel)
        draft["product_url"] = lead.product_url
        draft["evidence_source"] = lead.evidence_source
        draft["checked_at"] = lead.checked_at
        drafts.append(draft)
    return drafts

def build_campaigns(source: Path, destination: Path) -> dict[str, int]:
    raw = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Entrada precisa ser lista JSON")
    seen = set()
    drafts = []
    blocked = 0
    for record in raw:
        # Accept either source records or output of affiliate_discovery,
        # discarding assessment-only fields and recalculating eligibility.
        fields = ProductLead.__dataclass_fields__
        lead = ProductLead(**{key: value for key, value in record.items() if key in fields})
        key = (lead.program, lead.product_id)
        if key in seen:
            continue
        seen.add(key)
        result = campaign_from_lead(lead)
        if not result:
            blocked += 1
            continue
        drafts.extend(result)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"unique_products": len(seen), "blocked_products": blocked, "drafts": len(drafts)}
