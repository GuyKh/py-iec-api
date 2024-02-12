import requests

from src.login import IECLoginError
from src.models.customer import Customer
from src.const import GET_CONSUMER_URL, HEADERS_WITH_AUTH, GET_REQUEST_READING_URL
from src.models.response_descriptor import ErrorResponseDescriptor
from src.models.remote_reading import RemoteReadingRequest, RemoteReadingResponse


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


def get_remote_reading(meter_serial_number: str, meter_code: int, last_invoice_date: str, from_date: str,
                       resolution: int) -> RemoteReadingResponse:
    req = RemoteReadingRequest(meterSerialNumber=meter_serial_number, meterCode=meter_code,
                               lastInvoiceDate=last_invoice_date, fromDate=from_date, resolution=resolution)

    response = requests.post(url=GET_REQUEST_READING_URL, data=req, headers=HEADERS_WITH_AUTH, timeout=10)

    if response.status_code != 200:
        print(f"Failed Login: (Code {response.status_code}): {response.reason}")
        if len(response.content) > 0:
            login_error_response = ErrorResponseDescriptor.from_dict(response.json())
            raise IECLoginError(login_error_response.code, login_error_response.error)
        else:
            raise IECLoginError(response.status_code, response.reason)

    return RemoteReadingResponse.from_dict(response.json())
