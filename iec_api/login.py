""" IEC Login Module. """
import asyncio
import concurrent.futures
import json
import random
import re
import string
from logging import getLogger
from typing import Tuple

import jwt
import pkce
from aiohttp import ClientSession

from iec_api.commons import send_get_request, send_post_request
from iec_api.models.exceptions import IECLoginError
from iec_api.models.jwt import JWT

APP_CLIENT_ID = "0oaqf6zr7yEcQZqqt2p7"
CODE_CHALLENGE_METHOD = "S256"
APP_REDIRECT_URI = "com.iecrn:/"
code_verifier, code_challenge = pkce.generate_pkce_pair()
STATE = "".join(random.choice(string.digits + string.ascii_letters) for _ in range(12))
IEC_OKTA_BASE_URL = "https://iec-ext.okta.com"

AUTHORIZE_URL = ("https://iec-ext.okta.com/oauth2/default/v1/authorize?client_id={"
                 "client_id}&response_type=id_token+code&response_mode=form_post&scope=openid%20email%20profile"
                 "%20offline_access&redirect_uri=com.iecrn:/&state=123abc&nonce=abc123&code_challenge_method=S256"
                 "&sessionToken={sessionToken}&code_challenge={challenge}")

logger = getLogger(__name__)


async def authorize_session(session: ClientSession, session_token: str) -> str:
    """
    Authorizes a session using the provided session token.
    Args:
        session (ClientSession): Client Session
        session_token (str): The session token to be used for authorization.
    Returns:
        str: The code obtained from the authorization response.
    """
    cmd_url = AUTHORIZE_URL.format(client_id=APP_CLIENT_ID, sessionToken=session_token, challenge=code_challenge)
    authorize_response = await send_get_request(session, cmd_url, timeout=10)
    code = re.findall(r"<input type=\"hidden\" name=\"code\" value=\"(.+)\"/>",
                      authorize_response.get('content').decode('unicode-escape')
                      .encode('latin1').decode('utf-8'))[0]
    return code


async def get_first_factor_id(session: ClientSession, user_id: str):
    """
    Function to get the first factor ID using the provided ID.
        Args:
        id (str): The user ID be used for authorization.
    Returns:
        Tuple[str,str]: [The state token, the factor id]
    """
    data = {"username": f"{user_id}@iec.co.il"}
    headers = {"accept": "application/json", "content-type": "application/json"}

    response = await send_post_request(session, f"{IEC_OKTA_BASE_URL}/api/v1/authn", json_data=data, headers=headers,
                                       timeout=10)
    return response.get("stateToken", ""), response.get("_embedded", {}).get("factors", {})[0].get("id")


async def send_otp_code(session: ClientSession, factor_id: object, state_token: object,
                        pass_code: object = None) -> str | None:
    """
    Send OTP code for factor verification and return the session token if successful.

    Args:
        session (ClientSession): Client Session
        factor_id (object): The identifier of the factor for verification.
        state_token (object): The state token for the verification process.
        pass_code (object, optional): The pass code for verification. Defaults to None.

    Returns:
        str | None: The session token if verification is successful, otherwise None.
    """
    data = {"stateToken": state_token}
    if pass_code:
        data["passCode"] = pass_code
    headers = {"accept": "application/json", "content-type": "application/json"}

    response = await send_post_request(
        session,
        f"{IEC_OKTA_BASE_URL}/api/v1/authn/factors/{factor_id}/verify", json_data=data,
        headers=headers, timeout=10
    )
    if response.get("status") == "SUCCESS":
        return response.get("sessionToken")
    return None


async def get_access_token(session: ClientSession, code: str) -> JWT:
    """
    Get the access token using the provided authorization code.
    Args:
        session (ClientSession): Client Session
        code (str): The authorization code.
    Returns:
        JWT: The access token as a JWT object.
    """
    data = {
        "client_id": APP_CLIENT_ID,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": APP_REDIRECT_URI,
        "code": code,
    }
    response = await send_post_request(session, f"{IEC_OKTA_BASE_URL}/oauth2/default/v1/token",
                                       data=data, timeout=10)
    return JWT.from_dict(response)


async def first_login(session: ClientSession, id_number: str) -> Tuple[str, str, str]:
    """
    Perform the first login for a user.

    Args:
        session (ClientSession): Client Session
        id_number (str): The user's ID number.

    Returns:
        Tuple[str, str, str]: A tuple containing the state token, factor ID, and session token.
    """

    try:
        # Get the first factor ID and state token
        state_token, factor_id = await get_first_factor_id(session, id_number)

        # Send OTP code and get session token
        session_token = await send_otp_code(session, factor_id, state_token)

        return state_token, factor_id, session_token
    except Exception as error:
        logger.warning("Failed at first login: %s", error)
        raise IECLoginError(-1, "Failed at first login")


async def verify_otp_code(session: ClientSession, factor_id: str, state_token: str, otp_code: str) -> JWT:
    """
    Verify the OTP code for the given factor_id, state_token, and otp_code and return the JWT.

    Args:
        session (ClientSession): Client Session
        factor_id (str): The factor ID for the OTP verification.
        state_token (str): The state token for the OTP verification.
        otp_code (str): The OTP code to be verified.

    Returns:
        JWT: The JSON Web Token (JWT) for the authorized session.
    """
    try:
        otp_session_token = await send_otp_code(session, factor_id, state_token, otp_code)
        code = await authorize_session(session, otp_session_token)
        jwt_token = await get_access_token(session, code)
        return jwt_token
    except Exception as error:
        logger.warning("Failed at OTP verification: %s", error)
        raise IECLoginError(-1, "Failed at OTP verification")


async def manual_authorization(session: ClientSession, id_number: str | int) -> JWT | None:  # pragma: no cover
    """Get authorization token from IEC API."""
    if not id_number:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            id_number = await asyncio.get_event_loop().run_in_executor(pool, input, "Enter your ID Number: ")
    state_token, factor_id, session_token = await first_login(session, str(id_number))
    if not state_token:
        logger.error("Failed to send OTP")
        return None

    with concurrent.futures.ThreadPoolExecutor() as pool:
        otp_code = await asyncio.get_event_loop().run_in_executor(pool, input, "Enter your OTP code: ")
    code = await authorize_session(session, otp_code)
    jwt_token = await verify_otp_code(session, factor_id, state_token, code)
    logger.debug(f"Access token: {jwt_token.access_token}\n"
                 f"Refresh token: {jwt_token.refresh_token}\n"
                 f"id_token: {jwt_token.id_token}")
    return jwt_token


async def refresh_token(session: ClientSession, token: JWT) -> JWT | None:
    """Refresh IEC JWT token."""
    headers = {"accept": "application/json", "content-type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": APP_CLIENT_ID,
        "redirect_uri": APP_REDIRECT_URI,
        "refresh_token": token.refresh_token,
        "grant_type": "refresh_token",
        "scope": "openid email profile offline_access"
    }
    response = await send_post_request(session, f"{IEC_OKTA_BASE_URL}/oauth2/default/v1/token", data=data,
                                       headers=headers, timeout=10)
    return JWT.from_dict(response)


def save_token_to_file(token: JWT, path: str = "token.json") -> None:
    """Save token to file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(token.to_dict(), f)


def load_token_from_file(path: str = "token.json") -> JWT:
    """Load token from file."""
    with open(path, "r", encoding="utf-8") as f:
        jwt_data = JWT.from_dict(json.load(f))
        jwt.decode(jwt_data.access_token, options={"verify_signature": False}, algorithms=["RS256"])
        return jwt_data
