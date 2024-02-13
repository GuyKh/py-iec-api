""" IEC Login Module. """
import requests

from src import const
from src.models.login_flow import LoginResponse, OTPRequest, OTPResponse
from src.models.response_descriptor import ErrorResponseDescriptor

_SMS_URL = "https://iecapi.iec.co.il//api/Authentication/{}/1/-1"
_LOGIN_URL = "https://iecapi.iec.co.il//api/Authentication/login/{}"


def login_with_id_number(id_number: str) -> LoginResponse:
    # recaptcha_token = librecaptcha.get_token(api_key="", site_url="https://iecapi.iec.co.il//api/content/he-IL/login")
    """Get first login response from IEC API."""
    # sending get request and saving the response as response object
    response = requests.get(url=_SMS_URL.format(id_number), headers=const.HEADERS_NO_AUTH, timeout=10)

    if response.status_code != 200:
        login_error_response = ErrorResponseDescriptor.from_dict(response.json())
        raise IECLoginError(login_error_response.code, login_error_response.error)

    return LoginResponse.from_dict(response.json())


def verify_sms_otp(
        id_number: str, login_response: LoginResponse, sms_code: str
) -> str:
    """Get login token from IEC API by SMS authentication."""
    data = OTPRequest(login_response.href, login_response.state_token, sms_code)

    response = requests.post(
        url=_LOGIN_URL.format(id_number), headers=const.HEADERS_NO_AUTH, data=data, timeout=10
    )

    if response.status_code != 200:
        login_error_response = ErrorResponseDescriptor.from_dict(response.json())
        raise IECLoginError(login_error_response.code, login_error_response.error)

    return OTPResponse.from_dict(response.json()).token


def send_login_otp(id_number: str) -> LoginResponse:
    """Get authorization token from IEC API."""
    return login_with_id_number(id_number)  # pragma: no cover


def verify_otp(id_number: str, login_response: LoginResponse, otp_code: str) -> str:  # pragma: no cover
    """
    Verify OTP code and get authorization token from IEC API.
    """
    return verify_sms_otp(id_number, login_response, otp_code)


def get_authorization_token_from_user() -> str:  # pragma: no cover
    """Get authorization token from IEC API."""
    id_number = input("Enter ID number:")

    print(f"id_number: {id_number}")
    login_response = login_with_id_number(id_number)

    print(f"Hi {login_response.first_name}")
    print(
        f"please enter the SMS code sent to phone {login_response.phone_prefix}*****{login_response.phone_suffix}\n"
    )

    sms_code = input("Enter the SMS code:")
    return verify_sms_otp(id_number, login_response, sms_code)


class IECLoginError(Exception):
    """Exception raised for errors in the IEC Login.

    Attributes:
        code -- input salary which caused the error.
        error -- description of the error
    """

    def __init__(self, code, error):
        self.code = code
        self.error = error
        super().__init__(f"(Code {self.code}): {self.error}")


def refresh_token(prev_token: str) -> str | None:  # pragma: no cover
    """Refresh JWT token."""
    return None
