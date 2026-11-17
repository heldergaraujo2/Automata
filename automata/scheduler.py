"""Deterministic local scheduler for approved draft jobs; no external side effects."""
import json
from datetime import datetime, timezone
from pathlib import Path

def due_drafts(directory: Path, now: datetime | None = None) -> list[Path]:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone aware")
    result = []
    for path in sorted(directory.glob("*.json")) if directory.exists() else []:
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("status") != "approved":
            continue
        schedule = record.get("scheduled_at")
        if not schedule:
            continue
        when = datetime.fromisoformat(schedule.replace("Z", "+00:00"))
        if when.tzinfo is None:
            raise ValueError(f"scheduled_at must include timezone: {path}")
        if when <= now:
            result.append(path)
    return result
