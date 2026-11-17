"""Run a bounded local draft cycle with per-offer failure isolation and audit."""
from dataclasses import replace
from pathlib import Path
from .audit import record_event
from .catalog import load_offers
from .content import make_draft
from .media import render_offer
from .publishing import queue_draft

def run_cycle(catalog: Path, output: Path, audit_path: Path) -> dict[str, int]:
    counts = {"queued": 0, "failed": 0}
    offers = load_offers(catalog)
    for offer in offers:
        try:
            draft = make_draft(offer)
            video = render_offer(offer, output.parent / "videos")
            if video is not None:
                draft = replace(draft, video_path=str(video))
            queue_draft(draft, output)
        except (ValueError, OSError, RuntimeError) as exc:
            counts["failed"] += 1
            record_event(audit_path, "draft_cycle", offer.id, "failed:" + type(exc).__name__)
        else:
            counts["queued"] += 1
            record_event(audit_path, "draft_cycle", offer.id, "queued")
    return counts
