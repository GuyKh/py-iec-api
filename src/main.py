""" Main IEC Python API module. """

import os
from logging import getLogger

from src.iec_api_client import IecApiClient
from src.login import IECLoginError

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
# logConfig("logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)

if __name__ == "__main__":  # pragma: no cover
    try:
        # Example of usage
        client = IecApiClient("123456789")

        token_json_file = "token.json"
        if os.path.exists(token_json_file):
            client.load_token(token_json_file)
        else:
            client.login_with_id()
            otp = input("Enter the OTP received: ")
            client.verify_otp(otp)
            client.save_token(token_json_file)

        # client.manual_login()
        customer = client.get_customer()
        print(customer)

        contracts = client.get_contracts()
        for contract in contracts:
            print(contract)

        reading = client.get_last_meter_reading(customer.bp_number, contracts[0].contract_id)
        print(reading)

        print(client.get_devices_by_contract_id())
        print(client.get_electric_bill())
        print(client.get_device_type())
        print(client.get_devices())
        print(client.get_billing_invoices())

    except IECLoginError as err:
        logger.error("Failed Login: (Code %d): %s", err.code, err.error)
