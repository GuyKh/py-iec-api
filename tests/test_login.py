from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.login import IECLoginError, get_login_response, get_login_token
from src.models.login_flow import LoginResponse


class LoginTest(TestCase):
    @staticmethod
    def _get_login_successful_response() -> dict:
        return {
            "phoneNumber": None,
            "phonePrefix": "051",
            "phoneSuffix": "23",
            "href": "https://iec-ext.okta.com/api/v1/authn/factors/someText/verify",
            "stateToken": "tokenTOKENtoken",
            "firstName": "name",
            "userStatus": 0,
            "multiFactorType": 0,
        }

    @patch("src.login.requests")
    def test_get_login_response(self, mock_requests):
        login_response_json = self._get_login_successful_response()

        # mock the response
        mock_response: MagicMock = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = login_response_json

        mock_requests.get.return_value = mock_response

        expected_login_response = LoginResponse.from_dict(login_response_json)
        self.assertEqual(get_login_response("123456789"), expected_login_response)

    @patch("src.login.requests")
    def test_login_404_response(self, mock_requests):
        # mock the response
        mock_response: MagicMock = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "Error": "User not exist",
            "Code": 404,
            "Rid": "1234567-0401-4500-b63f-84710c7967bb",
        }

        mock_requests.get.return_value = mock_response
        with self.assertRaises(IECLoginError):
            get_login_response("123456789")

    @patch("src.login.requests")
    def test_get_login_token(self, mock_requests):
        authorization_token = "123456"
        otp_response_json = {"token": authorization_token}

        # mock the response
        mock_response: MagicMock = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = otp_response_json

        mock_requests.post.return_value = mock_response

        login_response = LoginResponse.from_dict(self._get_login_successful_response())
        self.assertEqual(
            get_login_token("123456789", login_response, "1234"), authorization_token
        )

    @patch("src.login.requests")
    def test_get_login_token_returning_403(self, mock_requests):

        # mock the response
        mock_response: MagicMock = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
                "Error": "Exception of type 'IEC.Digital.Common.Exception.CustomException' was thrown.",
                "Code": 403,
                "Rid": "800119d6-1234-2313-b63f-84710c7967bb"
            }

        mock_requests.post.return_value = mock_response

        login_response = LoginResponse.from_dict(self._get_login_successful_response())
        with self.assertRaises(IECLoginError):
            get_login_token("123456789", login_response, "1234")
