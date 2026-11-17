import json
import tempfile
import unittest
from pathlib import Path
from automata.viral_feed import build_review_queue

class ViralFeedTests(unittest.TestCase):
    def test_only_authorized_media_enters_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            feed = root / "feed.json"
            feed.write_text(json.dumps([
                {"source_url": "https://example.org/a", "creator_handle": "@a",
                 "views": 100, "likes": 20, "license_evidence": "written permission",
                 "licensed_media_url": "https://example.org/a.mp4"},
                {"source_url": "https://example.org/b", "creator_handle": "@b",
                 "views": 200, "likes": 80}
            ]), encoding="utf-8")
            output = root / "queue.json"
            result = build_review_queue(feed, output, approved_sources={"https://example.org/a"})
            self.assertEqual(result, {"discovered": 2, "review_ready": 1, "blocked": 1})
            queue = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(queue[0]["creator"], "@a")
            self.assertEqual(queue[0]["status"], "ready_for_manual_review")

if __name__ == "__main__":
    unittest.main()
