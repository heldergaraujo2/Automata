import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from automata.scheduler import due_drafts
from automata.video_queue import queue_video, approve_and_schedule

class VideoQueueTests(unittest.TestCase):
    def test_review_then_due(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            video = root / "demo.mp4"
            video.write_bytes(b"placeholder")
            draft = queue_video(video, "Publicidade: link de afiliado", root / "drafts",
                                rights_verified=True)
            self.assertEqual(due_drafts(root / "drafts"), [])
            with self.assertRaises(PermissionError):
                approve_and_schedule(draft, "2026-11-17T12:00:00-03:00",
                                     approval_confirmed=False)
            approve_and_schedule(draft, "2026-11-17T12:00:00-03:00",
                                 approval_confirmed=True)
            self.assertEqual(due_drafts(root / "drafts",
                             datetime(2026, 11, 17, 16, tzinfo=timezone.utc)), [draft])
            self.assertEqual(json.loads(draft.read_text())["status"], "approved")

    def test_rights_required(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            video = root / "demo.mp4"
            video.write_bytes(b"placeholder")
            with self.assertRaises(PermissionError):
                queue_video(video, "Legenda", root / "drafts", rights_verified=False)

if __name__ == "__main__":
    unittest.main()
