""" Main IEC Python API module. """

import asyncio
import os
from logging import config, getLogger

import aiohttp

from iec_api.iec_client import IecClient
from iec_api.login import IECLoginError
from iec_api.models.exceptions import IECError

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
config.fileConfig(ROOT_DIR + "/" +"logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)


async def main():
    try:
        # Example of usage
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False),
                                        timeout=aiohttp.ClientTimeout(total=10))

        client = IecClient(session, "123456782")

        token_json_file = "token.json"
        if os.path.exists(token_json_file):
            client.load_token(token_json_file)
        else:
            try:
                await client.login_with_id()
                otp = input("Enter the OTP received: ")
                await client.verify_otp(otp)
                client.save_token(token_json_file)
            except IECLoginError as err:
                logger.error("Failed Login: (Code %d): %s", err.code, err.error)

        # refresh token example
        # token = await client.refresh_token()
        # client.save_token(token_json_file)
        # exit(1)

        # client.manual_login()
        customer = await client.get_customer()
        print(customer)

        contracts = await client.get_contracts()
        for contract in contracts:
            print(contract)

        reading = await client.get_last_meter_reading(customer.bp_number, contracts[0].contract_id)
        print(reading)

        print(await client.get_devices_by_contract_id())
        print(await client.get_electric_bill())
        print(await client.get_device_type())
        print(await client.get_devices())
        print(await client.get_billing_invoices())
    except IECError as err:
        logger.error("IEC Error: (Code %d): %s", err.code, err.error)


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
