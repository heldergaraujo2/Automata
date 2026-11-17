import unittest
from automata.trends import Trend, rank_trends
from automata.customer_service import reply_to_question
from automata.core import Offer

class AgentTests(unittest.TestCase):
    def test_trend_ranking(self):
        trends = [Trend("a", 100, 5, 0, "https://example.com/a"),
                  Trend("b", 100, 20, 2, "https://example.com/b")]
        self.assertEqual(rank_trends(trends)[0].topic, "b")

    def test_customer_reply_grounded(self):
        offer = Offer("x", "Mouse", 50, "https://example.com/x", "demo", "Sem fio")
        response = reply_to_question(offer, "Tem frete?")
        self.assertIn("consulte", response.lower())
        self.assertIn("afiliado", response.lower())

if __name__ == "__main__":
    unittest.main()
