import csv
import json
import tempfile
import unittest
from pathlib import Path
from automata.affiliate_commissions import import_commission_csv, money

class CommissionTests(unittest.TestCase):
    def test_decimal_money(self):
        self.assertEqual(str(money("0.10") + money("0.20")), "0.30")
        with self.assertRaises(ValueError):
            money("-1")

    def test_import_and_status_separation(self):
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "commissions.csv"
            out = Path(temp) / "summary.json"
            rows = [
                ["mercado_livre", "t1", "p1", "tiktokp1", "pending", "100.00", "5.00", "2026-11-17"],
                ["mercado_livre", "t2", "p2", "instagramp2", "paid", "200.00", "10.00", "2026-11-17"],
                ["mercado_livre", "t3", "p3", "facebookp3", "refunded", "50.00", "2.50", "2026-11-17"]]
            with src.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["program", "transaction_id", "product_id", "campaign_tag",
                                 "status", "sale_amount_brl", "commission_amount_brl", "occurred_at"])
                writer.writerows(rows)
            result = import_commission_csv(src, out)
            self.assertEqual(result["paid_commission_brl"], "10.00")
            report = json.loads(out.read_text(encoding="utf-8"))
            self.assertFalse(report["verified_by_partner"])
            self.assertEqual(report["summary_by_status"]["pending"]["commission_brl"], "5.00")
            self.assertEqual(report["summary_by_status"]["refunded"]["commission_brl"], "2.50")

if __name__ == "__main__":
    unittest.main()
