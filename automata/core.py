from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass(frozen=True)
class Offer:
    id: str
    title: str
    price_brl: float
    affiliate_url: str
    source: str
    description: str
    media_product: str = ""
    media_viral: str = ""
    rights_product: str = ""
    rights_viral: str = ""

    def validate(self):
        u = urlparse(self.affiliate_url)
        if not all((self.id, self.title, self.source, self.description)) or self.price_brl <= 0:
            raise ValueError("Dados obrigatórios ausentes")
        if u.scheme != "https" or not u.netloc or u.username or u.password:
            raise ValueError("URL de afiliado inválida")

@dataclass(frozen=True)
class Draft:
    offer_id: str
    title: str
    caption: str
    affiliate_url: str
    video_path: str | None = None
    status: str = "pending_review"
