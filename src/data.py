import logging

import requests

from src.commons import add_jwt_to_headers
from src.const import (
    GET_BILLING_INVOICES,
    GET_CONSUMER_URL,
    GET_DEVICE_TYPE_URL,
    GET_DEVICES_BY_CONTRACT_ID_URL,
    GET_DEVICES_URL,
    GET_ELECTRIC_BILL_URL,
    GET_LAST_METER_READING_URL,
    GET_REQUEST_READING_URL,
    GET_SINGLE_CONTRACT_URL,
    HEADERS_WITH_AUTH,
)
from src.login import IECLoginError
from src.models.contract import GetContractResponse
from src.models.customer import Customer
from src.models.device import Device, Devices, GetDeviceResponse
from src.models.device_type import DeviceType, DeviceTypeResponse
from src.models.electric_bill import GetElectricBillResponse
from src.models.invoice import GetInvoicesBody, GetInvoicesResponse
from src.models.jwt import JWT
from src.models.meter_reading import GetLastMeterReadingResponse
from src.models.remote_reading import RemoteReadingRequest, RemoteReadingResponse
from src.models.response_descriptor import ErrorResponseDescriptor

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
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    return Customer.from_dict(response.json())


def get_remote_reading(token: JWT, meter_serial_number: str, meter_code: int, last_invoice_date: str, from_date: str,
                       resolution: int) -> RemoteReadingResponse:
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token.id_token)
    req = RemoteReadingRequest(meterSerialNumber=meter_serial_number, meterCode=meter_code,
                               lastInvoiceDate=last_invoice_date, fromDate=from_date, resolution=resolution)

    logger.debug("HTTP POST: %s", GET_REQUEST_READING_URL)
    response = requests.post(url=GET_REQUEST_READING_URL, data=req, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    return RemoteReadingResponse.from_dict(response.json())


def get_electric_bill(token: str, bp_number: str, contract_id: str) -> GetElectricBillResponse:
    """Get Electric Bill data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_ELECTRIC_BILL_URL.format(contract_id=contract_id, bp_number=bp_number),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    return GetElectricBillResponse.from_dict(response.json())


def get_contract(token: str, bp_number: str) -> GetContractResponse:
    """Get Electric Bill data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_SINGLE_CONTRACT_URL.format(bp_number=bp_number), headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    return GetContractResponse.from_dict(response.json())


def get_last_meter_reading(token: str, bp_number: str, contract_id: str) -> GetLastMeterReadingResponse:
    """Get Last Meter Reading data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_LAST_METER_READING_URL.format(contract_id=contract_id, bp_number=bp_number),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    return GetLastMeterReadingResponse.from_dict(response.json())


def get_devices(token: str, bp_number: str) -> list[Device]:
    """Get Device data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEVICES_URL.format(bp_number=bp_number),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    return [Device.from_dict(device) for device in response.json()]


def get_devices_by_contract_id(token: str, bp_number: str, contract_id: str) -> Devices:
    """Get Device data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEVICES_BY_CONTRACT_ID_URL.format(bp_number=bp_number, contract_id=contract_id),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    res = GetDeviceResponse.from_dict(response.json())
    return res.data


def get_device_type(token: str, bp_number: str, contract_id: str) -> DeviceType:
    """Get Device Type data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_DEVICE_TYPE_URL.format(bp_number=bp_number, contract_id=contract_id),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    resp = DeviceTypeResponse.from_dict(response.json())
    return resp.data


def get_billing_invoices(token: str, bp_number: str, contract_id: str) -> GetInvoicesBody:
    """Get Device Type data response from IEC API."""
    headers = add_jwt_to_headers(HEADERS_WITH_AUTH, token)
    # sending get request and saving the response as response object
    response = _get_url(url=GET_BILLING_INVOICES.format(bp_number=bp_number, contract_id=contract_id),
                        headers=headers)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    res = GetInvoicesResponse.from_dict(response.json())
    return res.data
