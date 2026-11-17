import unittest
from automata.media_discovery import MediaCandidate, build_discovery_plan

class MediaDiscoveryTests(unittest.TestCase):
    def test_reuses_licensed_video(self):
        scenes = [{"scene_key": "coffee", "allow_generic_generation": True}]
        candidates = [MediaCandidate("v1", "coffee", "video", "https://example.org/v.mp4",
                                     "licensed_library", "license-123", True, "media/coffee.mp4")]
        result = build_discovery_plan(scenes, candidates)
        self.assertEqual(result["media_decisions"][0]["action"], "reuse")
        self.assertEqual(result["approved_candidates"], 1)

    def test_rejects_unlicensed_and_generates_generic_only(self):
        scenes = [{"scene_key": "coffee", "allow_generic_generation": True},
                  {"scene_key": "product", "is_product_scene": True,
                   "product_id": "p1", "allow_generic_generation": True}]
        candidates = [MediaCandidate("v1", "coffee", "video", "https://example.org/v.mp4", "web")]
        result = build_discovery_plan(scenes, candidates)
        self.assertEqual(result["media_decisions"][0]["action"], "request_generation")
        self.assertEqual(result["media_decisions"][1]["action"], "needs_authorized_product_media")
        self.assertEqual(result["rejected_candidates"][0]["reason"], "rights_not_confirmed")

if __name__ == "__main__":
    unittest.main()
