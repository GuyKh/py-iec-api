""" IEC Login Module. """
import requests
from src.models.login_flow import LoginResponse, OTPRequest, OTPResponse
from src.models.response_descriptor import ErrorResponseDescriptor

_SMS_URL = "https://iecapi.iec.co.il//api/Authentication/{}/1/-1"
_LOGIN_URL = "https://iecapi.iec.co.il//api/Authentication/login/{}"
_HEADERS = {
    "Content-Type": "application/json",
    "accept": "application/json, text/plain, */*",
    "origin": "https://www.iec.co.il",
    "authority": "iecapi.iec.co.il",
    "referer": "https://www.iec.co.il/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36",
}


def get_login_response(id_number: str) -> LoginResponse:
    """Get first login response from IEC API."""
    # sending get request and saving the response as response object
    response = requests.get(url=_SMS_URL.format(id_number), headers=_HEADERS, timeout=10)

    if response.status_code != 200:
        login_error_response = ErrorResponseDescriptor.from_dict(response.json())
        raise IECLoginError(login_error_response.code, login_error_response.error)

    return LoginResponse.from_dict(response.json())


def get_login_token(
    id_number: str, login_response: LoginResponse, sms_code: str
) -> str:
    """Get login token from IEC API by SMS authentication."""
    data = OTPRequest(login_response.href, login_response.state_token, sms_code)

    response = requests.post(
        url=_LOGIN_URL.format(id_number), headers=_HEADERS, data=data, timeout=10
    )

    if response.status_code != 200:
        login_error_response = ErrorResponseDescriptor.from_dict(response.json())
        raise IECLoginError(login_error_response.code, login_error_response.error)

    return OTPResponse.from_dict(response.json()).token


def get_authorization_token() -> str:
    """Get authorization token from IEC API."""
    id_number = input("Enter ID number:")

    print(f"id_number: {id_number}")
    login_response = get_login_response(id_number)

    print(f"Hi {login_response.first_name}")
    print(
        f"please enter the SMS code sent to phone {login_response.phone_prefix}*****{login_response.phone_suffix}\n"
    )

    sms_code = input("Enter the SMS code:")
    return get_login_token(id_number, login_response, sms_code)


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
