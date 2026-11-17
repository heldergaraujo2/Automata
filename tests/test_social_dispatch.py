import json
import tempfile
import unittest
from pathlib import Path
from automata.media_hosting import validate_hosted_url, DisabledHostingProvider, HostingRequest
from automata.social_dispatch import prepare_due_posts
from automata.social_connectors import SocialAccount

class SocialDispatchTests(unittest.TestCase):
    def test_three_platform_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.json").write_text(json.dumps({
                "status": "approved", "scheduled_at": "2020-01-01T00:00:00+00:00",
                "rights_verified": True, "caption": "Publicidade: link de afiliado",
                "platforms": ["instagram", "facebook", "tiktok"]
            }), encoding="utf-8")
            accounts = [SocialAccount(p, "demo", "AUTOMATA_TOKEN", True)
                        for p in ("instagram", "facebook", "tiktok")]
            jobs = prepare_due_posts(root, accounts, {"sample": "https://cdn.example.org/sample.mp4"})
            self.assertEqual({job["platform"] for job in jobs},
                             {"instagram", "facebook", "tiktok"})
            self.assertTrue(all(job["status"] == "dry_run_ready" for job in jobs))

    def test_no_real_upload(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.mp4"
            path.write_bytes(b"placeholder")
            with self.assertRaises(NotImplementedError):
                DisabledHostingProvider().upload(HostingRequest(path, True, True))
            with self.assertRaises(ValueError):
                validate_hosted_url("http://localhost/video.mp4")

if __name__ == "__main__":
    unittest.main()
