"""Validate hosting handoff without uploading or exposing local videos."""
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

@dataclass(frozen=True)
class HostingRequest:
    local_video: Path
    rights_verified: bool
    approved: bool

    def validate(self) -> None:
        if not self.local_video.is_file() or self.local_video.suffix.lower() != ".mp4":
            raise ValueError("MP4 local necessário")
        if not self.rights_verified or not self.approved:
            raise PermissionError("Hospedagem exige direitos e aprovação")

def validate_hosted_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("URL pública HTTPS inválida")
    if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("URL local não é acessível pelas redes")
    return url

class DisabledHostingProvider:
    """Production uploads remain disabled until user-authorized PC testing."""
    def upload(self, request: HostingRequest) -> str:
        request.validate()
        raise NotImplementedError("Upload desabilitado até configuração autorizada")
