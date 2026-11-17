"""Manual production handoff for approved local assets."""
import argparse
import json
from pathlib import Path
from .trend_scripts import VideoPlan
from .trend_production import ProductionAssets, render_vertical

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--plan", type=Path, required=True, help="JSON file with one VideoPlan")
    p.add_argument("--top", type=Path, required=True)
    p.add_argument("--product", type=Path, required=True)
    p.add_argument("--top-rights-verified", action="store_true")
    p.add_argument("--product-rights-verified", action="store_true")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    data = json.loads(args.plan.read_text(encoding="utf-8"))
    data["scenes"] = tuple(data["scenes"])
    plan = VideoPlan(**data)
    render_vertical(plan, ProductionAssets(args.top, args.product,
                    args.top_rights_verified, args.product_rights_verified), args.output)
    print(f"Vídeo renderizado: {args.output}")

if __name__ == "__main__":
    main()
