import json
import tempfile
import unittest
from pathlib import Path
from automata.orchestrator import run_cycle

class OrchestratorTests(unittest.TestCase):
    def test_cycle_creates_draft_and_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "offers.json"
            catalog.write_text(json.dumps([{
                "id": "test", "title": "Mouse", "price_brl": 80,
                "affiliate_url": "https://example.com/offer", "source": "example",
                "description": "Mouse sem fio"
            }]), encoding="utf-8")
            result = run_cycle(catalog, root / "drafts", root / "audit.jsonl")
            self.assertEqual(result, {"queued": 1, "failed": 0})
            self.assertTrue((root / "drafts/test.json").is_file())
            self.assertIn('"queued"', (root / "audit.jsonl").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
