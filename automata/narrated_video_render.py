"""FFmpeg adapter for adding local Piper WAV and optional SRT to split-screen MP4.

Does not invoke FFmpeg until allow_execution=True in the final local test phase.
"""
from pathlib import Path
import shutil
import subprocess
from media.compose_split import probe_duration

def ffmpeg_subtitle_path(path: Path) -> str:
    # FFmpeg subtitles filter needs escaped path delimiters (especially Windows drive).
    raw = path.resolve().as_posix()
    return raw.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace(",", "\\,")

def render_narrated_video(video: Path, narration_wav: Path, output: Path, *,
                          subtitles_srt: Path | None = None,
                          allow_execution: bool = False) -> Path:
    if not allow_execution:
        raise PermissionError("Renderização reservada para testes locais finais")
    for source in (video, narration_wav):
        if not source.is_file():
            raise FileNotFoundError(source)
    if subtitles_srt is not None and not subtitles_srt.is_file():
        raise FileNotFoundError(subtitles_srt)
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("FFmpeg e ffprobe não disponíveis")
    video_seconds = probe_duration(video)
    voice_seconds = probe_duration(narration_wav)
    if not 0 < video_seconds <= 60:
        raise ValueError("Vídeo precisa ter até 60 segundos")
    if not 0 < voice_seconds <= video_seconds:
        raise ValueError("Narração excede a duração do vídeo")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-hide_banner", "-y", "-i", str(video), "-i", str(narration_wav)]
    if subtitles_srt is not None:
        command += ["-vf", "subtitles='" + ffmpeg_subtitle_path(subtitles_srt) + "'"]
    command += ["-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
                "-preset", "medium", "-crf", "22", "-c:a", "aac", "-b:a", "128k",
                "-t", str(video_seconds), "-movflags", "+faststart", str(output)]
    subprocess.run(command, check=True)
    if not output.is_file():
        raise RuntimeError("Arquivo final não foi produzido")
    return output
