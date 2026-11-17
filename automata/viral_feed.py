"""Import licensed trend observations from an authorized JSON export.

Provider-neutral boundary: no TikTok scraping, downloading, or publishing.
"""
import json
from pathlib import Path
from .viral_reposts import ViralCandidate, rank_candidates, prepare_repost

def load_feed(path: Path) -> list[ViralCandidate]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Feed precisa ser uma lista")
    items = []
    for row in data:
        if not isinstance(row, dict):
            raise ValueError("Item inválido")
        item = ViralCandidate(**row)
        item.validate()
        items.append(item)
    return rank_candidates(items)

def build_review_queue(feed: Path, output: Path, *, approved_sources: set[str] | None = None) -> dict[str, int]:
    """Only explicitly approved source URLs can become licensed review drafts."""
    approved_sources = approved_sources or set()
    candidates = load_feed(feed)
    queue = []
    seen = set()
    counts = {"discovered": len(candidates), "review_ready": 0, "blocked": 0}
    for candidate in candidates:
        if candidate.source_url in seen:
            continue
        seen.add(candidate.source_url)
        if candidate.source_url not in approved_sources:
            counts["blocked"] += 1
            continue
        try:
            draft = prepare_repost(candidate, approved=True)
        except (ValueError, PermissionError):
            counts["blocked"] += 1
            continue
        queue.append(draft)
        counts["review_ready"] += 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    return counts
