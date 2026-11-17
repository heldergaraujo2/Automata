"""Commerce routing for affiliate promotions vs authorized seller listings.

No provider API calls, account connections, scraping or live listing creation.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
import json

SUPPORTED_SOURCES = {"magalu", "pichau", "other"}
SUPPORTED_CHANNELS = {"tiktok", "instagram", "facebook", "tiktok_shop", "mercado_livre"}

@dataclass(frozen=True)
class CommerceProduct:
    id: str
    source: str
    title: str
    description: str
    price_brl: float
    source_url: str
    affiliate_url: str = ""
    verified_facts: tuple[str, ...] = ()
    image_rights_verified: bool = False
    seller_authorized: bool = False
    inventory_confirmed: bool = False
    fulfillment_confirmed: bool = False

    def validate(self) -> None:
        if not self.id.strip() or not self.title.strip() or not self.description.strip():
            raise ValueError("ID, título e descrição obrigatórios")
        if self.source not in SUPPORTED_SOURCES or self.price_brl <= 0:
            raise ValueError("Fonte ou preço inválido")
        for url in (self.source_url, self.affiliate_url):
            if not url:
                continue
            p = urlparse(url)
            if p.scheme != "https" or not p.netloc or p.username or p.password:
                raise ValueError("URL HTTPS inválida")

@dataclass(frozen=True)
class CommerceDraft:
    product_id: str
    channel: str
    mode: str
    title: str
    description: str
    destination_url: str
    status: str
    reason: str

def create_commerce_draft(product: CommerceProduct, channel: str,
                          mode: str = "affiliate") -> CommerceDraft:
    product.validate()
    if channel not in SUPPORTED_CHANNELS:
        raise ValueError("Canal desconhecido")
    if mode not in {"affiliate", "seller_listing"}:
        raise ValueError("Modelo comercial desconhecido")
    facts = "\n".join(f"- {fact}" for fact in product.verified_facts if fact.strip())
    description = (f"{product.title}\n{product.description}\n"
                   f"Preço de referência: R$ {product.price_brl:.2f} (sujeito a alteração).\n"
                   + (f"Características verificadas:\n{facts}\n" if facts else ""))
    if mode == "affiliate":
        if not product.affiliate_url:
            return CommerceDraft(product.id, channel, mode, product.title, description,
                                 "", "blocked", "affiliate_link_missing")
        if channel in {"mercado_livre", "tiktok_shop"}:
            return CommerceDraft(product.id, channel, mode, product.title, description,
                                 product.affiliate_url, "needs_channel_policy_check",
                                 "affiliate_links_may_not_be_supported_as_store_listings")
        return CommerceDraft(product.id, channel, mode, product.title,
                             description + "Publicidade | Link de afiliado.",
                             product.affiliate_url, "pending_review", "affiliate_promotion")
    if channel not in {"mercado_livre", "tiktok_shop"}:
        raise ValueError("Anúncio de vendedor requer marketplace")
    if not (product.seller_authorized and product.inventory_confirmed
            and product.fulfillment_confirmed):
        return CommerceDraft(product.id, channel, mode, product.title, description,
                             "", "blocked", "seller_authorization_inventory_or_fulfillment_missing")
    return CommerceDraft(product.id, channel, mode, product.title, description,
                         "", "pending_review", "seller_listing_requires_provider_validation")

def export_commerce_drafts(products: list[CommerceProduct], channels: list[str],
                           output: Path, mode: str = "affiliate") -> int:
    drafts = [asdict(create_commerce_draft(product, channel, mode))
              for product in products for channel in channels]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(drafts)
