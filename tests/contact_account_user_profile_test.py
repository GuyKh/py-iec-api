import unittest

from iec_api.masa_api_models.contact_account_user_profile import (
    MasaMainPortalContactAccountUserProfile,
)


def _base_payload() -> dict:
    """A minimal valid MASA main-portal user-profile payload (no verificationStatus)."""
    return {
        "governmentid": "000000000",
        "idType": 1,
        "firstName": "Test",
        "email": "test@example.com",
        "phoneNumber": "0500000000",
        "accounts": [],
        "phonePrefix": "050",
        "isConnectedToPrivateAccount": True,
        "isAccountOwner": True,
        "isAccountContact": False,
        "connectionBetweenContactAndContract": [],
        "id": "4cbc8831-1c73-e811-8102-3863bb357f98",
        "logicalName": "contact",
    }


class MasaMainPortalContactAccountUserProfileTest(unittest.TestCase):
    def test_parse_without_verification_status(self):
        """The endpoint omits verificationStatus for some accounts (e.g. private
        supplier); parsing must succeed and default the field to None."""
        payload = _base_payload()
        self.assertNotIn("verificationStatus", payload)

        profile = MasaMainPortalContactAccountUserProfile.from_dict(payload)

        self.assertIsNone(profile.verification_status)

    def test_parse_with_verification_status(self):
        """When verificationStatus is present it is preserved (both True and False)."""
        for value in (True, False):
            with self.subTest(value=value):
                payload = _base_payload()
                payload["verificationStatus"] = value

                profile = MasaMainPortalContactAccountUserProfile.from_dict(payload)

                self.assertEqual(profile.verification_status, value)

    def test_serialization_preserves_verification_status(self):
        """Serialization keeps the value. The model deserializes by the
        verificationStatus alias but to_dict emits the field name (it has no
        serialize_by_alias config), so assert the value is retained."""
        payload = _base_payload()
        payload["verificationStatus"] = True

        profile = MasaMainPortalContactAccountUserProfile.from_dict(payload)
        serialized = profile.to_dict()

        self.assertIn("verification_status", serialized)
        self.assertTrue(serialized["verification_status"])


if __name__ == "__main__":
    unittest.main()
