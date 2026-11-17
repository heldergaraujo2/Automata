"""Offline narration adapter for existing Piper TTS (not a new TTS engine).

Plans commands only unless explicitly invoked at a later local test phase.
"""
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class PiperConfig:
    executable: str
    model: Path
    config: Path

def narration_text(storyboard: dict) -> str:
    scenes = storyboard.get("scenes", [])
    if not scenes:
        raise ValueError("Storyboard sem cenas")
    lines = [str(scene["narration"]).strip() for scene in scenes]
    if any(not line for line in lines):
        raise ValueError("Cena sem narração")
    return " ".join(lines)

def piper_command(config: PiperConfig, output: Path) -> list[str]:
    if not config.executable.strip():
        raise ValueError("Executável Piper obrigatório")
    return [config.executable, "--model", str(config.model),
            "--config", str(config.config), "--output_file", str(output)]

def synthesize_piper(text: str, config: PiperConfig, output: Path, *,
                     allow_execution: bool = False) -> Path:
    if not text.strip():
        raise ValueError("Texto vazio")
    if not allow_execution:
        raise PermissionError("Síntese desabilitada até a fase final de testes locais")
    if not config.model.is_file() or not config.config.is_file():
        raise FileNotFoundError("Modelo Piper e configuração necessários")
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(piper_command(config, output), input=text, text=True, check=True)
    if not output.is_file():
        raise RuntimeError("Piper não gerou o arquivo esperado")
    return output

def _stamp(seconds: float) -> str:
    millis = round(seconds * 1000)
    h, remainder = divmod(millis, 3600000)
    m, remainder = divmod(remainder, 60000)
    s, ms = divmod(remainder, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def storyboard_srt(storyboard: dict) -> str:
    """Approximate scene-timed subtitles, NOT audio-aligned word timestamps."""
    scenes = storyboard.get("scenes", [])
    if not scenes:
        raise ValueError("Storyboard sem cenas")
    offset = 0.0
    blocks = []
    for index, scene in enumerate(scenes, 1):
        duration = float(scene["seconds"])
        if duration <= 0:
            raise ValueError("Duração inválida")
        narration = re.sub(r"\s+", " ", scene["narration"]).strip()
        if not narration:
            raise ValueError("Narração vazia")
        blocks.append(f"{index}\n{_stamp(offset)} --> {_stamp(offset + duration)}\n{narration}")
        offset += duration
    if offset > 60:
        raise ValueError("Storyboard ultrapassa 60 segundos")
    return "\n\n".join(blocks) + "\n"

def prepare_narration(storyboard_file: Path, text_file: Path, subtitles_file: Path) -> None:
    storyboard = json.loads(storyboard_file.read_text(encoding="utf-8"))
    text = narration_text(storyboard)
    subtitles = storyboard_srt(storyboard)
    text_file.parent.mkdir(parents=True, exist_ok=True)
    subtitles_file.parent.mkdir(parents=True, exist_ok=True)
    text_file.write_text(text, encoding="utf-8")
    subtitles_file.write_text(subtitles, encoding="utf-8")
