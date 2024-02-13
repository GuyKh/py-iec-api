from logging import getLogger

import jwt

from src import login, data
from src.const import HEADERS_WITH_AUTH
from src.models.contract import Contract
from src.models.customer import Customer
from src.models.electric_bill import Invoices
from src.models.meter_reading import MeterReadings
from src.models.remote_reading import RemoteReadingResponse

logger = getLogger(__name__)


class IecApiClient:

    def __init__(self, user_id):
        """
        Initialize the class with the provided phone number.
        Args:
        user_id (str): The User ID (SSN) to be associated with the instance.
        """
        # check_phone(phone)

        self.logged_in = None  # Flag to indicate if the user is logged in
        self._token = None  # Token for authentication
        self._user_id = user_id  # User ID associated with the instance
        self._login_response = None  # Login Response for OTP login
        self._bp_number = None  # BP Number associated with the instance
        self._contract_id = None  # Contract ID associated with the instance

    def login_with_id(self):
        """
        Login with ID and wait for SMS OTP
        :return: Login
        """
        self._login_response = login.login_with_id_number(self._user_id)

    def verify_otp(self, otp_code: str) -> str:
        """
        Verify the OTP code and return the token
        :param otp_code: The OTP code to be verified
        :return: The token
        """
        return login.verify_otp(self._user_id, self._login_response, otp_code)

    def manual_login(self):
        """
        Logs the user in by obtaining an authorization token, setting the authorization header,
        and updating the login status and token attribute.
        """
        token = login.get_authorization_token_from_user()
        logger.debug("Logged in with jwt token: %s", token)
        HEADERS_WITH_AUTH["Authorization"] = f"Bearer {token}"
        self.logged_in = True
        self._token = token

    def override_token(self, token):
        """
        Set the token and mark the user as logged in.
        :param token: The new token to be set.
        :return: None
        """
        logger.debug("Overriding jwt token: %s", token)
        self.logged_in = True
        self._token = token

    def get_customer(self) -> Customer:
        """
        Get consumer data response from IEC API.
        :return: Customer data
        """
        self.check_token()
        """Get consumer data response from IEC API."""
        customer = data.get_customer(self._token)
        if customer:
            self._bp_number = customer.bp_number
        return customer

    def get_contracts(self, bp_number: str = None) -> list[Contract]:
        """
        This function retrieves a contract based on the given BP number.
        :param bp_number: A string representing the BP number
        :return: A GetContractResponse object containing the contract information
        """

        self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        get_contract_response = data.get_contract(self._token, bp_number)
        if get_contract_response and get_contract_response.data:
            contracts = get_contract_response.data.contracts
            if contracts and len(contracts) > 0:
                self._contract_id = contracts[0].contract_id
            return contracts
        return list()

    def get_last_meter_reading(self, bp_number: str, contract_id: str) -> MeterReadings | None:
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

        if not contract_id:
            contract_id = self._contract_id

        response = data.get_last_meter_reading(self._token, bp_number, contract_id)
        if response and response.data:
            return response.data
        return None

    def get_electric_bill(self, bp_number: str, contract_id: str) -> Invoices | None:
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

        if not contract_id:
            contract_id = self._contract_id

        response = data.get_electric_bill(self._token, bp_number, contract_id)
        if response.data:
            return response.data
        return None

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
        return data.get_remote_reading(self._token, meter_serial_number, meter_code, last_invoice_date, from_date,
                                       resolution)

    def check_token(self):
        """
        Check the validity of the jwt token and refresh in the case of expired signature errors.
        """
        try:
            jwt.decode(self._token, options={"verify_signature": False}, algorithms=["RS256"])
        except jwt.exceptions.ExpiredSignatureError:
            logger.debug("jwt token expired, retrying login")
            self.logged_in = False
            login.refresh_token(self._token)
