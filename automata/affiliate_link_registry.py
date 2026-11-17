"""Local registry of operator-supplied referral links and their provenance.

An unverified URL never becomes a verified affiliate link by heuristic.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
import json

@dataclass(frozen=True)
class ReferralEvidence:
    program: str
    product_id: str
    affiliate_url: str
    obtained_via: str
    evidence_reference: str
    verified_at: str
    confirmed_by_operator: bool = False

def validate_evidence(e: ReferralEvidence) -> None:
    if e.program not in {"mercado_livre", "magalu", "pichau", "tiktok_shop"}:
        raise ValueError("Programa não suportado")
    p = urlparse(e.affiliate_url)
    if p.scheme != "https" or not p.netloc or p.username or p.password:
        raise ValueError("Link HTTPS inválido")
    if not all((e.product_id.strip(), e.obtained_via.strip(),
                e.evidence_reference.strip(), e.verified_at.strip())):
        raise ValueError("Proveniência incompleta")

def merge_verified_links(leads: Path, evidence: Path, output: Path) -> dict[str, int]:
    raw_leads = json.loads(leads.read_text(encoding="utf-8"))
    raw_evidence = json.loads(evidence.read_text(encoding="utf-8"))
    if not isinstance(raw_leads, list) or not isinstance(raw_evidence, list):
        raise ValueError("Arquivos devem conter listas JSON")
    registry = {}
    for item in raw_evidence:
        entry = ReferralEvidence(**item)
        validate_evidence(entry)
        key = (entry.program, entry.product_id)
        if key in registry:
            raise ValueError("Evidência duplicada para produto")
        if entry.confirmed_by_operator:
            registry[key] = entry
    result = []
    matched = 0
    for lead in raw_leads:
        row = dict(lead)
        key = (row.get("program"), row.get("product_id"))
        evidence_entry = registry.get(key)
        if evidence_entry:
            # Do not silently overwrite a different existing referral URL.
            if row.get("affiliate_url") not in ("", None, evidence_entry.affiliate_url):
                raise ValueError(f"Conflito de links para {key}")
            row["affiliate_url"] = evidence_entry.affiliate_url
            row["link_provenance"] = {
                "obtained_via": evidence_entry.obtained_via,
                "evidence_reference": evidence_entry.evidence_reference,
                "verified_at": evidence_entry.verified_at,
                "verification_level": "operator_attested",
            }
            matched += 1
        result.append(row)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"leads": len(result), "operator_attested_links": matched}
