"""Discovery-to-review workflow for licensed viral videos.

Finding a publicly viewable video does not grant download or repost rights.
This module never downloads media or publishes posts.
"""
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass(frozen=True)
class ViralCandidate:
    source_url: str
    creator_handle: str
    views: int
    likes: int
    license_evidence: str = ""
    licensed_media_url: str = ""

    def validate(self) -> None:
        source = urlparse(self.source_url)
        if source.scheme != "https" or not source.netloc:
            raise ValueError("URL de origem inválida")
        if not self.creator_handle.startswith("@") or len(self.creator_handle) < 2:
            raise ValueError("Crédito de criador obrigatório")
        if self.views < 0 or self.likes < 0:
            raise ValueError("Métricas inválidas")

def rank_candidates(candidates: list[ViralCandidate]) -> list[ViralCandidate]:
    for item in candidates:
        item.validate()
    return sorted(candidates, key=lambda c: (c.likes / max(c.views, 1), c.views), reverse=True)

def prepare_repost(candidate: ViralCandidate, *, approved: bool = False) -> dict[str, str]:
    candidate.validate()
    if not approved:
        raise PermissionError("Aprovação explícita necessária")
    if not candidate.license_evidence.strip():
        raise PermissionError("Comprovação de licença ou autorização necessária")
    media = urlparse(candidate.licensed_media_url)
    if media.scheme != "https" or not media.netloc:
        raise PermissionError("Arquivo autorizado precisa de URL HTTPS")
    return {
        "source_url": candidate.source_url,
        "creator": candidate.creator_handle,
        "media_url": candidate.licensed_media_url,
        "caption": f"Créditos ao criador: {candidate.creator_handle}. Fonte: {candidate.source_url}",
        "license_evidence": candidate.license_evidence,
        "status": "ready_for_manual_review",
    }
