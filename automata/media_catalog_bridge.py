"""Bridge inspected local media into the reuse-first catalog.

Only explicitly reviewed, content-inspected and license-approved records
become eligible. Never downloads, searches, renders, or publishes.
"""
import json
from dataclasses import dataclass
from pathlib import Path
from .media_reuse_policy import MediaAsset, plan_media

@dataclass(frozen=True)
class InspectedMedia:
    asset_id: str
    scene_key: str
    kind: str
    local_path: str
    sha256: str
    source_page: str
    license_reference: str
    attribution: str
    reviewed_by: str
    approved_for_commercial_use: bool
    content_verified: bool
    product_id: str = ""

def approved_asset(record: InspectedMedia) -> MediaAsset:
    if record.kind not in {"image", "video"}:
        raise ValueError("Tipo inválido")
    required = (record.asset_id, record.scene_key, record.local_path, record.sha256,
                record.source_page, record.license_reference, record.attribution,
                record.reviewed_by)
    if not all(isinstance(v, str) and v.strip() for v in required):
        raise ValueError("Evidências incompletas")
    if len(record.sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in record.sha256):
        raise ValueError("SHA-256 inválido")
    if not record.approved_for_commercial_use or not record.content_verified:
        raise PermissionError("Licença e conteúdo precisam de aprovação")
    # File existence and hash matching are intentionally deferred to final
    # execution-phase verification; this is a catalog planning record only.
    return MediaAsset(record.asset_id, record.scene_key, record.kind,
                      record.local_path, True, record.source_page, record.product_id)

def build_catalog(records: list[InspectedMedia]) -> dict:
    assets, rejected, seen = [], [], set()
    for record in records:
        if record.asset_id in seen:
            rejected.append({"asset_id": record.asset_id, "reason": "duplicate"})
            continue
        seen.add(record.asset_id)
        try:
            assets.append(approved_asset(record))
        except (ValueError, PermissionError) as exc:
            rejected.append({"asset_id": record.asset_id, "reason": str(exc)})
    return {"assets": assets, "rejected": rejected}

def create_media_plan(records_path: Path, scenes_path: Path, output_path: Path) -> dict:
    raw = json.loads(records_path.read_text(encoding="utf-8"))
    scenes = json.loads(scenes_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list) or not isinstance(scenes, list):
        raise ValueError("Registros e cenas devem ser listas")
    records = [InspectedMedia(**item) for item in raw]
    catalog = build_catalog(records)
    decisions = plan_media(scenes, catalog["assets"])
    result = {
        "status": "planning_only_files_not_verified",
        "approved_catalog_count": len(catalog["assets"]),
        "rejected": catalog["rejected"],
        "media_decisions": decisions,
        "attributions": [
            {"asset_id": r.asset_id, "attribution": r.attribution,
             "license_reference": r.license_reference, "source_page": r.source_page}
            for r in records if any(a.asset_id == r.asset_id for a in catalog["assets"])
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
