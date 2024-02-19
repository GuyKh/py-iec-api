import json
import logging
from datetime import datetime
from typing import Optional, TypeVar

import requests

from iec_api.commons import add_jwt_to_headers
from iec_api.const import (
    GET_ACCOUNTS_URL,
    GET_BILLING_INVOICES,
    GET_CONSUMER_URL,
    GET_CONTRACTS_URL,
    GET_DEFAULT_CONTRACT_URL,
    GET_DEVICE_TYPE_URL,
    GET_DEVICES_BY_CONTRACT_ID_URL,
    GET_DEVICES_URL,
    GET_ELECTRIC_BILL_URL,
    GET_LAST_METER_READING_URL,
    GET_REQUEST_READING_URL,
    HEADERS_WITH_AUTH,
)
from iec_api.models.account import Account
from iec_api.models.contract import Contract, Contracts
from iec_api.models.customer import Customer
from iec_api.models.device import Device, Devices
from iec_api.models.device_type import DeviceType
from iec_api.models.electric_bill import Invoices
from iec_api.models.exceptions import IECError
from iec_api.models.invoice import GetInvoicesBody
from iec_api.models.jwt import JWT
from iec_api.models.meter_reading import MeterReadings
from iec_api.models.remote_reading import RemoteReadingRequest, RemoteReadingResponse
from iec_api.models.response_descriptor import ErrorResponseDescriptor, ResponseWithDescriptor

logger = logging.getLogger(__name__)


def _get_url(url, headers):
    logger.debug("HTTP GET: %s", url)
    return requests.get(url=url, headers=headers, timeout=10)


T = TypeVar("T")


def _get_response_with_descriptor(jwt_token: JWT, request_url: str) -> dict | list[dict]:
    """
    A function to retrieve a response with a descriptor using a JWT token and a URL.

    Args:
        jwt_token (JWT): The JWT token used for authentication.
        request_url (str): The URL to send the request to.

    Returns:
        T: The response with a descriptor, with its type specified by the return type annotation.
    """
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, jwt_token.id_token)
    response = _get_url(request_url, headers)

    if response.status_code != 200:
        if response.content:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    response_with_descriptor = ResponseWithDescriptor[T].from_dict(response.json())

    if not response_with_descriptor.response_descriptor.is_success:
        raise IECError(response_with_descriptor.response_descriptor.code,
                       response_with_descriptor.response_descriptor.description)

    return response_with_descriptor.data


def get_accounts(token: JWT) -> list[Account]:
    """Get Accounts response from IEC API."""
    accounts = _get_response_with_descriptor(token, GET_ACCOUNTS_URL)

    accounts = [Account.from_dict(account) for account in accounts]
    return accounts


def get_customer(token: JWT) -> Optional[Customer]:
    """Get customer data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_CONSUMER_URL, headers=headers)

    if response.status_code != 200:
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return Customer.from_dict(response.json())


def get_remote_reading(token: JWT, meter_serial_number: str, meter_code: int, last_invoice_date: datetime,
                       from_date: datetime, resolution: int = 1) -> Optional[RemoteReadingResponse]:
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    req = RemoteReadingRequest(meter_serial_number=meter_serial_number, meter_code=meter_code,
                               last_invoice_date=last_invoice_date.strftime('%Y-%m-%d'),
                               from_date=from_date.strftime('%Y-%m-%d'), resolution=resolution)

    logger.debug("HTTP POST: %s", GET_REQUEST_READING_URL)

    data = req.to_dict()
    json_data = json.dumps(data)
    response = requests.post(url=GET_REQUEST_READING_URL, data=json_data, headers=headers, timeout=10)

    if response.status_code != 200:
        if response.status_code == 400:
            return None

        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return RemoteReadingResponse.from_dict(response.json())


def get_electric_bill(token: JWT, bp_number: str, contract_id: str) -> Invoices:
    """Get Electric Bill data response from IEC API."""
    invoice_dict = _get_response_with_descriptor(token,
                                                 GET_ELECTRIC_BILL_URL.format(contract_id=contract_id,
                                                                              bp_number=bp_number))
    return Invoices.from_dict(invoice_dict)


def get_default_contract(token: JWT, bp_number: str) -> Contract:
    """Get Contract data response from IEC API."""
    all_contracts_dict = _get_response_with_descriptor(token, GET_DEFAULT_CONTRACT_URL.format(bp_number=bp_number))

    all_contracts = [Contract.from_dict(contract) for contract in all_contracts_dict]
    return all_contracts[0]


def get_contracts(token: JWT, bp_number: str) -> Contracts:
    """Get all user's Contracts from IEC API."""
    contracts_dict = _get_response_with_descriptor(token, GET_CONTRACTS_URL.format(bp_number=bp_number))
    return Contracts.from_dict(contracts_dict)


def get_last_meter_reading(token: JWT, bp_number: str, contract_id: str) -> MeterReadings:
    """Get Last Meter Reading data response from IEC API."""
    meter_readings_dict = _get_response_with_descriptor(token,
                                                        GET_LAST_METER_READING_URL.format(contract_id=contract_id,
                                                                                          bp_number=bp_number))

    return MeterReadings.from_dict(meter_readings_dict)


def get_devices(token: JWT, bp_number: str) -> list[Device]:
    """Get Device data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEVICES_URL.format(bp_number=bp_number),
                        headers=headers)

    if response.status_code != 200:
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return [Device.from_dict(device) for device in response.json()]


def get_devices_by_contract_id(token: JWT, bp_number: str, contract_id: str) -> Devices:
    """Get Device data response from IEC API."""
    devices_dict = _get_response_with_descriptor(token, GET_DEVICES_BY_CONTRACT_ID_URL.format(bp_number=bp_number,
                                                                                              contract_id=contract_id))
    return Devices.from_dict(devices_dict)


def get_device_type(token: JWT, bp_number: str, contract_id: str) -> DeviceType:
    """Get Device Type data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEVICE_TYPE_URL.format(bp_number=bp_number, contract_id=contract_id),
                        headers=headers)

    if response.status_code != 200:
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    return DeviceType.from_dict(response.json())


def get_billing_invoices(token: JWT, bp_number: str, contract_id: str) -> GetInvoicesBody:
    """Get Device Type data response from IEC API."""
    get_invoices_body_dict = _get_response_with_descriptor(token, GET_BILLING_INVOICES.format(bp_number=bp_number,
                                                                                              contract_id=contract_id))
    return GetInvoicesBody.from_dict(get_invoices_body_dict)
