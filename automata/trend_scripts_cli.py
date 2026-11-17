"""Convert trend decisions into storyboard drafts, not published videos."""
import argparse
from pathlib import Path
from .trend_scripts import export_plans

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("output/trend_video_plans.json"))
    args = parser.parse_args()
    print(f"Planos preparados: {export_plans(args.decisions, args.output)}")

if __name__ == "__main__":
    main()
