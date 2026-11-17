import argparse
from pathlib import Path
from .pipeline import run

p = argparse.ArgumentParser()
p.add_argument("--catalog", type=Path, required=True)
p.add_argument("--output", type=Path, default=Path("output/drafts"))
args = p.parse_args()
for path in run(args.catalog, args.output):
    print(path)
