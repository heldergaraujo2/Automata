import unittest
from automata.media_catalog_bridge import InspectedMedia, build_catalog
from automata.media_reuse_policy import plan_media

class MediaCatalogBridgeTests(unittest.TestCase):
    def record(self, **overrides):
        base = dict(asset_id="asset1", scene_key="coffee", kind="video",
                    local_path="media/coffee.mp4", sha256="a"*64,
                    source_page="https://commons.wikimedia.org/wiki/File:Coffee.webm",
                    license_reference="https://creativecommons.org/licenses/by/4.0/",
                    attribution="Creator", reviewed_by="operator",
                    approved_for_commercial_use=True, content_verified=True)
        base.update(overrides)
        return InspectedMedia(**base)

    def test_reuse_approved_video(self):
        catalog = build_catalog([self.record()])
        decisions = plan_media([{"scene_key": "coffee", "allow_generic_generation": True}], catalog["assets"])
        self.assertEqual(decisions[0]["action"], "reuse")

    def test_uninspected_media_rejected(self):
        result = build_catalog([self.record(content_verified=False)])
        self.assertEqual(len(result["assets"]), 0)

    def test_duplicate_rejected(self):
        result = build_catalog([self.record(), self.record()])
        self.assertEqual(len(result["assets"]), 1)
        self.assertEqual(result["rejected"][0]["reason"], "duplicate")

if __name__ == "__main__":
    unittest.main()
