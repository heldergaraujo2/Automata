"""Prepare offline campaigns from user-authorized Mercado Livre records."""
import argparse
from pathlib import Path
from .mercado_livre_affiliates import export_campaigns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("output/mercado_livre_campaigns.json"))
    args = parser.parse_args()
    print(f"Rascunhos preparados: {export_campaigns(args.input, args.output)}")

if __name__ == "__main__":
    main()
