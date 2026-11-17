import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from automata.trend_scripts import VideoPlan
from automata.trend_production import ProductionAssets, render_vertical

class TrendProductionTests(unittest.TestCase):
    def setUp(self):
        self.plan = VideoPlan("https://example.org/t", "original_content",
                              "Original", "Narração", ("Cena 1",), "",
                              "pending_original_media_creation")
        self.assets = ProductionAssets(Path("top.mp4"), Path("product.mp4"), True, True)

    def test_rights_gate(self):
        denied = ProductionAssets(Path("top.mp4"), Path("product.mp4"), False, True)
        with self.assertRaises(PermissionError):
            render_vertical(self.plan, denied, Path("output.mp4"))

    @patch("automata.trend_production.compose")
    def test_ffmpeg_bridge(self, mocked_compose):
        output = Path("output.mp4")
        self.assertEqual(render_vertical(self.plan, self.assets, output), output)
        mocked_compose.assert_called_once_with(Path("top.mp4"), Path("product.mp4"),
                                               output, max_seconds=60.0)

if __name__ == "__main__":
    unittest.main()
