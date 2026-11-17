import unittest
from automata.commerce_channels import CommerceProduct, create_commerce_draft

class CommerceChannelTests(unittest.TestCase):
    def setUp(self):
        self.product = CommerceProduct(
            "p1", "magalu", "Monitor exemplo", "Tela de 24 polegadas",
            799.0, "https://example.org/product", "https://example.org/affiliate",
            ("24 polegadas",))

    def test_affiliate_social_is_review_only(self):
        draft = create_commerce_draft(self.product, "tiktok")
        self.assertEqual(draft.status, "pending_review")
        self.assertIn("afiliado", draft.description)

    def test_affiliate_marketplace_requires_policy_check(self):
        draft = create_commerce_draft(self.product, "mercado_livre")
        self.assertEqual(draft.status, "needs_channel_policy_check")

    def test_seller_listing_requires_authorization_and_fulfillment(self):
        draft = create_commerce_draft(self.product, "tiktok_shop", "seller_listing")
        self.assertEqual(draft.status, "blocked")

    def test_authorized_seller_listing_is_still_reviewed(self):
        product = CommerceProduct(**{**self.product.__dict__,
            "seller_authorized": True, "inventory_confirmed": True,
            "fulfillment_confirmed": True})
        draft = create_commerce_draft(product, "mercado_livre", "seller_listing")
        self.assertEqual(draft.status, "pending_review")

if __name__ == "__main__":
    unittest.main()
