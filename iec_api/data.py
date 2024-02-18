import json
import logging

import requests

from iec_api.commons import add_jwt_to_headers
from iec_api.const import (
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
from iec_api.models.contract import GetContractResponse
from iec_api.models.customer import Customer
from iec_api.models.device import Device, Devices, GetDeviceResponse
from iec_api.models.device_type import DeviceType
from iec_api.models.electric_bill import GetElectricBillResponse
from iec_api.models.exceptions import IECError
from iec_api.models.invoice import GetInvoicesBody, GetInvoicesResponse
from iec_api.models.jwt import JWT
from iec_api.models.meter_reading import GetLastMeterReadingResponse
from iec_api.models.remote_reading import RemoteReadingRequest, RemoteReadingResponse
from iec_api.models.response_descriptor import ErrorResponseDescriptor

logger = logging.getLogger(__name__)


def _get_url(url, headers):
    logger.debug("HTTP GET: %s", url)
    return requests.get(url=url, headers=headers, timeout=10)


def get_customer(token: JWT) -> Customer:
    """Get customer data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_CONSUMER_URL, headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return Customer.from_dict(response.json())


def get_remote_reading(token: JWT, meter_serial_number: str, meter_code: int, last_invoice_date: str, from_date: str,
                       resolution: int) -> RemoteReadingResponse:
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    req = RemoteReadingRequest(meterSerialNumber=meter_serial_number, meterCode=meter_code,
                               lastInvoiceDate=last_invoice_date, fromDate=from_date, resolution=resolution)

    logger.debug("HTTP POST: %s", GET_REQUEST_READING_URL)
    response = requests.post(url=GET_REQUEST_READING_URL, data=json.dumps(req), headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return RemoteReadingResponse.from_dict(response.json())


def get_electric_bill(token: JWT, bp_number: str, contract_id: str) -> GetElectricBillResponse:
    """Get Electric Bill data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_ELECTRIC_BILL_URL.format(contract_id=contract_id, bp_number=bp_number),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return GetElectricBillResponse.from_dict(response.json())


def get_default_contract(token: JWT, bp_number: str) -> GetContractResponse:
    """Get Electric Bill data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEFAULT_CONTRACT_URL.format(bp_number=bp_number), headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return GetContractResponse.from_dict(response.json())


def get_contracts(token: JWT, bp_number: str) -> GetContractResponse:
    """Get Electric Bill data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_CONTRACTS_URL.format(bp_number=bp_number), headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return GetContractResponse.from_dict(response.json())


def get_last_meter_reading(token: JWT, bp_number: str, contract_id: str) -> GetLastMeterReadingResponse:
    """Get Last Meter Reading data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_LAST_METER_READING_URL.format(contract_id=contract_id, bp_number=bp_number),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return GetLastMeterReadingResponse.from_dict(response.json())


def get_devices(token: JWT, bp_number: str) -> list[Device]:
    """Get Device data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEVICES_URL.format(bp_number=bp_number),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    return [Device.from_dict(device) for device in response.json()]


def get_devices_by_contract_id(token: JWT, bp_number: str, contract_id: str) -> Devices:
    """Get Device data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEVICES_BY_CONTRACT_ID_URL.format(bp_number=bp_number, contract_id=contract_id),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    res = GetDeviceResponse.from_dict(response.json())
    return res.data


def get_device_type(token: JWT, bp_number: str, contract_id: str) -> DeviceType:
    """Get Device Type data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEVICE_TYPE_URL.format(bp_number=bp_number, contract_id=contract_id),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    return DeviceType.from_dict(response.json())


def get_billing_invoices(token: JWT, bp_number: str, contract_id: str) -> GetInvoicesBody:
    """Get Device Type data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_BILLING_INVOICES.format(bp_number=bp_number, contract_id=contract_id),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(response.status_code, response.reason)

    logger.debug("Response: %s", response.json())
    res = GetInvoicesResponse.from_dict(response.json())
    return res.data
