import json
import tempfile
import unittest
from pathlib import Path
from automata.affiliate_discovery import ProductLead, assess_lead, import_leads

class AffiliateDiscoveryTests(unittest.TestCase):
    def test_missing_link_is_not_ready(self):
        lead = ProductLead("mercado_livre", "1", "Produto", "https://example.org/item")
        result = assess_lead(lead)
        self.assertEqual(result["status"], "needs_verification")
        self.assertIn("official_affiliate_link", result["missing"])

    def test_complete_offline_lead(self):
        lead = ProductLead("mercado_livre", "1", "Produto", "https://example.org/item",
                           "https://example.org/ref", "Descrição confirmada", 99.0,
                           "Exportação autorizada", "2026-11-17T12:00:00-03:00")
        self.assertEqual(assess_lead(lead)["status"], "ready_for_draft")

    def test_deduplicate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "in.json"
            out = root / "out.json"
            record = {"program": "mercado_livre", "product_id": "1",
                      "title": "Produto", "product_url": "https://example.org/item"}
            src.write_text(json.dumps([record, record]), encoding="utf-8")
            self.assertEqual(import_leads(src, out)["total"], 1)
            self.assertEqual(len(json.loads(out.read_text(encoding="utf-8"))), 1)

if __name__ == "__main__":
    unittest.main()
