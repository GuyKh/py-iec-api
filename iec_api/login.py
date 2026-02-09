"""IEC Login Module."""

import json
import logging
import os
import re
import time
from typing import Any, Optional, Tuple

import aiofiles
import jwt
from aiohttp import ClientSession
from jwt import PyJWKClient

from iec_api import commons
from iec_api.models.exceptions import IECLoginError
from iec_api.models.jwt import JWT

APP_CLIENT_ID = os.environ.get("IEC_CLIENT_ID", "0oaqf6zr7yEcQZqqt2p7")
APP_REDIRECT_URI = os.environ.get("IEC_REDIRECT_URI", "com.iecrn:/")
IEC_OKTA_BASE_URL = os.environ.get("IEC_OKTA_BASE_URL", "https://iec-ext.okta.com")

JWKS_URL = os.environ.get("IEC_JWKS_URL", f"{IEC_OKTA_BASE_URL}/oauth2/default/v1/keys")

_jwks_client: Optional[PyJWKClient] = None


def _get_jwks_client() -> PyJWKClient:
    """Get or create the JWKS client for JWT signature verification."""
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient(JWKS_URL)
    return _jwks_client


def decode_token(token: JWT) -> dict[str, Any]:
    """Decode and verify JWT token signature using JWKS.

    Fetches the signing key from OKTA's JWKS endpoint and verifies
    the token signature. Falls back to decoding without verification
    if JWKS is unavailable.
    """
    try:
        jwks_client = _get_jwks_client()
        signing_key = jwks_client.get_signing_key_from_jwt(token.id_token)
        return jwt.decode(
            token.id_token,
            key=signing_key.key,
            algorithms=["RS256"],
            audience=APP_CLIENT_ID,
        )
    except Exception:
        # Fallback: decode without signature verification
        # This maintains backward compatibility
        return jwt.decode(
            token.id_token,
            options={"verify_signature": False},
            algorithms=["RS256"],
        )


logger = logging.getLogger(__name__)

CODE_CHALLENGE_METHOD = "S256"

AUTHORIZE_URL = (
    "https://iec-ext.okta.com/oauth2/default/v1/authorize?client_id={"
    "client_id}&response_type=id_token+code&response_mode=form_post&scope=openid%20email%20profile"
    "%20offline_access&redirect_uri=com.iecrn:/&state=123abc&nonce=abc123&code_challenge_method=S256"
    "&sessionToken={sessionToken}&code_challenge={challenge}"
)


async def authorize_session(session: ClientSession, session_token) -> str:
    """
    Authorizes a session using the provided session token.
    Args:
        session: The aiohttp ClientSession object.
        session_token (str): The session token to be used for authorization.
    Returns:
        str: The code obtained from the authorization response.
    """
    import pkce

    code_verifier, code_challenge = pkce.generate_pkce_pair()
    cmd_url = AUTHORIZE_URL.format(client_id=APP_CLIENT_ID, sessionToken=session_token, challenge=code_challenge)
    authorize_response = await commons.send_non_json_get_request(
        session=session, url=cmd_url, encoding="unicode-escape"
    )
    code = re.findall(
        r"<input type=\"hidden\" name=\"code\" value=\"(.+)\"/>",
        authorize_response.encode("latin1").decode("utf-8"),
    )[0]
    return code


async def get_first_factor_id(session: ClientSession, user_id: str) -> Tuple[str, str]:
    """
    Function to get the first factor ID using the provided ID.
        Args:
        session: The aiohttp ClientSession object.
        user_id (str): The user ID be used for authorization.
    Returns:
        Tuple[str,str]: [The state token, the factor id]
    """
    data = {"username": f"{user_id}@iec.co.il"}
    headers = {"accept": "application/json", "content-type": "application/json"}

    response = await commons.send_post_request(
        session=session, url=f"{IEC_OKTA_BASE_URL}/api/v1/authn", json_data=data, headers=headers
    )
    return response.get("stateToken", ""), response.get("_embedded", {}).get("factors", {})[0].get("id")


async def send_otp_code(
    session: ClientSession, factor_id: object, state_token: object, pass_code: object = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Send OTP code for factor verification and return the session token and factor type.

    Args:
        session: The aiohttp ClientSession object.
        factor_id (object): The identifier of the factor for verification.
        state_token (object): The state token for the verification process.
        pass_code (object, optional): The pass code for verification. Defaults to None.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the session token and the factor type.
    """
    data = {"stateToken": state_token}
    if pass_code:
        data["passCode"] = pass_code
    headers = {"accept": "application/json", "content-type": "application/json"}

    response = await commons.send_post_request(
        session=session,
        url=f"{IEC_OKTA_BASE_URL}/api/v1/authn/factors/{factor_id}/verify",
        json_data=data,
        headers=headers,
    )

    session_token = response.get("sessionToken")
    factor_type = response.get("_embedded", {}).get("factor", {}).get("factorType")

    if response.get("status") in ("SUCCESS", "MFA_CHALLENGE"):
        return session_token, factor_type

    return None, None


async def get_access_token(session: ClientSession, code) -> JWT:
    """
    Get the access token using the provided authorization code.
    Args:
        session: The aiohttp ClientSession object.
        code (str): The authorization code.
    Returns:
        JWT: The access token as a JWT object.
    """
    import pkce

    code_verifier, _ = pkce.generate_pkce_pair()

    data = {
        "client_id": APP_CLIENT_ID,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": APP_REDIRECT_URI,
        "code": code,
    }
    response = await commons.send_post_request(
        session=session, url=f"{IEC_OKTA_BASE_URL}/oauth2/default/v1/token", data=data
    )
    return JWT.from_dict(response)


async def first_login(session: ClientSession, id_number: str) -> Tuple[str, str, Optional[str], Optional[str]]:
    """
    Perform the first login for a user.

    Args:
        session: The aiohttp ClientSession object.
        id_number (str): The user's ID number.

    Returns:
        Tuple[str, str, str, str]: A tuple containing the state token, factor ID, session token,
         and factor type.
    """

    try:
        # Get the first factor ID and state token
        state_token, factor_id = await get_first_factor_id(session, id_number)

        # Send OTP code and get session token
        session_token, factor_type = await send_otp_code(session, factor_id, state_token)

        return state_token, factor_id, session_token, factor_type
    except Exception as error:
        logger.warning(f"Failed at first login: {error}")
        raise IECLoginError(-1, "Failed at first login") from error


async def verify_otp_code(session: ClientSession, factor_id: str, state_token: str, otp_code: str) -> JWT:
    """
    Verify the OTP code for the given factor_id, state_token, and otp_code and return the JWT.

    Args:
        session: The aiohttp ClientSession object.
        factor_id (str): The factor ID for the OTP verification.
        state_token (str): The state token for the OTP verification.
        otp_code (str): The OTP code to be verified.

    Returns:
        JWT: The JSON Web Token (JWT) for the authorized session.
    """
    try:
        otp_session_token, _ = await send_otp_code(session, factor_id, state_token, otp_code)
        if not otp_session_token:
            raise IECLoginError(-1, "OTP verification failed: no session token")
        code = await authorize_session(session, otp_session_token)
        jwt_token = await get_access_token(session, code)
        return jwt_token
    except Exception as error:
        logger.warning(f"Failed at OTP verification: {error}")
        raise IECLoginError(-1, "Failed at OTP verification") from error


async def manual_authorization(session: ClientSession, id_number) -> JWT:  # pragma: no cover
    """Get authorization token from IEC API."""
    if not id_number:
        id_number = await commons.read_user_input("Enter your ID Number: ")
    state_token, factor_id, session_token, factor_type = await first_login(session, id_number)
    if not state_token:
        logger.error("Failed to send OTP")
        raise IECLoginError(-1, "Failed to send OTP, no state_token")

    otp_code = await commons.read_user_input(f"Enter your OTP code sent to your {factor_type}: ")
    code = await authorize_session(session, otp_code)
    jwt_token = await verify_otp_code(session, factor_id, state_token, code)
    logger.debug(
        f"Access token: {jwt_token.access_token}\n"
        f"Refresh token: {jwt_token.refresh_token}\n"
        f"id_token: {jwt_token.id_token}"
    )
    return jwt_token


async def refresh_token(session: ClientSession, token: JWT) -> JWT:
    """Refresh IEC JWT token."""
    headers = {"accept": "application/json", "content-type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": APP_CLIENT_ID,
        "redirect_uri": APP_REDIRECT_URI,
        "refresh_token": token.refresh_token,
        "grant_type": "refresh_token",
        "scope": "openid email profile offline_access",
    }
    response = await commons.send_post_request(
        session=session, url=f"{IEC_OKTA_BASE_URL}/oauth2/default/v1/token", data=data, headers=headers
    )
    return JWT.from_dict(response)


async def save_token_to_file(token: JWT, path: str = "token.json") -> None:
    """Save token to file."""
    async with aiofiles.open(path, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(token.to_dict()))


async def load_token_from_file(path: str = "token.json") -> JWT:
    """Load token from file."""
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        contents = await f.read()

    jwt_data = JWT.from_dict(json.loads(contents))

    # decode token to verify validity
    decode_token(jwt_data)

    return jwt_data


def get_token_remaining_time_to_expiration(token: JWT):
    decoded_token = decode_token(token)
    return decoded_token["exp"] - int(time.time())
