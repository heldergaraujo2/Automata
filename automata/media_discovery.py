"""Normalize discovered media candidates without downloading or claiming usage rights.

Search providers can later supply records from their documented APIs.
Only independently approved candidates enter the reusable media manifest.
"""
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse
from .media_reuse_policy import MediaAsset, plan_media

@dataclass(frozen=True)
class MediaCandidate:
    asset_id: str
    scene_key: str
    kind: str
    source_url: str
    provider: str
    license_reference: str = ""
    authorized_for_reuse: bool = False
    local_path: str = ""
    product_id: str = ""

def _valid_https(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username and not parsed.password

def approve_candidates(candidates: list[MediaCandidate]) -> tuple[list[MediaAsset], list[dict]]:
    approved, rejected = [], []
    seen = set()
    for item in candidates:
        if item.asset_id in seen:
            rejected.append({"asset_id": item.asset_id, "reason": "duplicate_id"})
            continue
        seen.add(item.asset_id)
        if item.kind not in {"video", "image"} or not _valid_https(item.source_url):
            rejected.append({"asset_id": item.asset_id, "reason": "invalid_media_metadata"})
            continue
        if not item.authorized_for_reuse or not item.license_reference.strip():
            rejected.append({"asset_id": item.asset_id, "reason": "rights_not_confirmed"})
            continue
        # Local file existence and authenticity must be verified before rendering.
        if not item.local_path.strip():
            rejected.append({"asset_id": item.asset_id, "reason": "local_media_not_supplied"})
            continue
        approved.append(MediaAsset(item.asset_id, item.scene_key, item.kind,
                                   item.local_path, True, item.provider, item.product_id))
    return approved, rejected

def build_discovery_plan(scenes: list[dict], candidates: list[MediaCandidate]) -> dict:
    approved, rejected = approve_candidates(candidates)
    return {"media_decisions": plan_media(scenes, approved),
            "approved_candidates": len(approved),
            "rejected_candidates": rejected,
            "status": "planning_only_no_downloads"}

def import_discovery_plan(scenes_path: Path, candidates_path: Path, output: Path) -> dict:
    scenes = json.loads(scenes_path.read_text(encoding="utf-8"))
    records = json.loads(candidates_path.read_text(encoding="utf-8"))
    if not isinstance(scenes, list) or not isinstance(records, list):
        raise ValueError("Cenas e candidatos devem ser listas JSON")
    candidates = [MediaCandidate(**record) for record in records]
    report = build_discovery_plan(scenes, candidates)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
