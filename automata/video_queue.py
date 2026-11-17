"""Queue completed local videos for review; scheduling requires explicit approval."""
import json
import re
from datetime import datetime
from pathlib import Path

def queue_video(video: Path, caption: str, destination: Path, *,
                rights_verified: bool, source_url: str = "") -> Path:
    if not rights_verified:
        raise PermissionError("Direitos de mídia não confirmados")
    if not video.is_file() or video.suffix.lower() != ".mp4":
        raise ValueError("Arquivo MP4 finalizado obrigatório")
    if not caption.strip():
        raise ValueError("Legenda obrigatória")
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / (re.sub(r"[^a-zA-Z0-9_-]", "_", video.stem) + ".json")
    if target.exists():
        raise FileExistsError("Rascunho já existe; revisão manual necessária")
    record = {
        "video_path": str(video.resolve()), "caption": caption,
        "source_url": source_url, "rights_verified": True,
        "status": "pending_review", "scheduled_at": None,
        "platforms": ["instagram", "facebook", "tiktok"],
    }
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return target

def approve_and_schedule(path: Path, scheduled_at: str, *,
                         approval_confirmed: bool) -> None:
    if not approval_confirmed:
        raise PermissionError("Aprovação explícita necessária")
    when = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
    if when.tzinfo is None:
        raise ValueError("Data precisa conter fuso horário")
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("status") != "pending_review" or record.get("rights_verified") is not True:
        raise PermissionError("Rascunho não elegível")
    if not Path(record["video_path"]).is_file():
        raise FileNotFoundError("Vídeo não encontrado")
    record["status"] = "approved"
    record["scheduled_at"] = when.isoformat()
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
