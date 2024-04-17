""" Main IEC Python API module. """

import asyncio
import concurrent.futures
import logging
import os
from datetime import datetime, timedelta

import aiohttp

from iec_api.iec_client import IecClient
from iec_api.login import IECLoginError
from iec_api.models.exceptions import IECError
from iec_api.usage_calculator.calculator import UsageCalculator

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.DEBUG)

    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=aiohttp.ClientTimeout(total=10))
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

    #
    # Example of usage of UsageCalculator
    #
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=aiohttp.ClientTimeout(total=10))
    try:
        usage_calculator = UsageCalculator()
        await usage_calculator.load_data(session)

        # Get kWh Tariff
        tariff = usage_calculator.get_kwh_tariff()
        print(f"kWh Tariff: {tariff} ILS/kWh")

        # Get all device names
        device_names = usage_calculator.get_device_names()
        print(device_names)

        # Select "Air-conditioner"
        device_name = device_names[8]
        print(f"Selected device: [{device_name}]")

        # Get device info by name
        device = usage_calculator.get_device_info_by_name(device_name)
        print(device)

        # Get default utility consumption by time
        consumption = usage_calculator.get_consumption_by_device_and_time(device_name, timedelta(days=1), None)
        print(consumption)

        # You can specify specific power usage of your device:
        # e.g. 3.5HP air-conditioner running for 6 hours
        consumption = usage_calculator.get_consumption_by_device_and_time(
            device_name, timedelta(hours=6), custom_usage_value=3.5
        )
        print(
            f"Running a {consumption.power} {consumption.power_unit.name} {consumption.name} "
            f"for {consumption.duration.seconds // (60 * 60)} hours would cost: "
            f"{round(consumption.cost, 2)} ILS"
        )

    finally:
        await session.close()


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
