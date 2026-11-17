import unittest
from urllib.parse import parse_qs, urlparse
from automata.oauth import OAuthProvider, create_authorization_request, verify_state, exchange_code

class OAuthTests(unittest.TestCase):
    def test_pkce_and_state(self):
        provider = OAuthProvider("tiktok", "https://example.com/authorize", "demo",
                                 "https://example.com/callback", ("scope.demo",))
        request = create_authorization_request(provider)
        params = parse_qs(urlparse(request.url).query)
        self.assertEqual(params["code_challenge_method"], ["S256"])
        self.assertEqual(params["state"], [request.state])
        verify_state(request.state, request.state)
        with self.assertRaises(PermissionError):
            verify_state(request.state, "incorrect")
        with self.assertRaises(NotImplementedError):
            exchange_code("placeholder")

if __name__ == "__main__":
    unittest.main()
