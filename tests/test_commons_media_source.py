import unittest
from automata.commons_media_source import parse_commons_response, search_commons

class CommonsSourceTests(unittest.TestCase):
    def test_parse_requires_manual_license_review(self):
        response = {"query": {"pages": [{"pageid": 42, "imageinfo": [{
            "mime": "image/jpeg", "url": "https://upload.wikimedia.org/test.jpg",
            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Test.jpg",
            "extmetadata": {"LicenseShortName": {"value": "CC BY-SA 4.0"}}}]}]}}
        items = parse_commons_response(response, "kitchen")
        self.assertEqual(len(items), 1)
        self.assertFalse(items[0]["authorized_for_reuse"])
        self.assertEqual(items[0]["review_status"], "needs_license_and_attribution_review")

    def test_network_disabled(self):
        with self.assertRaises(PermissionError):
            search_commons("coffee", "kitchen")

if __name__ == "__main__":
    unittest.main()
