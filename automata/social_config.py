"""Load platform account configuration without exposing tokens."""
import json
from pathlib import Path
from .social_connectors import SocialAccount

def load_accounts(path: Path) -> list[SocialAccount]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Configuração deve ser lista JSON")
    accounts = [SocialAccount(**row) for row in payload]
    for account in accounts:
        account.validate()
    if len({(a.platform, a.account_id) for a in accounts}) != len(accounts):
        raise ValueError("Conta duplicada")
    return accounts
