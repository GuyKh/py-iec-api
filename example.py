""" Main IEC Python API module. """

import os
from logging import config, getLogger

from py_iec.iec_client import IecClient
from py_iec.login import IECLoginError
from py_iec.models.exceptions import IECError

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)

if __name__ == "__main__":  # pragma: no cover
    try:
        # Example of usage
        client = IecClient(123456782)

        token_json_file = "token.json"
        if os.path.exists(token_json_file):
            client.load_token(token_json_file)
        else:
            try:
                client.login_with_id()
                otp = input("Enter the OTP received: ")
                token = client.verify_otp(otp)
                client.save_token(token_json_file)
            except IECLoginError as err:
                logger.error("Failed Login: (Code %d): %s", err.code, err.error)

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
    except IECError as err:
        logger.error("IEC Error: (Code %d): %s", err.code, err.error)


