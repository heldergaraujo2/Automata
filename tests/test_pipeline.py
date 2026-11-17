import json
import tempfile
import unittest
from pathlib import Path
from automata.pipeline import run
from automata.rights import authorized_media
from automata.core import Offer

class PipelineTests(unittest.TestCase):
    def test_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "offers.json"
            catalog.write_text(json.dumps([{
                "id": "demo1", "title": "Mouse", "price_brl": 99.9,
                "affiliate_url": "https://example.com/affiliate/demo",
                "source": "demo", "description": "Mouse sem fio"
            }]), encoding="utf-8")
            paths = run(catalog, root / "drafts")
            self.assertEqual(len(paths), 1)
            draft = json.loads(paths[0].read_text(encoding="utf-8"))
            self.assertEqual(draft["status"], "pending_review")
            self.assertIn("Publicidade", draft["caption"])

    def test_rights_gate(self):
        o = Offer("1", "Produto", 10, "https://example.com", "demo", "Descrição")
        self.assertFalse(authorized_media(o))

if __name__ == "__main__":
    unittest.main()
