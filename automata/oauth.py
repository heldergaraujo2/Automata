"""OAuth 2.0 PKCE helpers for authorized social account connections.

The callback exchange and provider-specific scope selection must be implemented
and verified against current official API documentation before activation.
"""
import base64
import hashlib
import secrets
from dataclasses import dataclass
from urllib.parse import urlencode, urlparse

@dataclass(frozen=True)
class OAuthProvider:
    name: str
    authorize_url: str
    client_id: str
    redirect_uri: str
    scopes: tuple[str, ...]

    def validate(self) -> None:
        if self.name not in {"instagram", "facebook", "tiktok"}:
            raise ValueError("Provedor desconhecido")
        if not self.client_id or not self.scopes:
            raise ValueError("Client ID e escopos são obrigatórios")
        for url in (self.authorize_url, self.redirect_uri):
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError("OAuth exige URLs HTTPS")

@dataclass(frozen=True)
class AuthorizationRequest:
    url: str
    state: str
    code_verifier: str

def create_authorization_request(provider: OAuthProvider) -> AuthorizationRequest:
    provider.validate()
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ascii")).digest()
    ).rstrip(b"=").decode("ascii")
    query = {
        "response_type": "code", "client_id": provider.client_id,
        "redirect_uri": provider.redirect_uri, "scope": " ".join(provider.scopes),
        "state": state, "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return AuthorizationRequest(
        provider.authorize_url + ("&" if "?" in provider.authorize_url else "?") + urlencode(query),
        state, verifier,
    )

def verify_state(expected: str, returned: str) -> None:
    if not expected or not returned or not secrets.compare_digest(expected, returned):
        raise PermissionError("OAuth state inválido")

def exchange_code(*_args, **_kwargs):
    raise NotImplementedError("Troca de código desativada até configuração e revisão por plataforma")
