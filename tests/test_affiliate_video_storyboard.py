import json
import tempfile
import unittest
from pathlib import Path
from automata.affiliate_video_storyboard import create_storyboard, export_storyboards

class StoryboardTests(unittest.TestCase):
    def setUp(self):
        self.campaign = {"product_id": "MLB-DEMO", "channel": "tiktok",
                         "affiliate_url": "https://example.org/ref",
                         "caption": "Publicidade | Link de afiliado",
                         "status": "pending_review"}

    def test_scene_duration_and_rights(self):
        result = create_storyboard(self.campaign)
        self.assertEqual(sum(scene.seconds for scene in result.scenes), result.duration_seconds)
        self.assertLessEqual(result.duration_seconds, 60)
        self.assertTrue(all(scene.rights_requirement for scene in result.scenes))
        self.assertEqual(result.status, "awaiting_media_and_voice")

    def test_export(self):
        with tempfile.TemporaryDirectory() as temp:
            src, dst = Path(temp) / "in.json", Path(temp) / "out.json"
            src.write_text(json.dumps([self.campaign]), encoding="utf-8")
            self.assertEqual(export_storyboards(src, dst), 1)
            self.assertEqual(len(json.loads(dst.read_text(encoding="utf-8"))), 1)

    def test_unreviewed_blocked(self):
        with self.assertRaises(PermissionError):
            create_storyboard({**self.campaign, "status": "published"})

if __name__ == "__main__":
    unittest.main()
