"""Offline visual-media planning for existing ComfyUI and licensed local assets.

No downloads, ComfyUI server calls, or generation occur here.
"""
import json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class VisualScene:
    index: int
    duration_seconds: int
    prompt: str
    negative_prompt: str
    source_kind: str
    rights_status: str = "pending_verification"

@dataclass(frozen=True)
class VisualPlan:
    product_id: str
    engine: str
    scenes: tuple[VisualScene, ...]
    status: str = "awaiting_generation_and_rights_review"

def plan_visuals(storyboard: dict, *, engine: str = "comfyui") -> VisualPlan:
    if engine != "comfyui":
        raise ValueError("Motor visual não suportado")
    if not isinstance(storyboard.get("product_id"), str) or not storyboard["product_id"].strip():
        raise ValueError("ID do produto obrigatório")
    scenes = storyboard.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("Storyboard precisa conter cenas")
    planned = []
    for index, scene in enumerate(scenes, 1):
        duration = scene.get("seconds")
        direction = scene.get("visual_direction")
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duração de cena inválida")
        if not isinstance(direction, str) or not direction.strip():
            raise ValueError("Direção visual obrigatória")
        # Generated imagery must not invent actual product appearance or claims.
        planned.append(VisualScene(
            index, duration,
            "Cinematic original generic lifestyle B-roll, vertical composition, "
            "no brands, no logos, no identifiable real products. " + direction,
            "watermark, trademark, fake product packaging, misleading text",
            "original_generated_background"))
    if sum(item.duration_seconds for item in planned) > 60:
        raise ValueError("Vídeo excede 60 segundos")
    return VisualPlan(storyboard["product_id"], engine, tuple(planned))

def export_visual_plans(storyboards: Path, output: Path) -> int:
    data = json.loads(storyboards.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Esperada lista de storyboards")
    plans = [asdict(plan_visuals(item)) for item in data]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(plans)
