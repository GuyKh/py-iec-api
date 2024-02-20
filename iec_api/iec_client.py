import datetime
from logging import getLogger
from typing import Optional

import jwt

from iec_api import data, login
from iec_api.commons import is_valid_israeli_id
from iec_api.models.contract import Contract
from iec_api.models.customer import Account, Customer
from iec_api.models.device import Device, Devices
from iec_api.models.device_type import DeviceType
from iec_api.models.electric_bill import ElectricBill
from iec_api.models.exceptions import IECLoginError
from iec_api.models.invoice import GetInvoicesBody
from iec_api.models.jwt import JWT
from iec_api.models.meter_reading import MeterReadings
from iec_api.models.remote_reading import ReadingResolution, RemoteReadingResponse

logger = getLogger(__name__)


class IecClient:
    """ IEC API Client. """

    def __init__(self, user_id: str | int, automatically_login: bool = False):
        """
        Initializes the class with the provided user ID and optionally logs in automatically.

        Args:
        user_id (str): The user ID (SSN) to be associated with the instance.
        automatically_login (bool): Whether to automatically log in the user. Default is False.
        """

        if not is_valid_israeli_id(user_id):
            raise ValueError("User ID must be a valid Israeli ID.")

        self._state_token: Optional[str] = None  # Token for maintaining the state of the user's session
        self._factor_id: Optional[str] = None  # Factor ID for multifactor authentication
        self._session_token: Optional[str] = None  # Token for maintaining the user's session
        self.logged_in: bool = False  # Flag to indicate if the user is logged in
        self._token: JWT = JWT(access_token="", refresh_token="", token_type="", expires_in=0,
                               scope="", id_token="")  # Token for authentication
        self._user_id: str = str(user_id)  # User ID associated with the instance
        self._login_response: Optional[str] = None  # Response from the login attempt
        self._bp_number: Optional[str] = None  # BP Number associated with the instance
        self._contract_id: Optional[str] = None  # Contract ID associated with the instance

        if automatically_login:
            self.login_with_id()  # Attempt to log in automatically if specified

    # -------------
    # Data methods:
    # -------------

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

    def get_accounts(self) -> list[Account]:
        """
        Get consumer data response from IEC API.
        :return: Customer data
        """
        self.check_token()
        accounts = data.get_accounts(self._token)

        if len(accounts) > 0:
            self._bp_number = accounts[0].account_number

        return accounts

    def get_default_account(self) -> Account:
        """
        Get consumer data response from IEC API.
        :return: Customer data
        """
        return self.get_accounts()[0]

    def get_default_contract(self, bp_number: str = None) -> Optional[Contract]:
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
        if get_contract_response and get_contract_response:
            contracts = get_contract_response.contracts
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
        if get_contract_response and get_contract_response:
            contracts = get_contract_response.contracts
            if contracts and len(contracts) > 0:
                self._contract_id = contracts[0].contract_id
            return contracts
        return []

    def get_last_meter_reading(self, bp_number: Optional[str] = None,
                               contract_id: Optional[str] = None) -> Optional[MeterReadings]:
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
        if response:
            return response
        return None

    def get_electric_bill(self, bp_number: Optional[str] = None, contract_id: Optional[str] = None) \
            -> Optional[ElectricBill]:
        """
        Retrieves a remote reading for a specific meter using the provided parameters.
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str): The contract ID associated with the meter.
        Returns:
            ElectricBill: The Invoices/Electric Bills for the user with the contract_id
        """
        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        response = data.get_electric_bill(self._token, bp_number, contract_id)
        if response:
            return response
        return None

    def get_devices(self, contract_id: Optional[str] = None) -> Optional[list[Device]]:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            contract_id (str): The Contract ID of the meter.
        Returns:
            list[Device]: List of devices
        """
        self.check_token()

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract Id must be provided"

        return data.get_devices(self._token, contract_id)

    def get_devices_by_contract_id(self, bp_number: Optional[str] = None, contract_id: Optional[str] = None) -> Devices:
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

    def get_remote_reading(self, meter_serial_number: str, meter_code: int,
                           last_invoice_date: datetime, from_date: datetime,
                           resolution: ReadingResolution = ReadingResolution.DAILY) -> Optional[RemoteReadingResponse]:
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
            RemoteReadingResponse: The response containing the remote reading or None if not found
        """
        self.check_token()
        return data.get_remote_reading(self._token, meter_serial_number, meter_code,
                                       last_invoice_date, from_date, resolution)

    def get_device_type(self, bp_number: Optional[str] = None, contract_id: Optional[str] = None) -> DeviceType:
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

    def get_billing_invoices(self, bp_number: Optional[str] = None, contract_id: Optional[str] = None) \
            -> GetInvoicesBody:
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

    # ----------------
    # Login/Token Flow
    # ----------------

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

    def get_token(self) -> JWT:
        """
        Return the JWT token.
        """
        return self._token

    def load_jwt_token(self, token: JWT):
        """
        Set the token and mark the user as logged in.
        :param token: The new token to be set.
        :return: None
        """
        self._token = token
        if self.check_token():
            self.logged_in = True

    def override_id_token(self, id_token):
        """
        Set the token and mark the user as logged in.
        :param id_token: The new token to be set.
        :return: None
        """
        logger.debug("Overriding jwt.py token: %s", id_token)
        self._token = JWT(access_token="", refresh_token="", token_type="", expires_in=0, scope="", id_token=id_token)
        self._token.id_token = id_token
        self.logged_in = True

    def check_token(self) -> bool:
        """
        Check the validity of the jwt.py token and refresh in the case of expired signature errors.
        """
        should_refresh = False

        try:
            remaining_to_expiration = login.get_token_remaining_time_to_expiration(self._token)
            if remaining_to_expiration < 0:
                should_refresh = True

        except jwt.exceptions.ExpiredSignatureError as e:
            raise IECLoginError(-1, "Expired JWT token") from e

        if should_refresh:
            logger.debug("jwt.py token is about to expire, refreshing token")
            self.logged_in = False
            self.refresh_token()

        return self.logged_in

    def refresh_token(self):
        """
        Refresh IEC JWT token.
        """
        self._token = login.refresh_token(self._token)
        if self._token:
            self.logged_in = True

    def load_token_from_file(self, file_path: str = "token.json"):
        """
        Load token from file.
        """
        self._token = login.load_token_from_file(file_path)
        self.logged_in = True

    def save_token_to_file(self, file_path: str = "token.json"):
        """
        Save token to file.
        """
        login.save_token_to_file(self._token, file_path)
