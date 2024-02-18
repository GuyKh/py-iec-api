import datetime
import time
from logging import getLogger

import jwt

from iec_api import data, login
from iec_api.commons import is_valid_israeli_id
from iec_api.const import DEFAULT_MINUTES_BEFORE_TO_REFRESH
from iec_api.models.contract import Contract
from iec_api.models.customer import Customer
from iec_api.models.device import Device, Devices
from iec_api.models.device_type import DeviceType
from iec_api.models.electric_bill import Invoices
from iec_api.models.invoice import GetInvoicesBody
from iec_api.models.jwt import JWT
from iec_api.models.meter_reading import MeterReadings
from iec_api.models.remote_reading import RemoteReadingResponse

logger = getLogger(__name__)


class IecClient:
    """ IEC API Client. """

    def __init__(self, user_id: str | int, automatically_login: bool = False,
                 mins_before_token_refresh: int = DEFAULT_MINUTES_BEFORE_TO_REFRESH):
        """
        Initializes the class with the provided user ID and optionally logs in automatically.

        Args:
        user_id (str): The user ID (SSN) to be associated with the instance.
        automatically_login (bool): Whether to automatically log in the user. Default is False.
        """

        if not is_valid_israeli_id(user_id):
            raise ValueError("User ID must be a valid Israeli ID.")

        self._state_token: str | None = None  # Token for maintaining the state of the user's session
        self._factor_id: str | None = None  # Factor ID for multi-factor authentication
        self._session_token: str | None = None  # Token for maintaining the user's session
        self.logged_in: bool = False  # Flag to indicate if the user is logged in
        self._token: JWT = JWT(access_token="", refresh_token="", token_type="", expires_in=0,
                               scope="", id_token="")  # Token for authentication
        self._user_id: str = str(user_id)  # User ID associated with the instance
        self._login_response: str | None = None  # Response from the login attempt
        self._bp_number: str | None = None  # BP Number associated with the instance
        self._contract_id: str | None = None  # Contract ID associated with the instance
        self._mins_before_token_refresh = mins_before_token_refresh # Minutes before requiring JWT token to refresh

        if automatically_login:
            self.login_with_id()  # Attempt to log in automatically if specified

    def login_with_id(self):
        """
        Login with ID and wait for OTP
        """
        state_token, factor_id, session_token = self._login_response = login.first_login(self._user_id)
        self._state_token = state_token
        self._factor_id = factor_id
        self._session_token = session_token

    def verify_otp(self, otp_code: str | int) -> bool:
        """
        Verify the OTP code and return the token
        :param otp_code: The OTP code to be verified
        :return: The token
        """
        jwt_token = login.verify_otp_code(self._factor_id, self._state_token, str(otp_code))
        self._token = jwt_token
        self.logged_in = True
        return True

    def manual_login(self):
        """
        Logs the user in by obtaining an authorization token, setting the authorization header,
        and updating the login status and token attribute.
        """
        token = login.manual_authorization(self._user_id)
        self.logged_in = True
        self._token = token

    def override_token(self, token):
        """
        Set the token and mark the user as logged in.
        :param token: The new token to be set.
        :return: None
        """
        logger.debug("Overriding jwt.py token: %s", token)
        self._token = JWT(access_token="", refresh_token="", token_type="", expires_in=0, scope="", id_token=token)
        self._token.id_token = token
        self.logged_in = True

    def get_customer(self) -> Customer:
        """
        Get consumer data response from IEC API.
        :return: Customer data
        """
        self.check_token()
        customer = data.get_customer(self._token)
        if customer:
            self._bp_number = customer.bp_number
        return customer

    def get_default_contract(self, bp_number: str = None) -> Contract | None:
        """
        This function retrieves the default contract based on the given BP number.
        :param bp_number: A string representing the BP number
        :return: Contract object containing the contract information
        """

        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        get_contract_response = data.get_contracts(self._token, bp_number)
        if get_contract_response and get_contract_response.data:
            contracts = get_contract_response.data.contracts
            if contracts and len(contracts) > 0:
                self._contract_id = contracts[0].contract_id
            return contracts[0]
        return None

    def get_contracts(self, bp_number: str = None) -> list[Contract]:
        """
        This function retrieves a contract based on the given BP number.
        :param bp_number: A string representing the BP number
        :return: list of Contract objects
        """

        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        get_contract_response = data.get_contracts(self._token, bp_number)
        if get_contract_response and get_contract_response.data:
            contracts = get_contract_response.data.contracts
            if contracts and len(contracts) > 0:
                self._contract_id = contracts[0].contract_id
            return contracts
        return []

    def get_last_meter_reading(self, bp_number: str | None = None,
                               contract_id: str | None = None) -> MeterReadings | None:
        """
        Retrieves a last meter reading for a specific contract and user.
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str): The contract ID associated with the meter.
        Returns:
            MeterReadings: The response containing the meter readings.
        """
        self.check_token()
        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        response = data.get_last_meter_reading(self._token, bp_number, contract_id)
        if response and response.data:
            return response.data
        return None

    def get_electric_bill(self, bp_number: str | None = None, contract_id: str | None = None) -> Invoices | None:
        """
        Retrieves a remote reading for a specific meter using the provided parameters.
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str): The contract ID associated with the meter.
        Returns:
            Invoices: The Invoices/Electric Bills for the user with the contract_id
        """
        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        response = data.get_electric_bill(self._token, bp_number, contract_id)
        if response.data:
            return response.data
        return None

    def get_devices(self, bp_number: str | None = None) -> list[Device] | None:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
        Returns:
            list[Device]: List of devices
        """
        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        return data.get_devices(self._token, bp_number)

    def get_devices_by_contract_id(self, bp_number: str | None = None, contract_id: str | None = None) -> Devices:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the user.
            contract_id (str): The Contract ID of the user.
        Returns:
            list[Device]: List of devices
        """
        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        return data.get_devices_by_contract_id(self._token, bp_number, contract_id)

    def get_remote_reading(self, meter_serial_number: str, meter_code: int, last_invoice_date: str, from_date: str,
                           resolution: int) -> RemoteReadingResponse:
        """
        Retrieves a remote reading for a specific meter using the provided parameters.
        Args:
            self: The instance of the class.
            meter_serial_number (str): The serial number of the meter.
            meter_code (int): The code associated with the meter.
            last_invoice_date (str): The date of the last invoice.
            from_date (str): The start date for the remote reading.
            resolution (int): The resolution of the remote reading.
        Returns:
            RemoteReadingResponse: The response containing the remote reading.
        """
        self.check_token()
        return data.get_remote_reading(self._token, meter_serial_number, meter_code,
                                       last_invoice_date, from_date, resolution)

    def get_device_type(self, bp_number: str | None = None, contract_id: str | None = None) -> DeviceType:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str: The Contract ID
        Returns:
            DeviceType
        """
        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        return data.get_device_type(self._token, bp_number, contract_id)

    def get_billing_invoices(self, bp_number: str, contract_id: str) -> GetInvoicesBody:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str: The Contract ID
        Returns:
            Billing Invoices data
        """
        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        return data.get_billing_invoices(self._token, bp_number, contract_id)

    def check_token(self):
        """
        Check the validity of the jwt.py token and refresh in the case of expired signature errors.
        """
        should_refresh = False
        should_relogin = False

        try:
            remaining_to_expiration = self.get_token_remaining_time_to_expiration()
            if remaining_to_expiration < 0:
                should_relogin = True
            if remaining_to_expiration < datetime.timedelta(minutes=self._mins_before_token_refresh).seconds:
                should_refresh = True

        except jwt.exceptions.ExpiredSignatureError:
            should_relogin = True

        if should_refresh:
            logger.debug("jwt.py token is about to expire, refreshing token")
            self.logged_in = False
            self.refresh_token()

        if should_relogin:
            logger.debug("jwt.py token expired, retrying login")
            self.logged_in = False

    def get_token_remaining_time_to_expiration(self):
        decoded_token = jwt.decode(self._token.id_token, options={"verify_signature": False}, algorithms=["RS256"])
        return decoded_token['exp'] - int(time.time())

    def refresh_token(self):
        """
        Refresh IEC JWT token.
        """
        self._token = login.refresh_token(self._token)
        self.logged_in = True

    def load_token(self, file_path: str = "token.json"):
        """
        Load token from file.
        """
        self._token = login.load_token_from_file(file_path)
        self.logged_in = True

    def save_token(self, file_path: str = "token.json"):
        """
        Save token to file.
        """
        login.save_token_to_file(self._token, file_path)
