import unittest
from pathlib import Path
from automata.media_acquisition import ApprovedMedia, acquire_media, validate_approval

class AcquisitionTests(unittest.TestCase):
    def setUp(self):
        self.item = ApprovedMedia("id1", "kitchen", "image",
            "https://upload.wikimedia.org/example.jpg",
            "https://commons.wikimedia.org/wiki/File:Example.jpg",
            "https://creativecommons.org/licenses/by/4.0/",
            "Author attribution", "operator", True)

    def test_approved_but_network_blocked(self):
        validate_approval(self.item)
        with self.assertRaises(PermissionError):
            acquire_media(self.item, Path("out.jpg"))

    def test_unapproved_rejected(self):
        from dataclasses import replace
        with self.assertRaises(PermissionError):
            validate_approval(replace(self.item, approved_for_commercial_use=False))

    def test_missing_evidence_rejected(self):
        from dataclasses import replace
        with self.assertRaises(ValueError):
            validate_approval(replace(self.item, attribution=""))

if __name__ == "__main__":
    unittest.main()
