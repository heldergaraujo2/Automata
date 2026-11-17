"""Explicitly approved media acquisition with strict URL and size checks.

No download unless allow_network=True. This is not a legal license verifier.
"""
import hashlib
import ipaddress
import json
import socket
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

MAX_BYTES = 100 * 1024 * 1024
EXTENSIONS = {"image": {".jpg", ".jpeg", ".png", ".webp"}, "video": {".mp4", ".webm", ".ogv"}}

@dataclass(frozen=True)
class ApprovedMedia:
    asset_id: str
    scene_key: str
    kind: str
    source_url: str
    source_page: str
    license_reference: str
    attribution: str
    reviewed_by: str
    approved_for_commercial_use: bool
    product_id: str = ""

def validate_approval(item: ApprovedMedia) -> None:
    if item.kind not in EXTENSIONS:
        raise ValueError("Tipo de mídia não suportado")
    if not all((item.asset_id.strip(), item.scene_key.strip(), item.source_page.strip(),
                item.license_reference.strip(), item.attribution.strip(), item.reviewed_by.strip())):
        raise ValueError("Evidência de licença, atribuição e revisor obrigatórios")
    if not item.approved_for_commercial_use:
        raise PermissionError("Uso comercial não aprovado")
    for url in (item.source_url, item.source_page, item.license_reference):
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("URL HTTPS inválida")
    if item.product_id and item.kind not in EXTENSIONS:
        raise ValueError("Mídia de produto inválida")

def _public_host(url: str) -> bool:
    hostname = urlparse(url).hostname
    if not hostname:
        return False
    try:
        addresses = socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)
        return bool(addresses) and all(ipaddress.ip_address(a[4][0]).is_global for a in addresses)
    except (OSError, ValueError):
        return False

class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirecionamento de download não permitido")

def acquire_media(item: ApprovedMedia, destination: Path, *,
                  allow_network: bool = False, max_bytes: int = MAX_BYTES) -> dict:
    validate_approval(item)
    if not allow_network:
        raise PermissionError("Download desabilitado até a etapa final de testes")
    if destination.suffix.lower() not in EXTENSIONS[item.kind]:
        raise ValueError("Extensão de destino incompatível")
    if not 0 < max_bytes <= MAX_BYTES:
        raise ValueError("Limite de download inválido")
    if not _public_host(item.source_url):
        raise ValueError("Destino de rede não público ou indisponível")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".part")
    digest = hashlib.sha256()
    total = 0
    try:
        opener = build_opener(NoRedirects())
        request = Request(item.source_url, headers={"User-Agent": "AutomataMediaPrototype/0.1"})
        with opener.open(request, timeout=30) as response, temporary.open("wb") as handle:
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                raise ValueError("Arquivo excede limite")
            while True:
                chunk = response.read(min(65536, max_bytes - total + 1))
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("Arquivo excede limite")
                digest.update(chunk)
                handle.write(chunk)
        if not total:
            raise ValueError("Arquivo vazio")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return {"asset_id": item.asset_id, "path": str(destination), "sha256": digest.hexdigest(),
            "size_bytes": total, "license_reference": item.license_reference,
            "attribution": item.attribution, "reviewed_by": item.reviewed_by,
            "source_page": item.source_page, "status": "downloaded_pending_content_validation"}

def load_approvals(path: Path) -> list[ApprovedMedia]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Lista JSON de aprovações esperada")
    return [ApprovedMedia(**record) for record in raw]
