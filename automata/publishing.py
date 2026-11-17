import json
from dataclasses import asdict
from pathlib import Path
from .core import Draft

def queue_draft(draft: Draft, directory: Path) -> Path:
    if draft.status != "pending_review":
        raise ValueError("Somente rascunhos aguardando revisão")
    directory.mkdir(parents=True, exist_ok=True)
    safe_id = "".join(c for c in draft.offer_id if c.isalnum() or c in "-_")
    if not safe_id:
        raise ValueError("ID inválido")
    target = directory / f"{safe_id}.json"
    target.write_text(json.dumps(asdict(draft), ensure_ascii=False, indent=2), encoding="utf-8")
    return target
