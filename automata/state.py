"""SQLite run ledger to support restart-safe scheduling and deduplication."""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=15)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("""CREATE TABLE IF NOT EXISTS cycles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        status TEXT NOT NULL,
        queued INTEGER NOT NULL DEFAULT 0,
        failed INTEGER NOT NULL DEFAULT 0
    )""")
    db.commit()
    return db

def start_cycle(db: sqlite3.Connection) -> int:
    stamp = datetime.now(timezone.utc).isoformat()
    cur = db.execute("INSERT INTO cycles(started_at,status) VALUES(?,?)", (stamp, "running"))
    db.commit()
    return int(cur.lastrowid)

def finish_cycle(db: sqlite3.Connection, cycle_id: int, counts: dict[str, int], status: str) -> None:
    if status not in {"completed", "partial_failure", "failed"}:
        raise ValueError("Estado inválido")
    db.execute("UPDATE cycles SET finished_at=?,status=?,queued=?,failed=? WHERE id=?",
               (datetime.now(timezone.utc).isoformat(), status, counts["queued"], counts["failed"], cycle_id))
    db.commit()
