"""Offline CSV-to-JSON affiliate commission report."""
import argparse
import json
from pathlib import Path
from .affiliate_commissions import import_commission_csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("output/affiliate_commissions.json"))
    args = parser.parse_args()
    print(json.dumps(import_commission_csv(args.input, args.output), ensure_ascii=False))

if __name__ == "__main__":
    main()
