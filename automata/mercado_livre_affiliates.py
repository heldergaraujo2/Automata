"""Offline Mercado Livre affiliate intake; does not generate or alter referral links.

The actual referral URL must be supplied by the authorized affiliate program.
No API calls, scraping, account connection, or publication.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
import json
from .affiliate_only import AffiliateItem, prepare_affiliate_promotion

@dataclass(frozen=True)
class MercadoLivreSourceRecord:
    item_id: str
    title: str
    description: str
    price_brl: float
    product_url: str
    affiliate_url: str
    evidence_source: str
    checked_at: str

    def validate(self) -> None:
        if not all((self.item_id.strip(), self.title.strip(), self.description.strip(),
                    self.evidence_source.strip(), self.checked_at.strip())):
            raise ValueError("Dados ou evidências incompletos")
        for value in (self.product_url, self.affiliate_url):
            parsed = urlparse(value)
            if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                raise ValueError("URL HTTPS inválida")
        if self.price_brl <= 0:
            raise ValueError("Preço inválido")

def build_campaign(record: MercadoLivreSourceRecord,
                   channels: tuple[str, ...] = ("tiktok", "instagram", "facebook")) -> list[dict]:
    record.validate()
    item = AffiliateItem(record.item_id, "mercado_livre", record.title,
                         record.description, record.affiliate_url, record.price_brl)
    drafts = []
    for channel in channels:
        draft = prepare_affiliate_promotion(item, channel)
        draft["source_product_url"] = record.product_url
        draft["evidence_source"] = record.evidence_source
        draft["checked_at"] = record.checked_at
        drafts.append(draft)
    return drafts

def export_campaigns(source: Path, destination: Path) -> int:
    records = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("Esperada lista de produtos")
    seen = set()
    drafts = []
    for raw in records:
        record = MercadoLivreSourceRecord(**raw)
        if record.item_id in seen:
            raise ValueError("Produto duplicado")
        seen.add(record.item_id)
        drafts.extend(build_campaign(record))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(drafts)
