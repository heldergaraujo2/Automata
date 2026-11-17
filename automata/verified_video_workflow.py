"""Four-stage opt-in verified-media production and review workflow.

No local execution, network, publication or scheduling unless explicitly enabled.
"""
from dataclasses import dataclass
from pathlib import Path
from .media_render_gate import RenderAsset, validate_render_assets
from .trend_production import ProductionAssets, render_vertical
from .narrated_video_render import render_narrated_video
from .video_queue import queue_video

@dataclass(frozen=True)
class VideoJob:
    top: RenderAsset
    product: RenderAsset
    split_output: Path
    final_output: Path
    caption: str
    review_directory: Path
    narration_wav: Path | None = None
    subtitles_srt: Path | None = None
    source_url: str = ""

def produce_for_review(plan, job: VideoJob, *, allow_execution: bool = False) -> dict:
    if not allow_execution:
        raise PermissionError("Produção e fila bloqueadas até testes finais")
    if job.top.kind != "video" or job.product.kind != "video":
        raise ValueError("A montagem split-screen atual exige dois vídeos; imagens exigem conversão prévia")
    if not job.caption.strip():
        raise ValueError("Legenda da campanha obrigatória")
    if job.final_output.suffix.lower() != ".mp4":
        raise ValueError("Saída final deve ser MP4")
    if job.narration_wav is None and job.subtitles_srt is not None:
        raise ValueError("Legendas exigem narração nesta versão")
    if job.narration_wav is not None and job.split_output == job.final_output:
        raise ValueError("Saídas intermediária e final precisam ser distintas")
    verification = validate_render_assets([job.top, job.product], allow_execution=True)
    assets = ProductionAssets(job.top.path, job.product.path, True, True)
    split_path = job.split_output if job.narration_wav else job.final_output
    render_vertical(plan, assets, split_path)
    if job.narration_wav:
        render_narrated_video(split_path, job.narration_wav, job.final_output,
                              subtitles_srt=job.subtitles_srt, allow_execution=True)
    queued = queue_video(job.final_output, job.caption, job.review_directory,
                         rights_verified=True, source_url=job.source_url)
    return {"status": "pending_review", "video": str(job.final_output),
            "review_record": str(queued), "validated_media": verification}

def planned_job_status(job: VideoJob) -> dict:
    """Describe the next action without touching files or executing programs."""
    return {"status": "awaiting_final_local_execution",
            "stages": ["validate_media", "render_split_screen",
                       "add_optional_narration_and_subtitles", "queue_for_review"],
            "video_output": str(job.final_output), "publishing_enabled": False}
