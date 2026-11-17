"""Offline discovery intake for officially supplied affiliate catalog exports.

Never invents referral URLs or scrapes sites. Items without verified facts
or official referral links remain blocked, rather than being advertised.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
import json

@dataclass(frozen=True)
class ProductLead:
    program: str
    product_id: str
    title: str
    product_url: str
    affiliate_url: str = ""
    verified_description: str = ""
    price_brl: float | None = None
    evidence_source: str = ""
    checked_at: str = ""

def _https(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username and not parsed.password

def assess_lead(lead: ProductLead) -> dict:
    if lead.program not in {"mercado_livre", "magalu", "pichau", "tiktok_shop"}:
        raise ValueError("Programa não reconhecido")
    if not lead.product_id.strip() or not lead.title.strip() or not _https(lead.product_url):
        raise ValueError("Identificador, título e URL original são obrigatórios")
    missing = []
    if not _https(lead.affiliate_url):
        missing.append("official_affiliate_link")
    if not lead.verified_description.strip():
        missing.append("verified_description")
    if lead.price_brl is None or lead.price_brl <= 0:
        missing.append("verified_price")
    if not lead.evidence_source.strip() or not lead.checked_at.strip():
        missing.append("source_evidence_and_timestamp")
    return {**asdict(lead), "status": "ready_for_draft" if not missing else "needs_verification",
            "missing": missing}

def import_leads(source: Path, destination: Path) -> dict[str, int]:
    raw = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("A lista de descoberta deve ser JSON array")
    seen = set()
    result = []
    for entry in raw:
        lead = ProductLead(**entry)
        key = (lead.program, lead.product_id)
        if key in seen:
            continue
        seen.add(key)
        result.append(assess_lead(lead))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"total": len(result),
            "ready_for_draft": sum(x["status"] == "ready_for_draft" for x in result),
            "needs_verification": sum(x["status"] == "needs_verification" for x in result)}
