import asyncio
import atexit
import logging
from datetime import datetime
from typing import List, Optional

import aiofiles
import aiohttp
import jwt
from aiohttp import ClientSession

from iec_api import commons, data, fault_portal_data, login, static_data
from iec_api.fault_portal_models.outages import FaultPortalOutage
from iec_api.fault_portal_models.user_profile import UserProfile
from iec_api.models.account import Account
from iec_api.models.contract import Contract
from iec_api.models.contract_check import ContractCheck
from iec_api.models.customer import Customer
from iec_api.models.device import Device, Devices
from iec_api.models.device_identity import DeviceDetails
from iec_api.models.device_type import DeviceType
from iec_api.models.efs import EfsMessage
from iec_api.models.electric_bill import ElectricBill
from iec_api.models.exceptions import IECLoginError
from iec_api.models.invoice import GetInvoicesBody
from iec_api.models.jwt import JWT
from iec_api.models.meter_reading import MeterReadings
from iec_api.models.outages import Outage
from iec_api.models.remote_reading import ReadingResolution, RemoteReadingResponse
from iec_api.usage_calculator.calculator import UsageCalculator

logger = logging.getLogger(__name__)


class IecClient:
    """IEC API Client."""

    def __init__(self, user_id: str | int, session: Optional[ClientSession] = None):
        """
        Initializes the class with the provided user ID and optionally logs in automatically.

        Args:
        session (ClientSession): The aiohttp ClientSession object.
        user_id (str): The user ID (SSN) to be associated with the instance.
        automatically_login (bool): Whether to automatically log in the user. Default is False.
        """

        if not commons.is_valid_israeli_id(user_id):
            raise ValueError("User ID must be a valid Israeli ID.")

        # Custom Logger to the session
        trace_config = aiohttp.TraceConfig()
        trace_config.on_request_start.append(commons.on_request_start_debug)
        trace_config.on_request_chunk_sent.append(commons.on_request_chunk_sent_debug)
        trace_config.on_request_end.append(commons.on_request_end_debug)
        trace_config.freeze()

        if not session:
            session = aiohttp.ClientSession(trace_configs=[trace_config])
            atexit.register(self._shutdown)
        else:
            session.trace_configs.append(trace_config)

        self._session = session

        self._state_token: Optional[str] = None  # Token for maintaining the state of the user's session
        self._factor_id: Optional[str] = None  # Factor ID for multifactor authentication
        self._session_token: Optional[str] = None  # Token for maintaining the user's session
        self.logged_in: bool = False  # Flag to indicate if the user is logged in
        self._token: JWT = JWT(
            access_token="", refresh_token="", token_type="", expires_in=0, scope="", id_token=""
        )  # Token for authentication
        self._user_id: str = str(user_id)  # User ID associated with the instance
        self._login_response: Optional[str] = None  # Response from the login attempt
        self._bp_number: Optional[str] = None  # BP Number associated with the instance
        self._contract_id: Optional[str] = None  # Contract ID associated with the instance
        self._account_id: Optional[str] = None  # Account ID associated with the instance

    def _shutdown(self):
        if not self._session.closed:
            asyncio.run(self._session.close())

    # -------------
    # Data methods:
    # -------------

    async def get_customer(self) -> Optional[Customer]:
        """
        Get consumer data response from IEC API.
        :return: Customer data
        """
        await self.check_token()
        customer = await data.get_customer(self._session, self._token)
        if customer:
            self._bp_number = customer.bp_number
        return customer

    async def get_accounts(self) -> Optional[List[Account]]:
        """
        Get consumer data response from IEC API.
        :return: Customer data
        """
        await self.check_token()
        accounts = await data.get_accounts(self._session, self._token)

        if accounts and len(accounts) > 0:
            self._bp_number = accounts[0].account_number
            self._account_id = accounts[0].id

        return accounts

    async def get_default_account(self) -> Account:
        """
        Get consumer data response from IEC API.
        :return: Customer data
        """
        accounts = await self.get_accounts()
        return accounts[0]

    async def get_default_contract(self, bp_number: str = None) -> Optional[Contract]:
        """
        This function retrieves the default contract based on the given BP number.
        :param bp_number: A string representing the BP number
        :return: Contract object containing the contract information
        """

        await self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        get_contract_response = await data.get_contracts(self._session, self._token, bp_number)
        if get_contract_response:
            contracts = get_contract_response.contracts
            if contracts and len(contracts) > 0:
                self._contract_id = contracts[0].contract_id
            return contracts[0]
        return None

    async def get_contracts(self, bp_number: str = None) -> list[Contract]:
        """
        This function retrieves a contract based on the given BP number.
        :param bp_number: A string representing the BP number
        :return: list of Contract objects
        """

        await self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        get_contract_response = await data.get_contracts(self._session, self._token, bp_number)
        if get_contract_response:
            contracts = get_contract_response.contracts
            if contracts and len(contracts) > 0:
                self._contract_id = contracts[0].contract_id
            return contracts
        return []

    async def get_contract_check(self, contract_id: Optional[str] = None) -> Optional[ContractCheck]:
        """
        Get contract check for the contract
        Args:
            self: The instance of the class.
            contract_id (str): The Contract ID of the meter.
        Returns:
            ContractCheck: a contract check
        """
        await self.check_token()

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract Id must be provided"

        return await data.get_contract_check(self._session, self._token, contract_id)

    async def get_last_meter_reading(
        self, bp_number: Optional[str] = None, contract_id: Optional[str] = None
    ) -> Optional[MeterReadings]:
        """
        Retrieves a last meter reading for a specific contract and user.
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str): The contract ID associated with the meter.
        Returns:
            MeterReadings: The response containing the meter readings.
        """
        await self.check_token()
        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        return await data.get_last_meter_reading(self._session, self._token, bp_number, contract_id)

    async def get_electric_bill(
        self, bp_number: Optional[str] = None, contract_id: Optional[str] = None
    ) -> Optional[ElectricBill]:
        """
        Retrieves a remote reading for a specific meter using the provided parameters.
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str): The contract ID associated with the meter.
        Returns:
            ElectricBill: The Invoices/Electric Bills for the user with the contract_id
        """
        await self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        return await data.get_electric_bill(self._session, self._token, bp_number, contract_id)

    async def save_invoice_pdf_to_file(
        self,
        file_path: str,
        invoice_number: str | int,
        bp_number: Optional[str | int] = None,
        contract_id: Optional[str | int] = None,
    ):
        """
        Get PDF of invoice from IEC api
        Args:
            self: The instance of the class.
            file_path (str): Path to save the bill to
            invoice_number (str): The requested invoice number
            bp_number (str): The BP number of the meter.
            contract_id (str): The contract ID associated with the meter.
        """
        await self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        response_bytes = await data.get_invoice_pdf(self._session, self._token, bp_number, contract_id, invoice_number)
        if response_bytes:
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(response_bytes)

    async def get_devices(self, contract_id: Optional[str] = None) -> Optional[List[Device]]:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            contract_id (str): The Contract ID of the meter.
        Returns:
            list[Device]: List of devices
        """
        await self.check_token()

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract Id must be provided"

        return await data.get_devices(self._session, self._token, contract_id)

    async def get_device_by_device_id(self, device_id: str, contract_id: Optional[str] = None) -> Optional[Devices]:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            device_id (str): The Device code.
            contract_id (str): The Contract ID of the user.
        Returns:
            list[Device]: List of devices
        """
        await self.check_token()

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        return await data.get_device_by_device_id(self._session, self._token, contract_id, device_id)

    async def get_device_details_by_device_id(self, device_id: str) -> Optional[List[DeviceDetails]]:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            device_id (str): The Device id.
        Returns:
            list[DeviceDetails]: List of device details or None
        """
        await self.check_token()

        return await data.get_device_details(self._session, self._token, device_id)

    async def get_device_details_by_device_id_and_code(
        self, device_id: str, device_code: str
    ) -> Optional[DeviceDetails]:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            device_id (str): The Device id.
            device_code (str): The Device code.
        Returns:
            DeviceDetails: Device details or None
        """
        await self.check_token()

        return await data.get_device_details_by_code(self._session, self._token, device_id, device_code)

    async def get_remote_reading(
        self,
        meter_serial_number: str,
        meter_code: int,
        last_invoice_date: datetime,
        from_date: datetime,
        resolution: ReadingResolution = ReadingResolution.DAILY,
        contract_id: Optional[str] = None,
    ) -> Optional[RemoteReadingResponse]:
        """
        Retrieves a remote reading for a specific meter using the provided parameters.
        Args:
            self: The instance of the class.
            meter_serial_number (str): The serial number of the meter.
            meter_code (int): The code associated with the meter.
            last_invoice_date (str): The date of the last invoice.
            from_date (str): The start date for the remote reading.
            resolution (int): The resolution of the remote reading.
            contract_id (str): The contract id.
        Returns:
            RemoteReadingResponse: The response containing the remote reading or None if not found
        """
        await self.check_token()
        if not contract_id:
            contract_id = self._contract_id

        return await data.get_remote_reading(
            self._session,
            self._token,
            contract_id,
            meter_serial_number,
            meter_code,
            last_invoice_date,
            from_date,
            resolution,
        )

    async def get_device_type(
        self, bp_number: Optional[str] = None, contract_id: Optional[str] = None
    ) -> Optional[DeviceType]:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str: The Contract ID
        Returns:
            DeviceType
        """
        await self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        return await data.get_device_type(self._session, self._token, bp_number, contract_id)

    async def get_billing_invoices(
        self, bp_number: Optional[str] = None, contract_id: Optional[str] = None
    ) -> Optional[GetInvoicesBody]:
        """
        Get a list of devices for the user
        Args:
            self: The instance of the class.
            bp_number (str): The BP number of the meter.
            contract_id (str: The Contract ID
        Returns:
            Billing Invoices data
        """
        await self.check_token()

        if not bp_number:
            bp_number = self._bp_number

        assert bp_number, "BP number must be provided"

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract ID must be provided"

        return await data.get_billing_invoices(self._session, self._token, bp_number, contract_id)

    async def get_kwh_tariff(self) -> float:
        """Get kWh tariff"""
        return await static_data.get_kwh_tariff(self._session)

    async def get_usage_calculator(self) -> UsageCalculator:
        """
        Get Usage Calculator module
        Returns:
            UsageCalculator
        """
        return await static_data.get_usage_calculator(self._session)

    async def get_efs_messages(
        self, contract_id: Optional[str] = None, service_code: Optional[int] = None
    ) -> Optional[List[EfsMessage]]:
        """Get EFS Messages for the contract
        Args:
            self: The instance of the class.
            contract_id (str): The Contract ID of the meter.
            service_code (str): Specific EFS Service code
        Returns:
            list[EfsMessage]: List of EFS Messages
        """
        await self.check_token()

        if not contract_id:
            contract_id = self._contract_id

        assert contract_id, "Contract Id must be provided"

        return await data.get_efs_messages(self._session, self._token, contract_id, service_code)

    async def get_outages_by_account(self, account_id: Optional[str] = None) -> Optional[List[Outage]]:
        """Get Outages for the Account
        Args:
            self: The instance of the class.
            account_id (str): The Account ID of the meter.
        Returns:
            list[Outage]: List of the Outages Messages
        """
        await self.check_token()

        if not account_id:
            account_id = self._account_id

        assert account_id, "Account Id must be provided"

        return await data.get_outages_by_account(self._session, self._token, account_id)

    # ----------------
    # Fault Portal Endpoints
    # ----------------

    async def get_fault_portal_user_profile(self) -> Optional[UserProfile]:
        """Get User Profile for the Account from Fault Portal
        Args:
            self: The instance of the class.
        Returns:
            list[UserProfile]: The User Profile
        """
        await self.check_token()

        return await fault_portal_data.get_user_profile(self._session, self._token)

    async def get_fault_portal_outages_by_account(
        self, account_id: Optional[str] = None
    ) -> (Optional)[List[FaultPortalOutage]]:
        """Get Outages for the Account from Fault Portal
        Args:
            self: The instance of the class.
            account_id (str): The Account ID of the meter.
        Returns:
            list[Outage]: List of the Outages Messages
        """
        await self.check_token()

        if not account_id:
            account_id = self._account_id

        assert account_id, "Account Id must be provided"

        return await fault_portal_data.get_outages_by_account(self._session, self._token, account_id)

    # ----------------
    # Login/Token Flow
    # ----------------

    async def login_with_id(self):
        """
        Login with ID and wait for OTP
        """
        state_token, factor_id, session_token = self._login_response = await login.first_login(
            self._session, self._user_id
        )
        self._state_token = state_token
        self._factor_id = factor_id
        self._session_token = session_token

    async def verify_otp(self, otp_code: str | int) -> bool:
        """
        Verify the OTP code and return the token
        :param otp_code: The OTP code to be verified
        :return: The token
        """
        jwt_token = await login.verify_otp_code(self._session, self._factor_id, self._state_token, str(otp_code))
        self._token = jwt_token
        self.logged_in = True
        return True

    async def manual_login(self):
        """
        Logs the user in by obtaining an authorization token, setting the authorization header,
        and updating the login status and token attribute.
        """
        token = await login.manual_authorization(self._session, self._user_id)
        self.logged_in = True
        self._token = token

    def get_token(self) -> JWT:
        """
        Return the JWT token.
        """
        return self._token

    async def load_jwt_token(self, token: JWT):
        """
        Set the token and mark the user as logged in.
        :param token: The new token to be set.
        :return: None
        """
        self._token = token
        if await self.check_token():
            self.logged_in = True
        else:
            raise IECLoginError(-1, "Invalid JWT token")

    async def override_id_token(self, id_token):
        """
        Set the token and mark the user as logged in.
        :param id_token: The new token to be set.
        :return: None
        """
        logger.debug(f"Overriding jwt.py token: {id_token}")
        self._token = JWT(access_token="", refresh_token="", token_type="", expires_in=0, scope="", id_token=id_token)
        self._token.id_token = id_token
        self.logged_in = True

    async def check_token(self) -> bool:
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
            logger.debug("jwt.py token expired, refreshing token")
            self.logged_in = False
            await self.refresh_token()

        return True

    async def refresh_token(self):
        """
        Refresh IEC JWT token.
        """
        self._token = await login.refresh_token(self._session, self._token)
        if self._token:
            self.logged_in = True

    async def load_token_from_file(self, file_path: str = "token.json"):
        """
        Load token from file.
        """
        self._token = await login.load_token_from_file(file_path)
        self.logged_in = True

    async def save_token_to_file(self, file_path: str = "token.json"):
        """
        Save token to file.
        """
        await login.save_token_to_file(self._token, file_path)
