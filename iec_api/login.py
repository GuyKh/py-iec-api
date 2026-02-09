"""IEC Login Module."""

import json
import logging
import os
import random
import re
import string
import time
from typing import Any, Optional, Tuple

import aiofiles
import jwt
import pkce
from aiohttp import ClientSession
from cryptography.fernet import Fernet
from jwt import PyJWKClient

from iec_api import commons
from iec_api.models.exceptions import IECLoginError
from iec_api.models.jwt import JWT

logger = logging.getLogger(__name__)


def _get_encryption_key() -> bytes | None:
    key = os.environ.get("IEC_TOKEN_ENCRYPTION_KEY")
    if key:
        return key.encode()
    return None


def _get_fernet() -> Fernet | None:
    key = _get_encryption_key()
    if key:
        return Fernet(key)
    return None


APP_CLIENT_ID = os.environ.get("IEC_CLIENT_ID", "0oaqf6zr7yEcQZqqt2p7")
CODE_CHALLENGE_METHOD = "S256"
APP_REDIRECT_URI = os.environ.get("IEC_REDIRECT_URI", "com.iecrn:/")
IEC_OKTA_BASE_URL = os.environ.get("IEC_OKTA_BASE_URL", "https://iec-ext.okta.com")

JWKS_URL = os.environ.get("IEC_JWKS_URL", f"{IEC_OKTA_BASE_URL}/oauth2/default/v1/keys")

_jwks_client: Optional[PyJWKClient] = None


def _get_jwks_client() -> PyJWKClient:
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient(JWKS_URL)
    return _jwks_client


def decode_token(token: JWT) -> dict[str, Any]:
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
        return jwt.decode(
            token.id_token,
            options={"verify_signature": False},
            algorithms=["RS256"],
        )


AUTHORIZE_URL = (
    "https://iec-ext.okta.com/oauth2/default/v1/authorize?client_id={"
    "client_id}&response_type=id_token+code&response_mode=form_post&scope=openid%20email%20profile"
    "%20offline_access&redirect_uri=com.iecrn:/&state={state}&nonce=abc123&code_challenge_method=S256"
    "&sessionToken={sessionToken}&code_challenge={challenge}"
)


async def authorize_session(session: ClientSession, session_token) -> Tuple[str, str]:
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    state = "".join(random.choice(string.digits + string.ascii_letters) for _ in range(12))

    cmd_url = AUTHORIZE_URL.format(
        client_id=APP_CLIENT_ID, sessionToken=session_token, challenge=code_challenge, state=state
    )
    authorize_response = await commons.send_non_json_get_request(
        session=session, url=cmd_url, encoding="unicode-escape"
    )
    code = re.findall(
        r"<input type=\"hidden\" name=\"code\" value=\"(.+)\"\/>",
        authorize_response.encode("latin1").decode("utf-8"),
    )[0]
    return code, code_verifier


async def get_first_factor_id(session: ClientSession, user_id: str) -> Tuple[str, str]:
    data = {"username": f"{user_id}@iec.co.il"}
    headers = {"accept": "application/json", "content-type": "application/json"}

    response = await commons.send_post_request(
        session=session, url=f"{IEC_OKTA_BASE_URL}/api/v1/authn", json_data=data, headers=headers
    )
    return response.get("stateToken", ""), response.get("_embedded", {}).get("factors", {})[0].get("id")


async def send_otp_code(
    session: ClientSession, factor_id: object, state_token: object, pass_code: object = None
) -> Tuple[Optional[str], Optional[str]]:
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


async def get_access_token(session: ClientSession, code, code_verifier) -> JWT:
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


async def first_login(
    session: ClientSession, id_number: str
) -> Tuple[str, str, Optional[str], Optional[str]]:
    try:
        state_token, factor_id = await get_first_factor_id(session, id_number)
        session_token, factor_type = await send_otp_code(session, factor_id, state_token)
        return state_token, factor_id, session_token, factor_type
    except Exception as error:
        logger.warning(f"Failed at first login: {error}")
        raise IECLoginError(-1, "Failed at first login") from error


async def verify_otp_code(
    session: ClientSession, factor_id: str, state_token: str, otp_code: str
) -> JWT:
    try:
        otp_session_token, _ = await send_otp_code(session, factor_id, state_token, otp_code)
        if not otp_session_token:
            raise IECLoginError(-1, "OTP verification failed: no session token")
        code, code_verifier = await authorize_session(session, otp_session_token)
        jwt_token = await get_access_token(session, code, code_verifier)
        return jwt_token
    except Exception as error:
        logger.warning(f"Failed at OTP verification: {error}")
        raise IECLoginError(-1, "Failed at OTP verification") from error


async def manual_authorization(session: ClientSession, id_number) -> JWT:
    if not id_number:
        id_number = await commons.read_user_input("Enter your ID Number: ")
    state_token, factor_id, session_token, factor_type = await first_login(session, id_number)
    if not state_token:
        logger.error("Failed to send OTP")
        raise IECLoginError(-1, "Failed to send OTP, no state_token")

    otp_code = await commons.read_user_input(f"Enter your OTP code sent to your {factor_type}: ")
    jwt_token = await verify_otp_code(session, factor_id, state_token, otp_code)
    logger.debug(
        f"Access token: {jwt_token.access_token}\n"
        f"Refresh token: {jwt_token.refresh_token}\n"
        f"id_token: {jwt_token.id_token}"
    )
    return jwt_token


async def refresh_token(session: ClientSession, token: JWT) -> JWT:
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
    token_data = json.dumps(token.to_dict()).encode()

    fernet = _get_fernet()
    if fernet:
        token_data = fernet.encrypt(token_data)
        async with aiofiles.open(path, mode="wb") as f:
            await f.write(token_data)
    else:
        async with aiofiles.open(path, mode="w", encoding="utf-8") as f:
            await f.write(token_data.decode())


async def load_token_from_file(path: str = "token.json") -> JWT:
    fernet = _get_fernet()

    if fernet:
        try:
            async with aiofiles.open(path, "rb") as f:
                encrypted_data = await f.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            jwt_data = JWT.from_dict(json.loads(decrypted_data.decode()))
        except Exception:
            async with aiofiles.open(path, "r", encoding="utf-8") as f:
                contents = await f.read()
            jwt_data = JWT.from_dict(json.loads(contents))
    else:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            contents = await f.read()
        jwt_data = JWT.from_dict(json.loads(contents))

    decode_token(jwt_data)

    return jwt_data


def get_token_remaining_time_to_expiration(token: JWT):
    decoded_token = decode_token(token)
    return decoded_token["exp"] - int(time.time())
