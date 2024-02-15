import unittest

import iec_api.commons


class CommonsTest(unittest.TestCase):
    def test_valid_israeli_id(self):
        user_id = 123456782
        self.assertTrue(iec_api.commons.is_valid_israeli_id(user_id), "Israeli ID should be valid")

    def test_invalid_israeli_id(self):
        user_id = 123456789
        self.assertFalse(iec_api.commons.is_valid_israeli_id(user_id), "Israeli ID should be invalid")

    def test_invalid_israeli_id_long(self):
        user_id = 1234567890
        self.assertFalse(iec_api.commons.is_valid_israeli_id(user_id), "Israeli ID should be invalid")


if __name__ == '__main__':
    unittest.main()
