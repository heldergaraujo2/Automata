"""Compose two licensed videos into a simultaneous vertical split-screen MP4."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        check=True, capture_output=True, text=True
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def compose(viral: Path, product: Path, output: Path, max_seconds: float = 60.0) -> None:
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("FFmpeg e ffprobe precisam estar no PATH")
    for path in (viral, product):
        if not path.is_file():
            raise FileNotFoundError(path)
    durations = [probe_duration(viral), probe_duration(product)]
    if any(d <= 0 or d > max_seconds for d in durations):
        raise ValueError(f"Cada vídeo deve ter duração entre 0 e {max_seconds}s: {durations}")
    if abs(durations[0] - durations[1]) > 0.5:
        raise ValueError("Durações diferentes: selecione vídeos compatíveis; não haverá cortes automáticos")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Each half is 1080x960; scale to fill and center crop. Audio comes from the product clip.
    graph = (
        "[0:v]scale=1080:960:force_original_aspect_ratio=increase,"
        "crop=1080:960,setsar=1,format=yuv420p[top];"
        "[1:v]scale=1080:960:force_original_aspect_ratio=increase,"
        "crop=1080:960,setsar=1,format=yuv420p[bottom];"
        "[top][bottom]vstack=inputs=2[v]"
    )
    command = [
        "ffmpeg", "-hide_banner", "-y", "-i", str(viral), "-i", str(product),
        "-filter_complex", graph, "-map", "[v]", "-map", "1:a?",
        "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-r", "30",
        "-c:a", "aac", "-b:a", "128k", "-t", str(min(durations)), "-movflags", "+faststart",
        str(output)
    ]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--viral", type=Path, required=True)
    parser.add_argument("--product", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    compose(args.viral, args.product, args.output)
