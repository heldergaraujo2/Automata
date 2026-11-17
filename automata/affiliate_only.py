"""Affiliate-only channel policy: no seller listings, inventory or order handling."""
from dataclasses import dataclass
from urllib.parse import urlparse

SUPPORTED_PROGRAMS = ("mercado_livre", "magalu", "pichau", "tiktok_shop")
SOCIAL_CHANNELS = ("tiktok", "instagram", "facebook")

@dataclass(frozen=True)
class AffiliateItem:
    id: str
    program: str
    title: str
    verified_description: str
    affiliate_url: str
    price_brl: float
    commission_rate: float | None = None

    def validate(self) -> None:
        if self.program not in SUPPORTED_PROGRAMS:
            raise ValueError("Programa não suportado")
        if not self.id or not self.title or not self.verified_description or self.price_brl <= 0:
            raise ValueError("Dados verificados insuficientes")
        parsed = urlparse(self.affiliate_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError("Link de afiliado HTTPS obrigatório")
        if self.commission_rate is not None and not 0 <= self.commission_rate <= 1:
            raise ValueError("Comissão fora do intervalo 0 a 1")

def prepare_affiliate_promotion(item: AffiliateItem, channel: str) -> dict[str, str]:
    item.validate()
    if channel not in SOCIAL_CHANNELS:
        raise ValueError("Destino não é um canal de divulgação suportado")
    caption = (f"{item.title}\n{item.verified_description}\n"
               f"Preço de referência: R$ {item.price_brl:.2f}; confirme no vendedor.\n"
               f"Confira: {item.affiliate_url}\n"
               "Publicidade | Link de afiliado: posso receber comissão.")
    return {"product_id": item.id, "program": item.program,
            "channel": channel, "caption": caption,
            "affiliate_url": item.affiliate_url, "status": "pending_review"}

def estimated_commission(item: AffiliateItem) -> float | None:
    item.validate()
    return (round(item.price_brl * item.commission_rate, 2)
            if item.commission_rate is not None else None)
