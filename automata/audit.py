"""Append-only JSONL audit events; never log tokens or private messages."""
import json
from datetime import datetime, timezone
from pathlib import Path

def record_event(path: Path, event: str, offer_id: str, outcome: str) -> None:
    if not all((event.strip(), offer_id.strip(), outcome.strip())):
        raise ValueError("Campos obrigatórios")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "event": event,
               "offer_id": offer_id, "outcome": outcome}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False) + "\n")
