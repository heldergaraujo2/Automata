"""Draft customer replies using only approved product data."""
from .core import Offer

def reply_to_question(offer: Offer, question: str) -> str:
    offer.validate()
    if not question.strip():
        raise ValueError("Pergunta vazia")
    return (
        f"Sobre {offer.title}: {offer.description}. "
        f"Preço informado: R$ {offer.price_brl:.2f}, sujeito a alteração. "
        f"Consulte disponibilidade, frete e condições na loja: {offer.affiliate_url}. "
        "Este é um link de afiliado. Para informações não confirmadas, consulte o vendedor."
    )
