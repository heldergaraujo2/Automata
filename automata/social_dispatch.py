"""Dry-run preparation of approved, due posts for three official platforms."""
import json
from pathlib import Path
from urllib.parse import urlparse
from .scheduler import due_drafts
from .social_api import get_adapter
from .social_connectors import SocialAccount, SocialPost
from .media_hosting import validate_hosted_url

def prepare_due_posts(directory: Path, accounts: list[SocialAccount],
                      hosted_urls: dict[str, str]) -> list[dict[str, str]]:
    jobs = []
    for draft_path in due_drafts(directory):
        draft = json.loads(draft_path.read_text(encoding="utf-8"))
        if draft.get("rights_verified") is not True:
            continue
        hosted_url = hosted_urls.get(draft_path.stem)
        if not hosted_url:
            continue
        validate_hosted_url(hosted_url)
        for account in accounts:
            if account.platform not in draft.get("platforms", []):
                continue
            post = SocialPost(draft["caption"], hosted_url, True, True)
            prepared = get_adapter(account.platform).prepare(account, post)
            jobs.append({"draft": draft_path.name, **prepared,
                         "status": "dry_run_ready"})
    return jobs
