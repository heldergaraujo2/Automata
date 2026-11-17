"""Offline import and review queue for authorized viral trend feeds."""
import argparse
import json
from pathlib import Path
from .viral_feed import build_review_queue

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed", required=True, type=Path)
    parser.add_argument("--approved-sources", required=True, type=Path,
                        help="JSON list of source URLs explicitly approved for review")
    parser.add_argument("--output", type=Path, default=Path("output/viral_review.json"))
    args = parser.parse_args()
    approved = json.loads(args.approved_sources.read_text(encoding="utf-8"))
    if not isinstance(approved, list) or not all(isinstance(x, str) for x in approved):
        raise ValueError("Lista de URLs aprovadas inválida")
    print(json.dumps(build_review_queue(args.feed, args.output, approved_sources=set(approved))))

if __name__ == "__main__":
    main()
