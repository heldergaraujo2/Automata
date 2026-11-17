"""Local ledger for approved commissions and real expenses."""
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

def summarize_ledger(path: Path) -> dict[str, str]:
    revenue = Decimal("0")
    expenses = Decimal("0")
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                amount = Decimal(row["amount_brl"])
            except (InvalidOperation, KeyError) as exc:
                raise ValueError("Valor inválido no ledger") from exc
            if not amount.is_finite() or amount < 0:
                raise ValueError("Valores devem ser finitos e não negativos")
            if row.get("type") == "commission" and row.get("status") == "approved":
                revenue += amount
            elif row.get("type") == "expense":
                expenses += amount
    return {"approved_commissions_brl": str(revenue),
            "expenses_brl": str(expenses), "net_brl": str(revenue - expenses)}
