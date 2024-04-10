""" Main IEC Python API module. """

import asyncio
import concurrent.futures
import logging
import os
from datetime import datetime, timedelta

import aiohttp

from iec_api import commons
from iec_api.iec_client import IecClient
from iec_api.login import IECLoginError
from iec_api.models.exceptions import IECError

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.DEBUG)

    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(commons.on_request_start_debug)
    trace_config.on_request_chunk_sent.append(commons.on_request_chunk_sent_debug)
    trace_config.on_request_end.append(commons.on_request_end_debug)

    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False), timeout=aiohttp.ClientTimeout(total=10), trace_configs=[trace_config]
    )
    try:
        # Example of usage
        client = IecClient(123456782, session)

        token_json_file = "token.json"
        if os.path.exists(token_json_file):
            await client.load_token_from_file(token_json_file)
        else:
            try:
                await client.login_with_id()
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    otp = await asyncio.get_event_loop().run_in_executor(pool, input, "Enter the OTP received: ")
                await client.verify_otp(otp)
                await client.save_token_to_file(token_json_file)
            except IECLoginError as err:
                logger.error(f"Failed Login: (Code {err.code}): {err.error}")
                raise

        # refresh token example
        token = client.get_token()
        await client.check_token()
        new_token = client.get_token()
        if token != new_token:
            print("Token refreshed")
            await client.save_token_to_file(token_json_file)

        print("id_token: " + token.id_token)

        tariff = await client.get_kwh_tariff()
        print(tariff)

        # client.manual_login()
        customer = await client.get_customer()
        print(customer)

        contracts = await client.get_contracts()
        for contract in contracts:
            print(contract)

        reading = await client.get_last_meter_reading(customer.bp_number, contracts[0].contract_id)
        print(reading)

        devices = await client.get_devices()
        device = devices[0]
        print(device)

        device_details = await client.get_device_by_device_id(device.device_number)
        print(device_details)

        # Get Remote Readings from the last three days

        selected_date: datetime = datetime.now() - timedelta(days=30)

        remote_readings = await client.get_remote_reading(
            device.device_number, int(device.device_code), selected_date, selected_date
        )

        if remote_readings:
            print("Got " + str(len(remote_readings.data)) + " readings for " + selected_date.strftime("%Y-%m-%d"))
            for remote_reading in remote_readings.data:
                print(remote_reading.date, remote_reading.value)
        else:
            print("Got no readings")

        print(await client.get_electric_bill())
        print(await client.get_device_type())
        print(await client.get_billing_invoices())
    except IECError as err:
        logger.error(f"IEC Error: (Code {err.code}): {err.error}")
    finally:
        await session.close()


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
