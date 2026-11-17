from .core import Offer

def authorized_media(offer: Offer) -> bool:
    return bool(offer.media_product and offer.media_viral
                and offer.rights_product.strip() and offer.rights_viral.strip())
