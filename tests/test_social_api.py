import unittest
from automata.social_api import get_adapter
from automata.social_connectors import SocialAccount, SocialPost

class SocialAPITests(unittest.TestCase):
    def test_all_adapters_prepare(self):
        for platform in ("instagram", "facebook", "tiktok"):
            adapter = get_adapter(platform)
            account = SocialAccount(platform, "account", "AUTOMATA_TOKEN", enabled=True)
            post = SocialPost("Publicidade: link de afiliado", "https://example.org/video.mp4", True, True)
            self.assertEqual(adapter.prepare(account, post)["platform"], platform)
            with self.assertRaises(NotImplementedError):
                adapter.publish(account, post)

    def test_wrong_account_blocked(self):
        adapter = get_adapter("tiktok")
        account = SocialAccount("facebook", "account", "AUTOMATA_TOKEN", enabled=True)
        post = SocialPost("Publicidade: link de afiliado", "https://example.org/video.mp4", True, True)
        with self.assertRaises(ValueError):
            adapter.prepare(account, post)

if __name__ == "__main__":
    unittest.main()
