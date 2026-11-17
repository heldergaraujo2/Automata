import unittest
from automata.media_reuse_policy import MediaAsset, select_media

class MediaReusePolicyTests(unittest.TestCase):
    def test_prefers_licensed_video(self):
        assets = [
            MediaAsset("img", "kitchen", "image", "kitchen.jpg", True, "licensed"),
            MediaAsset("vid", "kitchen", "video", "kitchen.mp4", True, "licensed")]
        self.assertEqual(select_media({"scene_key": "kitchen", "allow_generic_generation": True}, assets)["asset_id"], "vid")

    def test_rejects_unverified(self):
        assets = [MediaAsset("vid", "kitchen", "video", "x.mp4", False, "unknown")]
        self.assertEqual(select_media({"scene_key": "kitchen", "allow_generic_generation": True}, assets)["action"], "request_generation")

    def test_product_never_generated(self):
        self.assertEqual(select_media({"scene_key": "product", "is_product_scene": True,
                                      "product_id": "p1", "allow_generic_generation": True}, [])["action"],
                         "needs_authorized_product_media")

    def test_product_must_match(self):
        assets = [MediaAsset("wrong", "product", "video", "p2.mp4", True, "licensed", "p2")]
        self.assertEqual(select_media({"scene_key": "product", "is_product_scene": True,
                                      "product_id": "p1"}, assets)["action"],
                         "needs_authorized_product_media")

    def test_no_generation_without_opt_in(self):
        self.assertEqual(select_media({"scene_key": "kitchen"}, [])["action"], "needs_manual_media")

if __name__ == "__main__":
    unittest.main()
