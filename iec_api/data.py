import logging
from datetime import datetime
from typing import List, Optional, TypeVar

from aiohttp import ClientSession
from mashumaro.codecs import BasicDecoder

from iec_api import commons
from iec_api.const import (
    GET_ACCOUNTS_URL,
    GET_BILLING_INVOICES_URL,
    GET_CHECK_CONTRACT_URL,
    GET_CONSUMER_URL,
    GET_CONTRACTS_URL,
    GET_DEFAULT_CONTRACT_URL,
    GET_DEVICE_BY_DEVICE_ID_URL,
    GET_DEVICE_TYPE_URL,
    GET_DEVICES_URL,
    GET_EFS_MESSAGES_URL,
    GET_ELECTRIC_BILL_URL,
    GET_INVOICE_PDF_URL,
    GET_LAST_METER_READING_URL,
    GET_OUTAGES_URL,
    GET_REQUEST_READING_URL,
    GET_TENANT_IDENTITY_URL,
    HEADERS_WITH_AUTH,
)
from iec_api.models.account import Account
from iec_api.models.account import decoder as account_decoder
from iec_api.models.contract import Contract, Contracts
from iec_api.models.contract import decoder as contract_decoder
from iec_api.models.contract_check import ContractCheck
from iec_api.models.contract_check import decoder as contract_check_decoder
from iec_api.models.customer import Customer
from iec_api.models.device import Device, Devices
from iec_api.models.device import decoder as devices_decoder
from iec_api.models.device_identity import DeviceDetails, DeviceIdentity
from iec_api.models.device_identity import decoder as device_identity_decoder
from iec_api.models.device_type import DeviceType
from iec_api.models.device_type import decoder as device_type_decoder
from iec_api.models.efs import EfsMessage, EfsRequestAllServices, EfsRequestSingleService
from iec_api.models.efs import decoder as efs_decoder
from iec_api.models.electric_bill import ElectricBill
from iec_api.models.electric_bill import decoder as electric_bill_decoder
from iec_api.models.exceptions import IECError
from iec_api.models.get_pdf import GetPdfRequest
from iec_api.models.invoice import GetInvoicesBody
from iec_api.models.invoice import decoder as invoice_decoder
from iec_api.models.jwt import JWT
from iec_api.models.meter_reading import MeterReadings
from iec_api.models.meter_reading import decoder as meter_reading_decoder
from iec_api.models.outages import Outage
from iec_api.models.outages import decoder as outages_decoder
from iec_api.models.remote_reading import ReadingResolution, RemoteReadingRequest, RemoteReadingResponse
from iec_api.models.response_descriptor import ResponseWithDescriptor

T = TypeVar("T")
logger = logging.getLogger(__name__)


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


async def _post_response_with_descriptor(
    session: ClientSession,
    jwt_token: JWT,
    request_url: str,
    json_data: Optional[dict],
    decoder: BasicDecoder[ResponseWithDescriptor[T]],
) -> T:
    """
    A function to retrieve a response with a descriptor using a JWT token and a URL.

    Args:
        jwt_token (JWT): The JWT token used for authentication.
        request_url (str): The URL to send the request to.
        json_data (dict): POST content

    Returns:
        T: The response with a descriptor, with its type specified by the return type annotation.
    """
    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, jwt_token.id_token)
    response = await commons.send_post_request(session=session, url=request_url, headers=headers, json_data=json_data)

    response_with_descriptor = decoder.decode(response)

    if not response_with_descriptor.data and not response_with_descriptor.response_descriptor.is_success:
        raise IECError(
            response_with_descriptor.response_descriptor.code, response_with_descriptor.response_descriptor.description
        )

    return response_with_descriptor.data


async def get_accounts(session: ClientSession, token: JWT) -> Optional[List[Account]]:
    """Get Accounts response from IEC API."""
    return await _get_response_with_descriptor(session, token, GET_ACCOUNTS_URL, account_decoder)


async def get_customer(session: ClientSession, token: JWT) -> Optional[Customer]:
    """Get customer data response from IEC API."""
    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(session=session, url=GET_CONSUMER_URL, headers=headers)

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


async def get_efs_messages(
    session: ClientSession, token: JWT, contract_id: str, service_code: Optional[int] = None
) -> Optional[List[EfsMessage]]:
    """Get EFS Messages response from IEC API."""
    if service_code:
        req = EfsRequestSingleService(contract_number=contract_id, process_type=1, service_code=f"EFS{service_code:03}")
    else:
        req = EfsRequestAllServices(contract_number=contract_id, process_type=1)

    url = GET_EFS_MESSAGES_URL

    return await _post_response_with_descriptor(session, token, url, json_data=req.to_dict(), decoder=efs_decoder)


async def get_electric_bill(
    session: ClientSession, token: JWT, bp_number: str, contract_id: str
) -> Optional[ElectricBill]:
    """Get Electric Bill data response from IEC API."""
    return await _get_response_with_descriptor(
        session,
        token,
        GET_ELECTRIC_BILL_URL.format(contract_id=contract_id, bp_number=bp_number),
        electric_bill_decoder,
    )


async def get_default_contract(session: ClientSession, token: JWT, bp_number: str) -> Optional[Contract]:
    """Get Contract data response from IEC API."""
    return await _get_response_with_descriptor(
        session, token, GET_DEFAULT_CONTRACT_URL.format(bp_number=bp_number), contract_decoder
    )


async def get_contracts(session: ClientSession, token: JWT, bp_number: str) -> Optional[Contracts]:
    """Get all user's Contracts from IEC API."""
    return await _get_response_with_descriptor(
        session, token, GET_CONTRACTS_URL.format(bp_number=bp_number), contract_decoder
    )


async def get_contract_check(session: ClientSession, token: JWT, contract_id: str) -> Optional[ContractCheck]:
    """Get Contract Check response from IEC API."""
    return await _get_response_with_descriptor(
        session, token, GET_CHECK_CONTRACT_URL.format(contract_id=contract_id), contract_check_decoder
    )


async def get_last_meter_reading(
    session: ClientSession, token: JWT, bp_number: str, contract_id: str
) -> Optional[MeterReadings]:
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

    return [Device.from_dict(device) for device in response]


async def get_device_details(session: ClientSession, token: JWT, device_id: str) -> Optional[List[DeviceDetails]]:
    """Get Device Details response from IEC API."""
    device_identity: DeviceIdentity = await _get_response_with_descriptor(
        session, token, GET_TENANT_IDENTITY_URL.format(device_id=device_id), device_identity_decoder
    )

    return device_identity.device_details if device_identity else None


async def get_device_details_by_code(
    session: ClientSession, token: JWT, device_id: str, device_code: str
) -> Optional[DeviceDetails]:
    """Get Device Details response from IEC API."""
    devices = await get_device_details(session, token, device_id)

    return next((device for device in devices if device.device_code == device_code), None)


async def get_device_by_device_id(
    session: ClientSession, token: JWT, contract_id: str, device_id: str
) -> Optional[Devices]:
    """Get Device data response from IEC API."""
    return await _get_response_with_descriptor(
        session,
        token,
        GET_DEVICE_BY_DEVICE_ID_URL.format(device_id=device_id, contract_id=contract_id),
        devices_decoder,
    )


async def get_device_type(session: ClientSession, token: JWT, bp_number: str, contract_id: str) -> Optional[DeviceType]:
    """Get Device Type data response from IEC API."""
    # sending get request and saving the response as response object
    return await _get_response_with_descriptor(
        session, token, GET_DEVICE_TYPE_URL.format(bp_number=bp_number, contract_id=contract_id), device_type_decoder
    )


async def get_billing_invoices(
    session: ClientSession, token: JWT, bp_number: str, contract_id: str
) -> Optional[GetInvoicesBody]:
    """Get Device Type data response from IEC API."""
    return await _get_response_with_descriptor(
        session, token, GET_BILLING_INVOICES_URL.format(bp_number=bp_number, contract_id=contract_id), invoice_decoder
    )


async def get_invoice_pdf(
    session: ClientSession, token: JWT, bp_number: int | str, contract_id: int | str, invoice_number: int | str
) -> bytes:
    """Get Invoice PDF response from IEC API."""
    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    headers = headers.copy()  # don't modify original headers
    headers.update({"accept": "application/pdf", "content-type": "application/json"})

    request = GetPdfRequest(
        invoice_number=str(invoice_number), contract_id=str(contract_id), bp_number=str(bp_number)
    ).to_dict()
    response = await commons.send_non_json_post_request(
        session, url=GET_INVOICE_PDF_URL, headers=headers, json_data=request
    )
    return await response.read()


async def get_outages_by_account(session: ClientSession, token: JWT, account_id: str) -> Optional[list[Outage]]:
    """Get Device Type data response from IEC API."""
    return await _get_response_with_descriptor(
        session, token, GET_OUTAGES_URL.format(account_id=account_id), outages_decoder
    )
