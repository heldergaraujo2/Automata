"""Connect catalog, verified copy, media gate and publishing draft queue."""
from pathlib import Path
from .catalog import load_offers
from .content import make_draft
from .publishing import queue_draft
from .rights import authorized_media

def run(catalog: Path, output: Path) -> list[Path]:
    results = []
    for offer in load_offers(catalog):
        draft = make_draft(offer)
        # Video composition is deliberately separate until licensed local media are available.
        # No automatic publication, scraping, checkout or paid ads.
        if authorized_media(offer):
            pass
        results.append(queue_draft(draft, output))
    return results
