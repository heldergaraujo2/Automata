import unittest
from automata.affiliate_only import AffiliateItem, prepare_affiliate_promotion, estimated_commission

class AffiliateOnlyTests(unittest.TestCase):
    def test_mercado_livre_affiliate(self):
        item = AffiliateItem("a", "mercado_livre", "Produto", "Dados confirmados",
                             "https://example.org/ref", 100.0, 0.05)
        draft = prepare_affiliate_promotion(item, "tiktok")
        self.assertEqual(draft["status"], "pending_review")
        self.assertIn("Publicidade", draft["caption"])
        self.assertEqual(estimated_commission(item), 5.0)

    def test_no_seller_listing(self):
        item = AffiliateItem("a", "magalu", "Produto", "Dados confirmados",
                             "https://example.org/ref", 100.0)
        with self.assertRaises(ValueError):
            prepare_affiliate_promotion(item, "mercado_livre")

    def test_no_invented_commission(self):
        item = AffiliateItem("a", "pichau", "Produto", "Dados confirmados",
                             "https://example.org/ref", 100.0)
        self.assertIsNone(estimated_commission(item))

if __name__ == "__main__":
    unittest.main()
