import unittest
from json import JSONDecodeError
from unittest.mock import AsyncMock, MagicMock

import iec_api.commons
import iec_api.models.exceptions


class CommonsTest(unittest.IsolatedAsyncioTestCase):
    def test_valid_israeli_id(self):
        user_id = 123456782
        self.assertTrue(iec_api.commons.is_valid_israeli_id(user_id), "Israeli ID should be valid")

    def test_invalid_israeli_id(self):
        user_id = 123456789
        self.assertFalse(iec_api.commons.is_valid_israeli_id(user_id), "Israeli ID should be invalid")

    def test_invalid_israeli_id_long(self):
        user_id = 1234567890
        self.assertFalse(iec_api.commons.is_valid_israeli_id(user_id), "Israeli ID should be invalid")

    async def test_send_post_request_non_json_error_status(self):
        session = MagicMock()
        resp = MagicMock()
        resp.status = 504
        resp.reason = "Gateway Timeout"
        resp.json = AsyncMock(side_effect=JSONDecodeError("unexpected character", "<html...", 0))
        session.post = AsyncMock(return_value=resp)

        with self.assertRaises(iec_api.models.exceptions.IECError) as ctx:
            await iec_api.commons.send_post_request(session, "https://example.com")
        self.assertEqual(ctx.exception.code, 504)
        self.assertEqual(ctx.exception.error, "Gateway Timeout")

    async def test_send_get_request_non_json_error_status(self):
        session = MagicMock()
        resp = MagicMock()
        resp.status = 502
        resp.reason = "Bad Gateway"
        resp.json = AsyncMock(side_effect=JSONDecodeError("unexpected character", "<html...", 0))
        session.get = AsyncMock(return_value=resp)

        with self.assertRaises(iec_api.models.exceptions.IECError) as ctx:
            await iec_api.commons.send_get_request(session, "https://example.com")
        self.assertEqual(ctx.exception.code, 502)
        self.assertEqual(ctx.exception.error, "Bad Gateway")

    async def test_send_post_request_non_json_200_status(self):
        session = MagicMock()
        resp = MagicMock()
        resp.status = 200
        resp.reason = "OK"
        resp.json = AsyncMock(side_effect=JSONDecodeError("unexpected character", "<html...", 0))
        session.post = AsyncMock(return_value=resp)

        with self.assertRaises(iec_api.models.exceptions.IECError) as ctx:
            await iec_api.commons.send_post_request(session, "https://example.com")
        self.assertEqual(ctx.exception.code, -1)
        self.assertIn("Received invalid response from IEC API", ctx.exception.error)


if __name__ == "__main__":
    unittest.main()
