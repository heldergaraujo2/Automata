"""Produce reviewable decisions from a permitted trend-feed JSON export."""
import argparse
import json
from pathlib import Path
from dataclasses import asdict
from .viral_feed import load_feed
from .trend_strategy import route_trends

def _urls(path: Path | None) -> set[str]:
    if path is None:
        return set()
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise ValueError("Esperada lista JSON de URLs")
    return set(value)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed", type=Path, required=True)
    parser.add_argument("--verified-rights", type=Path)
    parser.add_argument("--approved-reposts", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/trend_decisions.json"))
    args = parser.parse_args()
    decisions = route_trends(load_feed(args.feed),
        _urls(args.verified_rights), _urls(args.approved_reposts))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps([asdict(d) for d in decisions],
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"trends": len(decisions),
        "licensed_reposts": sum(d.strategy == "licensed_repost" for d in decisions),
        "original_briefs": sum(d.strategy == "original_content" for d in decisions)}))

if __name__ == "__main__":
    main()
