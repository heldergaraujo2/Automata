import json
import tempfile
import unittest
from pathlib import Path
from automata.visual_media_adapter import plan_visuals, export_visual_plans

class VisualMediaTests(unittest.TestCase):
    def setUp(self):
        self.board = {"product_id": "DEMO-1", "scenes": [
            {"seconds": 6, "visual_direction": "Pessoa preparando mesa"},
            {"seconds": 8, "visual_direction": "Ambiente caseiro"}]}

    def test_plan_requires_rights_review(self):
        result = plan_visuals(self.board)
        self.assertEqual(result.engine, "comfyui")
        self.assertEqual(result.scenes[0].rights_status, "pending_verification")
        self.assertNotIn("DEMO-1", result.scenes[0].prompt)

    def test_export(self):
        with tempfile.TemporaryDirectory() as temp:
            source, dest = Path(temp) / "boards.json", Path(temp) / "plans.json"
            source.write_text(json.dumps([self.board]), encoding="utf-8")
            self.assertEqual(export_visual_plans(source, dest), 1)
            self.assertEqual(len(json.loads(dest.read_text(encoding="utf-8"))), 1)

if __name__ == "__main__":
    unittest.main()
