import unittest
from datetime import datetime, timedelta

from iec_api.iec_client import IecClient
from iec_api.models.jwt import JWT


class CommonsTest(unittest.IsolatedAsyncioTestCase):
    jwt_token = {
        "access_token": "Fill",
        "refresh_token": "this",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "offline_access email openid profile",
        "id_token": "yourself",
    }

    async def test_e2e_with_existing_token(self):
        user_id = 1234567832

        client = IecClient(user_id)
        await client.load_jwt_token(JWT.from_dict(self.jwt_token))
        await client.check_token()
        await client.refresh_token()
        await client.save_token_to_file()

        await client.get_customer()
        await client.get_accounts()
        await client.get_default_account()
        await client.get_contracts()
        await client.get_default_contract()

        await client.get_device_type()
        devices = await client.get_devices()
        device = devices[0]
        await client.get_device_by_device_id(device_id=device.device_number)

        await client.get_billing_invoices()
        await client.get_electric_bill()
        await client.get_last_meter_reading()

        selected_date: datetime = datetime.now() - timedelta(days=30)

        await client.get_remote_reading(device.device_number, int(device.device_code), selected_date, selected_date)

        await client.save_token_to_file()
        await client.load_token_from_file()
        await client.check_token()
        await client.refresh_token()


if __name__ == "__main__":
    unittest.main()
