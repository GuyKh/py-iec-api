""" Main IEC Python API module. """

import os
from datetime import datetime, timedelta
from logging import config, getLogger

from iec_api.iec_client import IecClient
from iec_api.login import IECLoginError
from iec_api.models.exceptions import IECError

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
config.fileConfig(ROOT_DIR + "/logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)

if __name__ == "__main__":  # pragma: no cover
    try:
        # Example of usage
        client = IecClient(200461929)

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

        # refresh token example
        #token = client.refresh_token()
        #client.save_token(token_json_file)
        #exit(1)

        # client.manual_login()
        account = client.get_default_account()
        print(account)

        contract = client.get_default_contract()
        print(contract)

        device = client.get_devices()[0]
        print(device)

        # Get Remote Readings from the last three days
        for i in range(2, -1, -1):
            selected_date: datetime = (datetime.now() - timedelta(days=i))
            remote_readings = client.get_remote_reading(device.device_number, int(device.device_code), selected_date,
                                                        selected_date)

            print("Got " + str(len(remote_readings.data)) + " readings for " + selected_date.strftime("%Y-%m-%d"))
            for remote_reading in remote_readings.data:
                print(remote_reading.date, remote_reading.value)

    except IECError as err:
        logger.error("IEC Error: (Code %d): %s", err.code, err.error)


