"""Block render inputs until license and local file validation succeed."""
from dataclasses import dataclass
from pathlib import Path
from .media_file_validation import validate_local_media

@dataclass(frozen=True)
class RenderAsset:
    path: Path
    expected_sha256: str
    kind: str
    rights_verified: bool

def validate_render_assets(assets: list[RenderAsset], *, allow_execution: bool = False) -> list[dict]:
    if not allow_execution:
        raise PermissionError("Validação bloqueada até a fase final")
    if not assets:
        raise ValueError("Nenhuma mídia informada")
    results = []
    for asset in assets:
        if not asset.rights_verified:
            raise PermissionError("Direitos de uso não aprovados")
        results.append(validate_local_media(asset.path, asset.expected_sha256, asset.kind, allow_execution=True))
    return results
