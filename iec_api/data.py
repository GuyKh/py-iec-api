from datetime import datetime
from typing import Optional, TypeVar

from aiohttp import ClientSession
from loguru import logger
from mashumaro.codecs import BasicDecoder

from iec_api import commons
from iec_api.const import (
    GET_ACCOUNTS_URL,
    GET_BILLING_INVOICES,
    GET_CONSUMER_URL,
    GET_CONTRACTS_URL,
    GET_DEFAULT_CONTRACT_URL,
    GET_DEVICE_BY_DEVICE_ID_URL,
    GET_DEVICE_TYPE_URL,
    GET_DEVICES_URL,
    GET_ELECTRIC_BILL_URL,
    GET_LAST_METER_READING_URL,
    GET_REQUEST_READING_URL,
    HEADERS_WITH_AUTH,
)
from iec_api.models.account import Account
from iec_api.models.account import decoder as account_decoder
from iec_api.models.contract import Contract, Contracts
from iec_api.models.contract import decoder as contract_decoder
from iec_api.models.customer import Customer
from iec_api.models.device import Device, Devices
from iec_api.models.device import decoder as devices_decoder
from iec_api.models.device_type import DeviceType
from iec_api.models.device_type import decoder as device_type_decoder
from iec_api.models.electric_bill import ElectricBill
from iec_api.models.electric_bill import decoder as electric_bill_decoder
from iec_api.models.exceptions import IECError
from iec_api.models.invoice import GetInvoicesBody
from iec_api.models.invoice import decoder as invoice_decoder
from iec_api.models.jwt import JWT
from iec_api.models.meter_reading import MeterReadings
from iec_api.models.meter_reading import decoder as meter_reading_decoder
from iec_api.models.remote_reading import ReadingResolution, RemoteReadingRequest, RemoteReadingResponse
from iec_api.models.response_descriptor import ResponseWithDescriptor

T = TypeVar("T")


async def _get_response_with_descriptor(
    session: ClientSession, jwt_token: JWT, request_url: str, decoder: BasicDecoder[ResponseWithDescriptor[T]]
) -> T:
    """
    A function to retrieve a response with a descriptor using a JWT token and a URL.

    Args:
        jwt_token (JWT): The JWT token used for authentication.
        request_url (str): The URL to send the request to.

    Returns:
        T: The response with a descriptor, with its type specified by the return type annotation.
    """
    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, jwt_token.id_token)
    response = await commons.send_get_request(session=session, url=request_url, headers=headers)

    response_with_descriptor = decoder.decode(response)

    if not response_with_descriptor.data and not response_with_descriptor.response_descriptor.is_success:
        raise IECError(
            response_with_descriptor.response_descriptor.code, response_with_descriptor.response_descriptor.description
        )

    return response_with_descriptor.data


async def get_accounts(session: ClientSession, token: JWT) -> list[Account]:
    """Get Accounts response from IEC API."""
    return await _get_response_with_descriptor(session, token, GET_ACCOUNTS_URL, account_decoder)


async def get_customer(session: ClientSession, token: JWT) -> Optional[Customer]:
    """Get customer data response from IEC API."""
    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(session=session, url=GET_CONSUMER_URL, headers=headers)

    logger.debug(f"Response: {response}")
    return Customer.from_dict(response)


async def get_remote_reading(
    session: ClientSession,
    token: JWT,
    contract_id: str,
    meter_serial_number: str,
    meter_code: int,
    last_invoice_date: datetime,
    from_date: datetime,
    resolution: ReadingResolution = ReadingResolution.DAILY,
) -> Optional[RemoteReadingResponse]:
    req = RemoteReadingRequest(
        meter_serial_number=meter_serial_number,
        meter_code=str(meter_code),
        last_invoice_date=last_invoice_date.strftime("%Y-%m-%d"),
        from_date=from_date.strftime("%Y-%m-%d"),
        resolution=resolution,
    )

    url = GET_REQUEST_READING_URL.format(contract_id=contract_id)
    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)

    response = await commons.send_post_request(session=session, url=url, headers=headers, json_data=req.to_dict())

    return RemoteReadingResponse.from_dict(response)


async def get_electric_bill(session: ClientSession, token: JWT, bp_number: str, contract_id: str) -> ElectricBill:
    """Get Electric Bill data response from IEC API."""
    return await _get_response_with_descriptor(
        session,
        token,
        GET_ELECTRIC_BILL_URL.format(contract_id=contract_id, bp_number=bp_number),
        electric_bill_decoder,
    )


async def get_default_contract(session: ClientSession, token: JWT, bp_number: str) -> Contract:
    """Get Contract data response from IEC API."""
    return await _get_response_with_descriptor(
        session, token, GET_DEFAULT_CONTRACT_URL.format(bp_number=bp_number), contract_decoder
    )


async def get_contracts(session: ClientSession, token: JWT, bp_number: str) -> Contracts:
    """Get all user's Contracts from IEC API."""
    return await _get_response_with_descriptor(
        session, token, GET_CONTRACTS_URL.format(bp_number=bp_number), contract_decoder
    )


async def get_last_meter_reading(session: ClientSession, token: JWT, bp_number: str, contract_id: str) -> MeterReadings:
    """Get Last Meter Reading data response from IEC API."""
    return await _get_response_with_descriptor(
        session,
        token,
        GET_LAST_METER_READING_URL.format(contract_id=contract_id, bp_number=bp_number),
        meter_reading_decoder,
    )


async def get_devices(session: ClientSession, token: JWT, contract_id: str) -> list[Device]:
    """Get Device data response from IEC API."""
    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_DEVICES_URL.format(contract_id=contract_id), headers=headers
    )

    logger.debug(f"Response: {response}")
    return [Device.from_dict(device) for device in response]


async def get_device_by_device_id(session: ClientSession, token: JWT, contract_id: str, device_id: str) -> Devices:
    """Get Device data response from IEC API."""
    return await _get_response_with_descriptor(
        session,
        token,
        GET_DEVICE_BY_DEVICE_ID_URL.format(device_id=device_id, contract_id=contract_id),
        devices_decoder,
    )


async def get_device_type(session: ClientSession, token: JWT, bp_number: str, contract_id: str) -> DeviceType:
    """Get Device Type data response from IEC API."""
    # sending get request and saving the response as response object
    return await _get_response_with_descriptor(
        session, token, GET_DEVICE_TYPE_URL.format(bp_number=bp_number, contract_id=contract_id), device_type_decoder
    )


async def get_billing_invoices(session: ClientSession, token: JWT, bp_number: str, contract_id: str) -> GetInvoicesBody:
    """Get Device Type data response from IEC API."""
    return await _get_response_with_descriptor(
        session, token, GET_BILLING_INVOICES.format(bp_number=bp_number, contract_id=contract_id), invoice_decoder
    )
