"""Conservative provider adapters for official publishing APIs.

No requests are sent unless the caller supplies an explicit HTTPS API endpoint,
a token, an approved post and enables network publishing. Provider-specific
endpoint and permission validation must happen before production use.
"""
from dataclasses import dataclass
from urllib.parse import urlparse
import json
import urllib.request
from .social_connectors import SocialAccount, SocialPost, prepare_post

@dataclass(frozen=True)
class PublishResult:
    platform: str
    status: str
    external_id: str | None = None

class SocialAPIAdapter:
    platform: str

    def __init__(self, platform: str):
        if platform not in ("instagram", "facebook", "tiktok"):
            raise ValueError("Plataforma desconhecida")
        self.platform = platform

    def prepare(self, account: SocialAccount, post: SocialPost) -> dict[str, str]:
        if account.platform != self.platform:
            raise ValueError("Conta pertence a outra plataforma")
        return prepare_post(account, post)

    def publish(self, account: SocialAccount, post: SocialPost) -> PublishResult:
        self.prepare(account, post)
        raise NotImplementedError(
            "Publicação bloqueada: requer fluxo oficial específico, credenciais, "
            "permissões e testes de integração"
        )

class InstagramAdapter(SocialAPIAdapter):
    def __init__(self):
        super().__init__("instagram")

class FacebookAdapter(SocialAPIAdapter):
    def __init__(self):
        super().__init__("facebook")

class TikTokAdapter(SocialAPIAdapter):
    def __init__(self):
        super().__init__("tiktok")

def get_adapter(platform: str) -> SocialAPIAdapter:
    adapters = {"instagram": InstagramAdapter, "facebook": FacebookAdapter,
                "tiktok": TikTokAdapter}
    try:
        return adapters[platform]()
    except KeyError as exc:
        raise ValueError("Plataforma desconhecida") from exc
