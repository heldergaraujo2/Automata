"""Offline affiliate commission reconciliation from explicitly supplied reports.

No API, login, payment, or real commission verification. Monetary math uses Decimal.
"""
import csv
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

VALID_STATUSES = {"pending", "approved", "paid", "cancelled", "refunded"}

@dataclass(frozen=True)
class CommissionEntry:
    program: str
    transaction_id: str
    product_id: str
    campaign_tag: str
    status: str
    sale_amount_brl: str
    commission_amount_brl: str
    occurred_at: str

def money(value: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Valor monetário inválido") from None
    if not result.is_finite() or result < 0 or result.as_tuple().exponent < -2:
        raise ValueError("Valor monetário deve ser não negativo e ter até duas casas")
    return result

def parse_entry(row: dict) -> CommissionEntry:
    entry = CommissionEntry(**{key: row[key] for key in CommissionEntry.__dataclass_fields__})
    if entry.program not in {"mercado_livre", "magalu", "pichau", "tiktok_shop"}:
        raise ValueError("Programa inválido")
    if entry.status not in VALID_STATUSES:
        raise ValueError("Status inválido")
    if not all((entry.transaction_id.strip(), entry.product_id.strip(), entry.occurred_at.strip())):
        raise ValueError("Identificador, produto e data obrigatórios")
    money(entry.sale_amount_brl)
    money(entry.commission_amount_brl)
    return entry

def import_commission_csv(source: Path, destination: Path) -> dict:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        entries = [parse_entry(row) for row in csv.DictReader(handle)]
    seen = set()
    for entry in entries:
        key = (entry.program, entry.transaction_id)
        if key in seen:
            raise ValueError("Transação duplicada no relatório")
        seen.add(key)
    totals = defaultdict(lambda: {"transactions": 0, "commission_brl": Decimal("0.00")})
    by_status = defaultdict(lambda: Decimal("0.00"))
    for entry in entries:
        totals[entry.status]["transactions"] += 1
        totals[entry.status]["commission_brl"] += money(entry.commission_amount_brl)
        by_status[entry.status] += money(entry.commission_amount_brl)
    report = {
        "source_type": "operator_supplied_csv",
        "verified_by_partner": False,
        "transactions": [asdict(e) for e in entries],
        "summary_by_status": {
            status: {"transactions": value["transactions"],
                     "commission_brl": str(value["commission_brl"].quantize(Decimal("0.01")))}
            for status, value in sorted(totals.items())
        },
        "paid_commission_brl": str(by_status["paid"].quantize(Decimal("0.01"))),
        "note": "Valores importados do arquivo; confirmação depende do parceiro."
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"transactions": len(entries), "paid_commission_brl": report["paid_commission_brl"]}
