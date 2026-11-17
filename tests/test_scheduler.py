import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from automata.scheduler import due_drafts
from automata.social import DisabledPublisher

class SchedulerTests(unittest.TestCase):
    def test_only_due_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = [
                ("due", {"status": "approved", "scheduled_at": "2026-01-01T00:00:00Z"}),
                ("pending", {"status": "pending_review", "scheduled_at": "2026-01-01T00:00:00Z"}),
                ("future", {"status": "approved", "scheduled_at": "2027-01-01T00:00:00Z"})
            ]
            for name, value in records:
                (root / f"{name}.json").write_text(json.dumps(value), encoding="utf-8")
            found = due_drafts(root, datetime(2026, 11, 17, tzinfo=timezone.utc))
            self.assertEqual([p.stem for p in found], ["due"])

    def test_publishing_requires_integration(self):
        with self.assertRaises(RuntimeError):
            DisabledPublisher().publish("caption", "video.mp4")

if __name__ == "__main__":
    unittest.main()
