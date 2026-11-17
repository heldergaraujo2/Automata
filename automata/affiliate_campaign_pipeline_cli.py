"""Offline affiliate discovery-to-campaign bridge."""
import argparse
import json
from pathlib import Path
from .affiliate_campaign_pipeline import build_campaigns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("output/affiliate_leads.json"))
    parser.add_argument("--output", type=Path, default=Path("output/affiliate_campaigns.json"))
    args = parser.parse_args()
    print(json.dumps(build_campaigns(args.input, args.output), ensure_ascii=False))

if __name__ == "__main__":
    main()
