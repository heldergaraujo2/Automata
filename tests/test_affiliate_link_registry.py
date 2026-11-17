import json
import tempfile
import unittest
from pathlib import Path
from automata.affiliate_link_registry import merge_verified_links

class AffiliateLinkRegistryTests(unittest.TestCase):
    def test_only_operator_confirmed_link_is_merged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            leads, evidence, output = (root / x for x in ("leads.json", "evidence.json", "out.json"))
            leads.write_text(json.dumps([{"program": "mercado_livre", "product_id": "1",
                                          "affiliate_url": ""}]), encoding="utf-8")
            entry = {"program": "mercado_livre", "product_id": "1",
                     "affiliate_url": "https://example.org/ref",
                     "obtained_via": "official affiliate panel",
                     "evidence_reference": "operator reference", "verified_at": "2026-11-17",
                     "confirmed_by_operator": False}
            evidence.write_text(json.dumps([entry]), encoding="utf-8")
            self.assertEqual(merge_verified_links(leads, evidence, output)["operator_attested_links"], 0)
            entry["confirmed_by_operator"] = True
            evidence.write_text(json.dumps([entry]), encoding="utf-8")
            self.assertEqual(merge_verified_links(leads, evidence, output)["operator_attested_links"], 1)
            self.assertEqual(json.loads(output.read_text())[0]["affiliate_url"], "https://example.org/ref")

if __name__ == "__main__":
    unittest.main()
