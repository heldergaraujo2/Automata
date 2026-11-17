"""Route every discovered trend into licensed repost or original-content brief.

A trend is retained even when its source video cannot legally be reused.
This module never downloads or publishes third-party video.
"""
from dataclasses import dataclass
from .viral_reposts import ViralCandidate, prepare_repost

@dataclass(frozen=True)
class TrendDecision:
    source_url: str
    creator_handle: str
    strategy: str
    reason: str
    payload: dict[str, str]

def decide_trend(candidate: ViralCandidate, *, rights_verified: bool = False,
                 approved: bool = False) -> TrendDecision:
    candidate.validate()
    if rights_verified and approved:
        try:
            repost = prepare_repost(candidate, approved=True)
        except (ValueError, PermissionError):
            pass
        else:
            return TrendDecision(candidate.source_url, candidate.creator_handle,
                                 "licensed_repost", "rights_verified", repost)
    brief = {
        "topic_reference": candidate.source_url,
        "creator_reference": candidate.creator_handle,
        "instruction": (
            "Criar roteiro e vídeo inteiramente originais sobre a tendência; "
            "não reutilizar imagens, áudio ou trechos protegidos do vídeo de origem."
        ),
        "status": "original_brief_pending_creation",
    }
    return TrendDecision(candidate.source_url, candidate.creator_handle,
                         "original_content", "source_media_not_cleared", brief)

def route_trends(candidates: list[ViralCandidate],
                 verified_urls: set[str] | None = None,
                 approved_urls: set[str] | None = None) -> list[TrendDecision]:
    verified_urls = verified_urls or set()
    approved_urls = approved_urls or set()
    seen = set()
    decisions = []
    for candidate in candidates:
        candidate.validate()
        if candidate.source_url in seen:
            continue
        seen.add(candidate.source_url)
        decisions.append(decide_trend(candidate,
            rights_verified=candidate.source_url in verified_urls,
            approved=candidate.source_url in approved_urls))
    return decisions
