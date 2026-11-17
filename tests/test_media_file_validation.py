import unittest
from pathlib import Path
from automata.media_file_validation import validate_local_media
from automata.media_render_gate import RenderAsset, validate_render_assets

class MediaValidationTests(unittest.TestCase):
    def test_disabled_by_default(self):
        with self.assertRaises(PermissionError):
            validate_local_media(Path("missing.mp4"), "a"*64, "video")
        with self.assertRaises(PermissionError):
            validate_render_assets([RenderAsset(Path("missing.mp4"), "a"*64, "video", True)])
    def test_empty_assets(self):
        with self.assertRaises(ValueError):
            validate_render_assets([], allow_execution=True)
    def test_rights_gate(self):
        with self.assertRaises(PermissionError):
            validate_render_assets([RenderAsset(Path("missing.mp4"), "a"*64, "video", False)], allow_execution=True)

if __name__ == "__main__":
    unittest.main()
