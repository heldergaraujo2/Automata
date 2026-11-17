from .core import Offer, Draft

def make_draft(offer: Offer) -> Draft:
    offer.validate()
    caption = (f"{offer.title}\n{offer.description}\n"
               f"Preço informado: R$ {offer.price_brl:.2f} (confirme na loja).\n"
               f"Confira: {offer.affiliate_url}\n"
               "Publicidade | Link de afiliado: posso receber comissão por compras qualificadas.")
    return Draft(offer.id, f"Conheça: {offer.title}", caption, offer.affiliate_url)
