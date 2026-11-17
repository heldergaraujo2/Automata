"""Single-instance bounded loop. Disabled by default; no social publishing."""
import argparse
import time
from pathlib import Path
from .orchestrator import run_cycle
from .state import connect, start_cycle, finish_cycle

def serve(catalog: Path, output: Path, audit: Path, db_path: Path, interval: int, once: bool = True) -> None:
    if interval < 60:
        raise ValueError("Intervalo mínimo de 60 segundos")
    with connect(db_path) as db:
        while True:
            cycle_id = start_cycle(db)
            try:
                counts = run_cycle(catalog, output, audit)
            except Exception:
                finish_cycle(db, cycle_id, {"queued": 0, "failed": 1}, "failed")
                raise
            finish_cycle(db, cycle_id, counts, "partial_failure" if counts["failed"] else "completed")
            if once:
                break
            time.sleep(interval)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("output/drafts"))
    p.add_argument("--audit", type=Path, default=Path("logs/audit.jsonl"))
    p.add_argument("--db", type=Path, default=Path("output/automata.sqlite3"))
    p.add_argument("--interval", type=int, default=3600)
    p.add_argument("--continuous", action="store_true", help="Repeat cycles until stopped; no publishing")
    args = p.parse_args()
    serve(args.catalog, args.output, args.audit, args.db, args.interval, once=not args.continuous)

if __name__ == "__main__":
    main()
