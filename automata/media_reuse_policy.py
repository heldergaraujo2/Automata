"""Reuse-first visual asset decisions; no generation, downloads or publishing.

Only approved rights-cleared assets are eligible. AI is last resort for
generic background scenes, never a substitute for real product evidence.
"""
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass(frozen=True)
class MediaAsset:
    asset_id: str
    scene_key: str
    kind: str
    path: str
    rights_verified: bool
    source: str
    product_id: str = ""

def select_media(scene: dict, assets: list[MediaAsset]) -> dict:
    key = str(scene.get("scene_key", "")).strip()
    if not key:
        raise ValueError("scene_key obrigatório")
    is_product = bool(scene.get("is_product_scene", False))
    product_id = str(scene.get("product_id", "")).strip()
    if is_product and not product_id:
        raise ValueError("product_id obrigatório para cena de produto")
    eligible = [
        a for a in assets
        if a.rights_verified and a.scene_key == key
        and a.kind in {"video", "image"}
        and (not is_product or (a.product_id == product_id and a.source != "ai_generated"))
    ]
    # Prefer an already available authorized video over still images.
    eligible.sort(key=lambda a: (a.kind != "video", a.asset_id))
    if eligible:
        asset = eligible[0]
        return {"action": "reuse", "asset_id": asset.asset_id, "path": asset.path,
                "kind": asset.kind, "reason": "authorized_existing_media"}
    if is_product:
        return {"action": "needs_authorized_product_media",
                "reason": "never_generate_fake_product_media"}
    if scene.get("allow_generic_generation") is True:
        return {"action": "request_generation", "reason": "no_approved_existing_media"}
    return {"action": "needs_manual_media", "reason": "generation_not_allowed"}

def plan_media(scenes: list[dict], assets: list[MediaAsset]) -> list[dict]:
    return [{"scene_key": scene.get("scene_key"),
             **select_media(scene, assets)} for scene in scenes]

def load_manifest(path: Path) -> list[MediaAsset]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Manifesto deve ser lista")
    return [MediaAsset(**entry) for entry in raw]
