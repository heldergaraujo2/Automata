"""Official social API adapter boundary, intentionally disabled until configured."""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class PublishResult:
    platform: str
    external_post_id: str

class SocialPublisher(Protocol):
    def publish(self, caption: str, video_path: str) -> PublishResult: ...

class DisabledPublisher:
    def publish(self, caption: str, video_path: str) -> PublishResult:
        raise RuntimeError("Publicação desativada: conecte API oficial, permissões e aprovação")
