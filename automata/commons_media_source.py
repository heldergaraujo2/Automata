"""Wikimedia Commons public API search adapter, disabled by default.

Discovery does not grant reuse rights. Each result requires license review,
attribution review, and acquisition before entering the approved catalog.
"""
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://commons.wikimedia.org/w/api.php"
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "video/webm", "video/ogg"}

def parse_commons_response(payload: dict, scene_key: str) -> list[dict]:
    pages = payload.get("query", {}).get("pages", [])
    if isinstance(pages, dict):
        pages = list(pages.values())
    results = []
    for page in pages:
        info = (page.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        if mime not in ALLOWED_MIME:
            continue
        meta = info.get("extmetadata") or {}
        license_name = (meta.get("LicenseShortName") or {}).get("value", "")
        license_url = (meta.get("LicenseUrl") or {}).get("value", "")
        description_page = info.get("descriptionurl", "")
        media_url = info.get("url", "")
        if not (description_page.startswith("https://commons.wikimedia.org/") and media_url.startswith("https://")):
            continue
        results.append({
            "asset_id": "commons-" + str(page.get("pageid", "")),
            "scene_key": scene_key,
            "kind": "video" if mime.startswith("video/") else "image",
            "source_url": media_url,
            "provider": "wikimedia_commons",
            "description_page": description_page,
            "license_name": license_name,
            "license_reference": license_url,
            "attribution_html": (meta.get("Attribution") or {}).get("value", ""),
            "artist_html": (meta.get("Artist") or {}).get("value", ""),
            "authorized_for_reuse": False,
            "local_path": "",
            "review_status": "needs_license_and_attribution_review",
        })
    return results

def search_commons(query: str, scene_key: str, *, limit: int = 10,
                   allow_network: bool = False) -> list[dict]:
    if not allow_network:
        raise PermissionError("Busca online bloqueada até a etapa final autorizada")
    if not query.strip() or not scene_key.strip():
        raise ValueError("Consulta e cena obrigatórias")
    if not 1 <= limit <= 30:
        raise ValueError("Limite deve estar entre 1 e 30")
    params = {
        "action": "query", "format": "json", "formatversion": "2",
        "generator": "search", "gsrsearch": "filetype:bitmap OR filetype:video " + query,
        "gsrnamespace": "6", "gsrlimit": str(limit),
        "prop": "imageinfo", "iiprop": "url|mime|extmetadata",
    }
    url = API_URL + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": "AutomataAffiliatePrototype/0.1 (research; no downloads)"})
    with urlopen(request, timeout=20) as response:
        return parse_commons_response(json.load(response), scene_key)
