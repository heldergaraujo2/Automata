import unittest
from automata.social_connectors import SocialAccount, SocialPost, prepare_post

class SocialConnectorsTests(unittest.TestCase):
    def test_all_three_platforms_supported(self):
        for platform in ("instagram", "facebook", "tiktok"):
            account = SocialAccount(platform, "123", "AUTOMATA_TOKEN")
            account.validate()

    def test_unapproved_post_blocked(self):
        account = SocialAccount("instagram", "123", "AUTOMATA_TOKEN", enabled=True)
        post = SocialPost("Publicidade, link de afiliado", "https://example.com/v.mp4", False, True)
        with self.assertRaises(PermissionError):
            prepare_post(account, post)

    def test_disabled_account_blocked(self):
        account = SocialAccount("tiktok", "123", "AUTOMATA_TOKEN")
        post = SocialPost("Publicidade, link de afiliado", "https://example.com/v.mp4", True, True)
        with self.assertRaises(PermissionError):
            prepare_post(account, post)

if __name__ == "__main__":
    unittest.main()
