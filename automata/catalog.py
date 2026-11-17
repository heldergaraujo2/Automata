import json
from pathlib import Path
from .core import Offer

def load_offers(path: Path) -> list[Offer]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Catálogo deve ser lista")
    offers = [Offer(**row) for row in data]
    ids = set()
    for offer in offers:
        offer.validate()
        if offer.id in ids:
            raise ValueError("ID duplicado")
        ids.add(offer.id)
    return offers
