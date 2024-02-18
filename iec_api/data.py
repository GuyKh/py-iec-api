import logging
from typing import Any

from aiohttp import ClientSession

from iec_api.commons import send_get_request, send_post_request
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
)
from iec_api.models.contract import GetContractResponse
from iec_api.models.customer import Customer
from iec_api.models.device import Device, Devices, GetDeviceResponse
from iec_api.models.device_type import DeviceType
from iec_api.models.electric_bill import GetElectricBillResponse
from iec_api.models.invoice import GetInvoicesBody, GetInvoicesResponse
from iec_api.models.jwt import JWT
from iec_api.models.meter_reading import GetLastMeterReadingResponse
from iec_api.models.remote_reading import RemoteReadingRequest, RemoteReadingResponse

logger = logging.getLogger(__name__)


async def _get_url(session, url) -> dict[str, Any]:
    logger.debug("HTTP GET: %s", url)
    return await send_get_request(session, url, timeout=10)


async def get_customer(session: ClientSession, token: JWT) -> Customer:
    """Get customer data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session, url=GET_CONSUMER_URL)

    logger.debug("Response: %s", response)
    return Customer.from_dict(response)


async def get_remote_reading(session: ClientSession, token: JWT, meter_serial_number: str, meter_code: int,
                             last_invoice_date: str, from_date: str,
                             resolution: int) -> RemoteReadingResponse:

    req = RemoteReadingRequest(meter_serial_number, meter_code,
                               last_invoice_date, from_date, resolution)

    response = await send_post_request(session, url=GET_REQUEST_READING_URL, data=RemoteReadingRequest.to_dict(req),
                                       timeout=10)

    logger.debug("Response: %s", response)
    return RemoteReadingResponse.from_dict(response)


async def get_electric_bill(session: ClientSession, token: JWT, bp_number: str,
                            contract_id: str) -> GetElectricBillResponse:
    """Get Electric Bill data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session, url=GET_ELECTRIC_BILL_URL.format(contract_id=contract_id, bp_number=bp_number))

    logger.debug("Response: %s", response)
    return GetElectricBillResponse.from_dict(response)


async def get_default_contract(session: ClientSession, token: JWT, bp_number: str) -> GetContractResponse:
    """Get Electric Bill data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session, url=GET_DEFAULT_CONTRACT_URL.format(bp_number=bp_number))

    logger.debug("Response: %s", response)
    return GetContractResponse.from_dict(response)


async def get_contracts(session: ClientSession, token: JWT, bp_number: str) -> GetContractResponse:
    """Get Electric Bill data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session, url=GET_CONTRACTS_URL.format(bp_number=bp_number))

    logger.debug("Response: %s", response)
    return GetContractResponse.from_dict(response)


async def get_last_meter_reading(session: ClientSession, token: JWT, bp_number: str,
                                 contract_id: str) -> GetLastMeterReadingResponse:
    """Get Last Meter Reading data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session,
                              url=GET_LAST_METER_READING_URL.format(contract_id=contract_id, bp_number=bp_number))

    logger.debug("Response: %s", response)
    return GetLastMeterReadingResponse.from_dict(response)


async def get_devices(session: ClientSession, token: JWT, bp_number: str) -> list[Device]:
    """Get Device data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session, url=GET_DEVICES_URL.format(bp_number=bp_number))

    logger.debug("Response: %s", response)
    devices: list[dict] = response

    return [Device.from_dict(device) for device in devices]


async def get_devices_by_contract_id(session: ClientSession, token: JWT, bp_number: str, contract_id: str) -> Devices:
    """Get Device data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session,
                              url=GET_DEVICES_BY_CONTRACT_ID_URL.format(bp_number=bp_number, contract_id=contract_id))

    logger.debug("Response: %s", response)
    res = GetDeviceResponse.from_dict(response)
    return res.data


async def get_device_type(session: ClientSession, token: JWT, bp_number: str, contract_id: str) -> DeviceType:
    """Get Device Type data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session, url=GET_DEVICE_TYPE_URL.format(bp_number=bp_number, contract_id=contract_id))

    return DeviceType.from_dict(response)


async def get_billing_invoices(session: ClientSession, token: JWT, bp_number: str, contract_id: str) -> GetInvoicesBody:
    """Get Device Type data response from IEC API."""

    # sending get request and saving the response as response object
    response = await _get_url(session, url=GET_BILLING_INVOICES.format(bp_number=bp_number, contract_id=contract_id))

    logger.debug("Response: %s", response)
    res = GetInvoicesResponse.from_dict(response)
    return res.data
