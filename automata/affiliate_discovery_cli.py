"""Classify a permitted offline catalog export before generating campaigns."""
import argparse
import json
from pathlib import Path
from .affiliate_discovery import import_leads

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("output/affiliate_leads.json"))
    a = p.parse_args()
    print(json.dumps(import_leads(a.input, a.output), ensure_ascii=False))

if __name__ == "__main__":
    main()
