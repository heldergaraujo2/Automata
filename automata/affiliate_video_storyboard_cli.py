"""Prepare offline affiliate video storyboard JSON files."""
import argparse
from pathlib import Path
from .affiliate_video_storyboard import export_storyboards

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("output/affiliate_campaigns.json"))
    parser.add_argument("--output", type=Path, default=Path("output/affiliate_storyboards.json"))
    args = parser.parse_args()
    print(f"Roteiros preparados: {export_storyboards(args.input, args.output)}")

if __name__ == "__main__":
    main()
