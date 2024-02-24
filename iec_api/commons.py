import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
from json import JSONDecodeError
from logging import getLogger
from typing import Any, Optional

from aiohttp import ClientError, ClientSession

from iec_api.models.exceptions import IECError
from iec_api.models.response_descriptor import RESPONSE_DESCRIPTOR_FIELD, ErrorResponseDescriptor

logger = getLogger(__name__)


def add_jwt_to_headers(headers, token) -> dict:
    """
    Add JWT token to the headers' dictionary.
    Args:
    headers (dict): The headers dictionary to be modified.
    token (str): The JWT token to be added to the headers.
    Returns:
    dict: The modified headers dictionary with the JWT token added.
    """
    headers["Authorization"] = f"Bearer {token}"
    return headers


PHONE_REGEX: str = "^(+972|0)5[0-9]{8}$"


def check_phone(phone):
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


async def send_get_request(
    session: ClientSession, url: str, timeout: Optional[int] = 60, headers: Optional[dict] = None
) -> dict[str, Any]:
    try:
        if not headers:
            headers = session.headers

        if not timeout:
            timeout = session.timeout

        logger.debug("HTTP GET: %s", url)
        resp = await session.get(url=url, headers=headers, timeout=timeout)
        json_resp: dict = await resp.json(content_type=None)
    except TimeoutError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to time out: ({str(ex)})")
    except ClientError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise IECError(-1, f"Received invalid response from IEC API: {str(ex)}")

    logger.debug("HTTP GET Response: %s", json_resp)
    if resp.status != 200:
        logger.warning(f"Failed call: (Code {resp.status}): {resp.reason}")
        if len(json_resp) > 0 and json_resp.get(RESPONSE_DESCRIPTOR_FIELD) is not None:
            login_error_response = ErrorResponseDescriptor.from_dict(json_resp.get(RESPONSE_DESCRIPTOR_FIELD))
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(resp.status, resp.reason)

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

        logger.debug("HTTP GET: %s", url)
        resp = await session.get(url=url, headers=headers, timeout=timeout)
        resp_content = await resp.text(encoding=encoding)
    except TimeoutError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to time out: ({str(ex)})")
    except ClientError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise IECError(-1, f"Received invalid response from IEC API: {str(ex)}")

    logger.debug("HTTP GET Response: %s", resp_content)

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

        logger.debug("HTTP POST: %s", url)
        logger.debug("HTTP Content: %s", data or json_data)

        if data:
            resp = await session.post(url=url, data=data, headers=headers, timeout=timeout)
        else:
            if json_data:
                resp = await session.post(url=url, json=json_data, headers=headers, timeout=timeout)

        json_resp: dict = await resp.json(content_type=None)
    except TimeoutError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to time out: ({str(ex)})")
    except ClientError as ex:
        raise IECError(-1, f"Failed to communicate with IEC API due to ClientError: ({str(ex)})")
    except JSONDecodeError as ex:
        raise IECError(-1, f"Received invalid response from IEC API: {str(ex)}")

    logger.debug("HTTP POST Response: %s", json_resp)

    if resp.status != 200:
        logger.warning(f"Failed call: (Code {resp.status}): {resp.reason}")
        if len(json_resp) > 0 and json_resp.get(RESPONSE_DESCRIPTOR_FIELD) is not None:
            login_error_response = ErrorResponseDescriptor.from_dict(json_resp.get(RESPONSE_DESCRIPTOR_FIELD))
            raise IECError(login_error_response.code, login_error_response.error)
        else:
            raise IECError(resp.status, resp.reason)

    return json_resp
