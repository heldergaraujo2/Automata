import unittest
from pathlib import Path
from unittest.mock import patch
from automata.core import Offer
from automata.media import render_offer

class MediaBridgeTests(unittest.TestCase):
    def test_unlicensed_media_not_rendered(self):
        offer = Offer("demo", "Mouse", 10, "https://example.com/x", "demo", "desc")
        with patch("automata.media.compose") as compose:
            self.assertIsNone(render_offer(offer, Path("output/videos")))
            compose.assert_not_called()

if __name__ == "__main__":
    unittest.main()
