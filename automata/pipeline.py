"""Catalog -> verified copy -> licensed video -> review queue."""
from dataclasses import replace
from pathlib import Path
from .catalog import load_offers
from .content import make_draft
from .media import render_offer
from .publishing import queue_draft

def run(catalog: Path, output: Path) -> list[Path]:
    results = []
    for offer in load_offers(catalog):
        draft = make_draft(offer)
        video = render_offer(offer, output.parent / "videos")
        if video is not None:
            draft = replace(draft, video_path=str(video))
        results.append(queue_draft(draft, output))
    return results
