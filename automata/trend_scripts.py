"""Turn trend decisions into original storyboard briefs or licensed repost tasks."""
from dataclasses import asdict, dataclass
from pathlib import Path
import json
from .trend_strategy import TrendDecision

@dataclass(frozen=True)
class VideoPlan:
    source_url: str
    strategy: str
    title: str
    narration: str
    scenes: tuple[str, ...]
    media_url: str
    status: str

def plan_video(decision: TrendDecision) -> VideoPlan:
    if decision.strategy == "licensed_repost":
        media = decision.payload.get("media_url", "")
        if not media.startswith("https://"):
            raise ValueError("Mídia licenciada inválida")
        return VideoPlan(decision.source_url, "licensed_repost",
                         "Repost com créditos", decision.payload["caption"],
                         (), media, "pending_media_verification")
    if decision.strategy != "original_content":
        raise ValueError("Estratégia desconhecida")
    return VideoPlan(
        decision.source_url, "original_content", "Ideia de vídeo original",
        "Você já percebeu esta tendência? Veja nossa abordagem original.",
        ("Abertura: apresentar o tema com imagens próprias.",
         "Desenvolvimento: mostrar um exemplo criado pela equipe.",
         "Encerramento: convite para comentar, sem promessas inventadas."),
        "", "pending_original_media_creation")

def export_plans(decisions_path: Path, output_path: Path) -> int:
    raw = json.loads(decisions_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Lista de decisões esperada")
    plans = [plan_video(TrendDecision(**item)) for item in raw]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps([asdict(p) for p in plans],
                           ensure_ascii=False, indent=2), encoding="utf-8")
    return len(plans)
