import asyncio
import http
import re
from concurrent.futures import ThreadPoolExecutor
from json import JSONDecodeError
from typing import Any, Optional

from aiohttp import ClientError, ClientResponse, ClientSession
from loguru import logger

from iec_api.models.exceptions import IECError, IECLoginError
from iec_api.models.okta_errors import OktaError
from iec_api.models.response_descriptor import RESPONSE_DESCRIPTOR_FIELD, ErrorResponseDescriptor


def add_auth_bearer_to_headers(headers: dict[str, str], token: str) -> dict[str, str]:
    """
    Add JWT bearer token to the Authorization header.
    Args:
    headers (dict): The headers dictionary to be modified.
    token (str): The JWT token to be added to the headers.
    Returns:
    dict: The modified headers dictionary with the JWT token added.
    """
    headers["Authorization"] = f"Bearer {token}"
    return headers


PHONE_REGEX = "^(+972|0)5[0-9]{8}$"


def check_phone(phone: str):
    """
    Check if the phone number is valid.
    Args:
    phone (str): The phone number to be checked.
    Returns:
    bool: True if the phone number is valid, False otherwise.
    """
    if not phone or not re.match(PHONE_REGEX, phone):
        raise ValueError("Invalid phone number")


def is_valid_israeli_id(id_number: str | int) -> bool:
    """
    Check if the ID number is valid.
    Args:
    id_number (str): The ID number to be checked.
    Returns:
    bool: True if the ID number is valid, False otherwise.
    """

    id_str = str(id_number).strip()
    if len(id_str) > 9 or not id_str.isdigit():
        return False
    id_str = id_str.zfill(9)
    return (
        sum(
            (int(digit) if i % 2 == 0 else int(digit) * 2 if int(digit) * 2 < 10 else int(digit) * 2 - 9)
            for i, digit in enumerate(id_str)
        )
        % 10
        == 0
    )


async def read_user_input(prompt: str) -> str:
    with ThreadPoolExecutor(1, "AsyncInput") as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)


def parse_error_response(resp: ClientResponse, json_resp: dict[str, Any]):
    """
    A function to parse error responses from IEC or Okta Server
    """
    logger.warning(f"Failed call: (Code {resp.status}): {resp.reason}")
    if len(json_resp) > 0:
        if json_resp.get(RESPONSE_DESCRIPTOR_FIELD) is not None:
            login_error_response = ErrorResponseDescriptor.from_dict(json_resp.get(RESPONSE_DESCRIPTOR_FIELD))
            raise IECError(login_error_response.code, login_error_response.error)
        elif json_resp.get("errorSummary") is not None:
            login_error_response = OktaError.from_dict(json_resp)
            raise IECLoginError(resp.status, resp.reason + ": " + login_error_response.error_summary)
    raise IECError(resp.status, resp.reason)


async def send_get_request(
    session: ClientSession, url: str, timeout: Optional[int] = 60, headers: Optional[dict] = None
) -> dict[str, Any]:
    try:
        if not headers:
            headers = session.headers

        if not timeout:
            timeout = session.timeout

        logger.debug(f"HTTP GET: {url}")
        resp = await session.get(url=url, headers=headers, timeout=timeout)
        json_resp: dict = await resp.json(content_type=None)
    except TimeoutError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to time out: ({str(ex)})")
    except ClientError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise IECError(-1, f"Received invalid response from IEC API: {str(ex)}")

    logger.debug(f"HTTP GET Response: {json_resp}")
    if resp.status != http.HTTPStatus.OK:
        parse_error_response(resp, json_resp)

    return json_resp


async def send_non_json_get_request(
    session: ClientSession,
    url: str,
    timeout: Optional[int] = 60,
    headers: Optional[dict] = None,
    encoding: Optional[str] = None,
) -> str:
    try:
        if not headers:
            headers = session.headers

        if not timeout:
            timeout = session.timeout

        logger.debug(
            f"HTTP GET: {url}",
        )
        resp = await session.get(url=url, headers=headers, timeout=timeout)
        resp_content = await resp.text(encoding=encoding)
    except TimeoutError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to time out: ({str(ex)})")
    except ClientError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise IECError(-1, f"Received invalid response from IEC API: {str(ex)}")

    logger.debug(f"HTTP GET Response: {resp_content}")

    return resp_content


async def send_post_request(
    session: ClientSession,
    url: str,
    timeout: Optional[int] = 60,
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    json_data: Optional[dict] = None,
) -> dict[str, Any]:
    try:
        if not headers:
            headers = session.headers

        if not timeout:
            headers = session.timeout

        logger.debug(f"HTTP POST: {url}")
        logger.debug(f"HTTP Content: {data or json_data}")

        resp = await session.post(url=url, data=data, json=json_data, headers=headers, timeout=timeout)

        json_resp: dict = await resp.json(content_type=None)
    except TimeoutError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to time out: ({str(ex)})")
    except ClientError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise IECError(-1, f"Received invalid response from IEC API: {str(ex)}")

    logger.debug(f"HTTP POST Response: {json_resp}")

    if resp.status != http.HTTPStatus.OK:
        parse_error_response(resp, json_resp)
    return json_resp
