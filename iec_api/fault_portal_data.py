from typing import List, Optional

from aiohttp import ClientSession

from iec_api import commons
from iec_api.const import (
    GET_OUTAGES_FROM_FAULT_PORTAL_URL,
    GET_USER_PROFILE_FROM_FAULT_PORTAL_URL,
    HEADERS_WITH_AUTH,
    POST_ACCOUNTS_TRANSACTIONS_URL,
)
from iec_api.fault_portal_models.accounts_transactions import AccountsTransactionsRequest, AccountsTransactionsResponse
from iec_api.fault_portal_models.outages import FaultPortalOutage, OutagesResponse
from iec_api.fault_portal_models.user_profile import UserProfile
from iec_api.models.jwt import JWT


async def get_user_profile(session: ClientSession, token: JWT) -> Optional[UserProfile]:
    """Get User Profile from IEC Fault PortalAPI."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(
        session=session, url=GET_USER_PROFILE_FROM_FAULT_PORTAL_URL, headers=headers
    )

    return UserProfile.from_dict(response)


async def post_accounts_transactions(
    session: ClientSession, token: JWT, accounts: List[str], state_code: int = 0
) -> AccountsTransactionsResponse:
    """Post Accounts Transactions to IEC Fault Portal API.

    Args:
        session: The aiohttp ClientSession object.
        token: The JWT token for authentication.
        accounts: List of account UUIDs to query.
        state_code: The state code filter (default 0).

    Returns:
        AccountsTransactionsResponse: The accounts transactions response.
    """

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    request = AccountsTransactionsRequest(accounts=accounts, state_code=state_code).to_dict(by_alias=True)
    response = await commons.send_post_request(
        session=session, url=POST_ACCOUNTS_TRANSACTIONS_URL, headers=headers, json_data=request
    )

    return AccountsTransactionsResponse.from_dict(response)


async def get_outages_by_account(
    session: ClientSession, token: JWT, account_id: str
) -> Optional[List[FaultPortalOutage]]:
    """Get Outages from IEC Fault PortalAPI."""

    headers = commons.add_auth_bearer_to_headers(HEADERS_WITH_AUTH, token.id_token)
    # sending get request and saving the response as response object
    response = await commons.send_get_request(session=session, url=GET_OUTAGES_FROM_FAULT_PORTAL_URL, headers=headers)

    return OutagesResponse.from_dict(response).data_collection
