import json
import tempfile
import unittest
from pathlib import Path
from automata.mercado_livre_affiliates import MercadoLivreSourceRecord, build_campaign, export_campaigns

class MercadoLivreAffiliateTests(unittest.TestCase):
    def setUp(self):
        self.record = MercadoLivreSourceRecord(
            "MLB-DEMO", "Produto exemplo", "Especificação verificada",
            199.0, "https://example.org/product", "https://example.org/affiliate",
            "registro fornecido pelo operador", "2026-11-17T12:00:00-03:00")

    def test_three_social_drafts(self):
        drafts = build_campaign(self.record)
        self.assertEqual(len(drafts), 3)
        self.assertTrue(all(d["status"] == "pending_review" for d in drafts))
        self.assertTrue(all("afiliado" in d["caption"] for d in drafts))

    def test_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "input.json"
            output = Path(tmp) / "out.json"
            source.write_text(json.dumps([self.record.__dict__]), encoding="utf-8")
            self.assertEqual(export_campaigns(source, output), 3)
            self.assertEqual(len(json.loads(output.read_text(encoding="utf-8"))), 3)

if __name__ == "__main__":
    unittest.main()
