from typing import List

from aiohttp import ClientSession

from iec_api import commons
from iec_api.const import (
    GET_MASA_CITIES_LOOKUP_URL,
    GET_MASA_EQUIPMENTS_URL,
    GET_MASA_LOOKUP_URL,
    GET_MASA_ORDER_LOOKUP_URL,
    GET_MASA_ORDER_TITLES_URL,
    GET_MASA_USER_PROFILE_LOOKUP_URL,
    GET_MASA_VOLT_LEVELS_URL,
    HEADERS_WITH_AUTH,
)
from iec_api.masa_api_models.cities import CitiesResponse, City
from iec_api.masa_api_models.equipment import GetEquipmentResponse
from iec_api.masa_api_models.lookup import GetLookupResponse
from iec_api.masa_api_models.order_lookup import OrderCategory, OrderLookupResponse
from iec_api.masa_api_models.titles import GetTitleResponse
from iec_api.masa_api_models.user_profile import MasaUserProfile
from iec_api.masa_api_models.volt_levels import VoltLevel, VoltLevelsResponse
from iec_api.models.jwt import JWT


async def get_masa_cities(session: ClientSession, token: JWT) -> List[City]:
    """Get Cities from IEC Masa API."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_MASA_CITIES_LOOKUP_URL, headers=headers
    )

    return CitiesResponse.from_dict(response).data_collection


async def get_masa_order_categories(session: ClientSession, token: JWT) -> List[OrderCategory]:
    """Get Order Categories from IEC Masa API."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_MASA_ORDER_LOOKUP_URL, headers=headers
    )

    return OrderLookupResponse.from_dict(response).order_categories


async def get_masa_user_profile(session: ClientSession, token: JWT, account_id: str) -> MasaUserProfile:
    """Get User Profile from IEC Masa API."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_MASA_USER_PROFILE_LOOKUP_URL.format(account_id=account_id), headers=headers
    )

    return MasaUserProfile.from_dict(response)


async def get_masa_equipments(session: ClientSession, token: JWT, account_id: str) -> GetEquipmentResponse:
    """Get Equimpents from IEC Masa API."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_MASA_EQUIPMENTS_URL.format(account_id=account_id), headers=headers
    )

    return GetEquipmentResponse.from_dict(response)


async def get_masa_volt_levels(session: ClientSession, token: JWT) -> List[VoltLevel]:
    """Get Volt Levels from IEC Masa API."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_MASA_VOLT_LEVELS_URL, headers=headers
    )

    return VoltLevelsResponse.from_dict(response).data_collection


async def get_masa_order_titles(session: ClientSession, token: JWT) -> GetTitleResponse:
    """Get Order Title from IEC Masa API."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_MASA_ORDER_TITLES_URL, headers=headers
    )

    return GetTitleResponse.from_dict(response)

async def get_masa_lookup(session: ClientSession, token: JWT) -> GetLookupResponse:
    """Get All Lookup from IEC Masa API."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_MASA_LOOKUP_URL, headers=headers
    )

    return GetLookupResponse.from_dict(response)
