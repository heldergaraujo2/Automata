"""Official social publishing connectors: explicit configuration, no browser automation.

These are preparation and validation boundaries. Real API requests are deliberately
not enabled until account permissions, media hosting and provider review are complete.
"""
from dataclasses import dataclass
from urllib.parse import urlparse

SUPPORTED = ("instagram", "facebook", "tiktok")

@dataclass(frozen=True)
class SocialAccount:
    platform: str
    account_id: str
    token_env: str
    enabled: bool = False

    def validate(self) -> None:
        if self.platform not in SUPPORTED:
            raise ValueError("Plataforma não suportada")
        if not self.account_id.strip():
            raise ValueError("ID de conta obrigatório")
        if not self.token_env.startswith("AUTOMATA_"):
            raise ValueError("Nome da variável de token inválido")

@dataclass(frozen=True)
class SocialPost:
    caption: str
    video_url: str
    approved: bool
    rights_confirmed: bool

    def validate(self) -> None:
        url = urlparse(self.video_url)
        if url.scheme != "https" or not url.netloc or url.username or url.password:
            raise ValueError("Vídeo precisa de URL HTTPS acessível pela plataforma")
        if not self.caption.strip() or "afiliad" not in self.caption.lower():
            raise ValueError("Legenda e identificação de afiliado obrigatórias")
        if not self.approved or not self.rights_confirmed:
            raise PermissionError("Publicação exige aprovação e direitos confirmados")

def prepare_post(account: SocialAccount, post: SocialPost) -> dict[str, str]:
    account.validate()
    post.validate()
    if not account.enabled:
        raise PermissionError("Conta desabilitada até autenticação oficial e aprovação")
    return {"platform": account.platform, "account_id": account.account_id,
            "caption": post.caption, "video_url": post.video_url, "status": "ready_for_adapter"}
