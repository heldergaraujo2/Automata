"""Single-shot CLI for orchestrated draft cycles (not a background daemon)."""
import argparse
from pathlib import Path
from .orchestrator import run_cycle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/drafts"))
    parser.add_argument("--audit", type=Path, default=Path("logs/audit.jsonl"))
    args = parser.parse_args()
    counts = run_cycle(args.catalog, args.output, args.audit)
    print(f"Rascunhos: {counts['queued']}; falhas: {counts['failed']}")
    if counts["failed"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
