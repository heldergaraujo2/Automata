"""Opt-in verification of local media bytes and FFprobe metadata.

No files are read and no subprocesses run unless allow_execution=True.
"""
import hashlib
import json
import subprocess
from pathlib import Path

def validate_local_media(path: Path, expected_sha256: str, kind: str, *,
                         allow_execution: bool = False, max_seconds: float = 60.0) -> dict:
    if not allow_execution:
        raise PermissionError("Validação local bloqueada até a fase final")
    if kind not in {"video", "image"}:
        raise ValueError("Tipo de mídia inválido")
    if len(expected_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in expected_sha256):
        raise ValueError("SHA-256 inválido")
    if not path.is_file():
        raise FileNotFoundError(path)
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != expected_sha256.lower():
        raise ValueError("Hash do arquivo diferente do registrado")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True, timeout=30)
    info = json.loads(result.stdout)
    streams = info.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    if not videos:
        raise ValueError("Arquivo sem imagem ou vídeo decodificável")
    width = int(videos[0].get("width") or 0)
    height = int(videos[0].get("height") or 0)
    if width < 320 or height < 240:
        raise ValueError("Resolução insuficiente")
    if kind == "video":
        duration = float(info.get("format", {}).get("duration") or 0)
        if not 0 < duration <= max_seconds:
            raise ValueError("Duração de vídeo inválida")
    else:
        duration = None
    return {"path": str(path), "sha256": digest.hexdigest(), "kind": kind,
            "width": width, "height": height, "duration_seconds": duration,
            "status": "file_integrity_and_metadata_verified"}
