import unittest
from automata.trend_strategy import route_trends
from automata.viral_reposts import ViralCandidate

class TrendStrategyTests(unittest.TestCase):
    def test_unlicensed_trend_becomes_original_brief(self):
        item = ViralCandidate("https://example.org/viral", "@creator", 1000, 100)
        decisions = route_trends([item])
        self.assertEqual(decisions[0].strategy, "original_content")
        self.assertIn("originais", decisions[0].payload["instruction"])

    def test_licensed_and_approved_repost(self):
        item = ViralCandidate("https://example.org/viral", "@creator", 1000, 100,
                              "permission recorded", "https://example.org/licensed.mp4")
        decisions = route_trends([item], {item.source_url}, {item.source_url})
        self.assertEqual(decisions[0].strategy, "licensed_repost")

    def test_unverified_rights_fall_back_to_original(self):
        item = ViralCandidate("https://example.org/viral", "@creator", 1000, 100,
                              "unverified claim", "https://example.org/video.mp4")
        decisions = route_trends([item], set(), {item.source_url})
        self.assertEqual(decisions[0].strategy, "original_content")

    def test_deduplicates_without_discarding_distinct_trends(self):
        a = ViralCandidate("https://example.org/a", "@a", 100, 10)
        b = ViralCandidate("https://example.org/b", "@b", 100, 20)
        self.assertEqual(len(route_trends([a, a, b])), 2)

if __name__ == "__main__":
    unittest.main()
