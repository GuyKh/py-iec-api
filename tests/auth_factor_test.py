import unittest
from unittest.mock import AsyncMock, patch

from iec_api import login


class AuthFactorTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.factors_response = {
            "stateToken": "token123",
            "_embedded": {
                "factors": [
                    {"id": "f1", "factorType": "email", "profile": {"email": "user@sns.iec.co.il"}},
                    {"id": "f2", "factorType": "email", "profile": {"email": "user@gmail.com"}},
                ]
            },
        }

    @patch("iec_api.commons.send_post_request")
    async def test_get_first_factor_id_prefer_sms(self, mock_post):
        mock_post.return_value = self.factors_response

        # Should pick f1 because it's sms
        state_token, factor_id = await login.get_first_factor_id(AsyncMock(), "123456782", prefer_sms=True)
        self.assertEqual(factor_id, "f1")
        self.assertEqual(state_token, "token123")

    @patch("iec_api.commons.send_post_request")
    async def test_get_first_factor_id_prefer_email(self, mock_post):
        mock_post.return_value = self.factors_response

        # Should pick f2 because it's NOT sms
        state_token, factor_id = await login.get_first_factor_id(AsyncMock(), "123456782", prefer_sms=False)
        self.assertEqual(factor_id, "f2")

    @patch("iec_api.commons.send_post_request")
    async def test_get_first_factor_id_single_factor(self, mock_post):
        single_factor = {
            "stateToken": "token123",
            "_embedded": {"factors": [{"id": "f2", "factorType": "email", "profile": {"email": "user@gmail.com"}}]},
        }
        mock_post.return_value = single_factor

        # Should pick f2 even if sms preferred because it's the only one
        state_token, factor_id = await login.get_first_factor_id(AsyncMock(), "123456782", prefer_sms=True)
        self.assertEqual(factor_id, "f2")

    @patch("iec_api.commons.send_post_request")
    async def test_get_first_factor_id_no_factors(self, mock_post):
        mock_post.return_value = {"stateToken": "token123", "_embedded": {"factors": []}}

        with self.assertRaises(IndexError):
            await login.get_first_factor_id(AsyncMock(), "123456782", prefer_sms=True)

    def test_get_factor_type_sms(self):
        factor = {"factorType": "email", "profile": {"email": "test@sns.iec.co.il"}}
        self.assertEqual(login._get_factor_type(factor), "sms")

    def test_get_factor_type_email(self):
        factor = {"factorType": "email", "profile": {"email": "test@gmail.com"}}
        self.assertEqual(login._get_factor_type(factor), "email")

    def test_select_factor_logic(self):
        factors = [
            {"id": "sms", "factorType": "email", "profile": {"email": "a@sns.iec.co.il"}},
            {"id": "email", "factorType": "email", "profile": {"email": "b@gmail.com"}},
        ]

        self.assertEqual(login._select_factor(factors, prefer_sms=True)["id"], "sms")
        self.assertEqual(login._select_factor(factors, prefer_sms=False)["id"], "email")

        # Reverse order
        factors_rev = [factors[1], factors[0]]
        self.assertEqual(login._select_factor(factors_rev, prefer_sms=True)["id"], "sms")
        self.assertEqual(login._select_factor(factors_rev, prefer_sms=False)["id"], "email")


if __name__ == "__main__":
    unittest.main()
