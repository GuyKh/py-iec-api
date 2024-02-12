import requests

from src.login import IECLoginError
from src.models.customer import Customer
from src.const import GET_CONSUMER_URL, HEADERS_WITH_AUTH
from src.models.response_descriptor import ErrorResponseDescriptor


def get_consumer() -> Customer:
    """Get consumer data response from IEC API."""
    # sending get request and saving the response as response object
    response = requests.get(url=GET_CONSUMER_URL, headers=HEADERS_WITH_AUTH, timeout=10)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    return Customer.from_dict(response.json())
