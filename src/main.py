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
        client.manual_login()
        customer = client.get_customer()
        print(customer)

        contracts = client.get_contracts()
        for contract in contracts:
            print(contract)

        reading = client.get_last_meter_reading(customer.bp_number, contracts[0].contract_id)
        print(reading)
    except IECLoginError as err:
        logger.error("Failed Login: (Code %d): %s", err.code, err.error)
