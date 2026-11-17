import unittest
from automata.viral_reposts import ViralCandidate, prepare_repost, rank_candidates

class ViralRepostTests(unittest.TestCase):
    def test_rank(self):
        a = ViralCandidate("https://example.com/a", "@a", 100, 5)
        b = ViralCandidate("https://example.com/b", "@b", 100, 30)
        self.assertEqual(rank_candidates([a, b])[0].creator_handle, "@b")

    def test_credit_alone_does_not_authorize(self):
        candidate = ViralCandidate("https://example.com/a", "@creator", 100, 20)
        with self.assertRaises(PermissionError):
            prepare_repost(candidate, approved=True)

    def test_licensed_approved_candidate(self):
        candidate = ViralCandidate("https://example.com/a", "@creator", 100, 20,
                                   "written permission ref 123", "https://example.com/licensed.mp4")
        result = prepare_repost(candidate, approved=True)
        self.assertIn("@creator", result["caption"])
        self.assertEqual(result["status"], "ready_for_manual_review")

if __name__ == "__main__":
    unittest.main()
