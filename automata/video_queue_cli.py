"""Manual handoff from rendered MP4 to the existing scheduler's draft format."""
import argparse
from pathlib import Path
from .video_queue import queue_video

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--rights-verified", action="store_true")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--queue", type=Path, default=Path("output/drafts"))
    args = parser.parse_args()
    target = queue_video(args.video, args.caption, args.queue,
                         rights_verified=args.rights_verified,
                         source_url=args.source_url)
    print(f"Rascunho aguardando revisão: {target}")

if __name__ == "__main__":
    main()
