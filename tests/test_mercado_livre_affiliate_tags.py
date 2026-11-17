import unittest
from automata.mercado_livre_affiliate_tags import suggest_tag, prepare_tagged_campaign

class MercadoLivreTagTests(unittest.TestCase):
    def test_tag_format(self):
        tag = suggest_tag("MLB-1234_ABC", "tiktok")
        self.assertTrue(tag.isalnum())
        self.assertLessEqual(len(tag), 30)

    def test_requires_portal_assignment(self):
        campaign = {"product_id": "MLB-123", "channel": "instagram",
                    "affiliate_url": "https://example.org/ref",
                    "status": "pending_review"}
        self.assertEqual(prepare_tagged_campaign(campaign).status,
                         "pending_official_tag_assignment")

if __name__ == "__main__":
    unittest.main()
