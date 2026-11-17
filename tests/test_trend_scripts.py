import json
import tempfile
import unittest
from pathlib import Path
from automata.trend_scripts import plan_video, export_plans
from automata.trend_strategy import TrendDecision

class TrendScriptTests(unittest.TestCase):
    def test_original_storyboard(self):
        decision = TrendDecision("https://example.org/a", "@a", "original_content",
                                 "source_media_not_cleared", {"topic_reference": "https://example.org/a"})
        plan = plan_video(decision)
        self.assertEqual(plan.status, "pending_original_media_creation")
        self.assertEqual(len(plan.scenes), 3)
        self.assertEqual(plan.media_url, "")

    def test_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "decisions.json"
            source.write_text(json.dumps([{
                "source_url": "https://example.org/a", "creator_handle": "@a",
                "strategy": "original_content", "reason": "not_cleared",
                "payload": {"topic_reference": "https://example.org/a"}
            }]), encoding="utf-8")
            target = root / "plans.json"
            self.assertEqual(export_plans(source, target), 1)
            self.assertEqual(len(json.loads(target.read_text(encoding="utf-8"))), 1)

if __name__ == "__main__":
    unittest.main()
