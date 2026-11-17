import json
import tempfile
import unittest
from pathlib import Path
from automata.affiliate_campaign_pipeline import build_campaigns

class AffiliateCampaignPipelineTests(unittest.TestCase):
    def test_complete_lead_creates_three_review_drafts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src, dst = root / "leads.json", root / "campaigns.json"
            complete = {
                "program": "mercado_livre", "product_id": "MLB-1",
                "title": "Monitor exemplo", "product_url": "https://example.org/item",
                "affiliate_url": "https://example.org/ref",
                "verified_description": "Tela de 24 polegadas",
                "price_brl": 499.0, "evidence_source": "registro autorizado",
                "checked_at": "2026-11-17T12:00:00-03:00",
                "status": "ready_for_draft", "missing": []}
            incomplete = {**complete, "product_id": "MLB-2", "affiliate_url": ""}
            src.write_text(json.dumps([complete, complete, incomplete]), encoding="utf-8")
            result = build_campaigns(src, dst)
            self.assertEqual(result, {"unique_products": 2, "blocked_products": 1, "drafts": 3})
            drafts = json.loads(dst.read_text(encoding="utf-8"))
            self.assertEqual({x["channel"] for x in drafts},
                             {"tiktok", "instagram", "facebook"})
            self.assertTrue(all(x["status"] == "pending_review" for x in drafts))

if __name__ == "__main__":
    unittest.main()
