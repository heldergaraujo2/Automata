import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from automata.affiliate_video_pipeline import make_brief, export_briefs, render_and_queue
from automata.trend_production import ProductionAssets

class AffiliateVideoPipelineTests(unittest.TestCase):
    def setUp(self):
        self.campaign = {
            "product_id": "MLB-1", "channel": "tiktok",
            "caption": "Publicidade | Link de afiliado: https://example.org/ref",
            "affiliate_url": "https://example.org/ref", "status": "pending_review"}

    def test_campaign_to_brief(self):
        brief = make_brief(self.campaign)
        self.assertEqual(brief.channel, "tiktok")
        self.assertEqual(brief.status, "awaiting_media")

    def test_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src, dst = root / "campaigns.json", root / "briefs.json"
            src.write_text(json.dumps([self.campaign]), encoding="utf-8")
            self.assertEqual(export_briefs(src, dst), 1)
            self.assertEqual(len(json.loads(dst.read_text(encoding="utf-8"))), 1)

    @patch("automata.affiliate_video_pipeline.render_vertical")
    def test_render_to_review_queue(self, mocked):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "final.mp4"
            output.write_bytes(b"placeholder")
            mocked.return_value = output
            brief = make_brief(self.campaign)
            assets = ProductionAssets(root / "top.mp4", root / "product.mp4", True, True)
            queued = render_and_queue(brief, assets, output, root / "drafts")
            self.assertTrue(queued.is_file())
            self.assertEqual(json.loads(queued.read_text())["status"], "pending_review")

    def test_rights_block(self):
        brief = make_brief(self.campaign)
        with self.assertRaises(PermissionError):
            render_and_queue(brief, ProductionAssets(Path("a"), Path("b"), False, True),
                             Path("out.mp4"), Path("drafts"))

if __name__ == "__main__":
    unittest.main()
