"""Rank trend observations supplied by permitted data providers."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Trend:
    topic: str
    views: int
    likes: int
    comments: int
    source_url: str

def rank_trends(items: list[Trend]) -> list[Trend]:
    for t in items:
        if min(t.views, t.likes, t.comments) < 0 or not t.source_url.startswith("https://"):
            raise ValueError("Métricas ou origem inválidas")
    return sorted(items, key=lambda t: ((t.likes + 2 * t.comments) / max(t.views, 1), t.views), reverse=True)
