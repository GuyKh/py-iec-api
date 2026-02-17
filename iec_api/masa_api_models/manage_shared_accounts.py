from dataclasses import dataclass, field
from typing import Optional

from mashumaro import DataClassDictMixin, field_options

from iec_api.masa_api_models.masa_types import IDWrapper

# GET https://masa-mainportalapi.iec.co.il/api/contacts/{user_profile_id}/contract/{contract_id}
#
# Request:
# no body
#
# Response:
# {
#   "isConnectedToPrivateAccount": false,
#   "isAccountOwner": false,
#   "isAccountContact": false,
#   "connectionBetweenContactAndContract": [
#     {
#       "contact": {
#         "id": "00000000-0000-0000-0000-000000000001",
#         "isConnectedToPrivateAccount": false,
#         "isAccountOwner": false,
#         "isAccountContact": false,
#         "logicalName": "contact"
#       },
#       "contract": {
#         "id": "00000000-0000-0000-0000-000000000002",
#         "logicalName": "iec_contract"
#       },
#       "account": {
#         "id": "00000000-0000-0000-0000-000000000003",
#         "consumptionOrderViewTypeCode": 1,
#         "logicalName": "account"
#       },
#       "partConnectionCode": 4,
#       "connectionType": {
#         "id": "00000000-0000-0000-0000-000000000004",
#         "logicalName": "iec_connectiontype"
#       },
#       "tokenExpirationDate": "0001-01-01T00:00:00Z",
#       "id": "00000000-0000-0000-0000-000000000005",
#       "logicalName": "iec_connectionbetweencontactandcontract"
#     }
#   ],
#   "logicalName": "contact"
# }


@dataclass
class SharedAccountContact(IDWrapper):
    is_connected_to_private_account: bool = field(metadata=field_options(alias="isConnectedToPrivateAccount"))
    is_account_owner: bool = field(metadata=field_options(alias="isAccountOwner"))
    is_account_contact: bool = field(metadata=field_options(alias="isAccountContact"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class SharedAccountContract(IDWrapper):
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class SharedAccountAccount(IDWrapper):
    logical_name: str = field(metadata=field_options(alias="logicalName"))
    consumption_order_view_type_code: Optional[int] = field(
        default=None, metadata=field_options(alias="consumptionOrderViewTypeCode")
    )

@dataclass
class SharedAccountConnectionType(IDWrapper):
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class ConnectionBetweenContactAndContract(IDWrapper):
    contact: SharedAccountContact = field(metadata=field_options(alias="contact"))
    contract: SharedAccountContract = field(metadata=field_options(alias="contract"))
    account: SharedAccountAccount = field(metadata=field_options(alias="account"))
    part_connection_code: int = field(metadata=field_options(alias="partConnectionCode"))
    token_expiration_date: str = field(metadata=field_options(alias="tokenExpirationDate"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
    connection_type: Optional[SharedAccountConnectionType] = field(
        default=None, metadata=field_options(alias="connectionType")
    )


@dataclass
class ManageSharedAccountsResponse(DataClassDictMixin):
    is_connected_to_private_account: bool = field(metadata=field_options(alias="isConnectedToPrivateAccount"))
    is_account_owner: bool = field(metadata=field_options(alias="isAccountOwner"))
    is_account_contact: bool = field(metadata=field_options(alias="isAccountContact"))
    connection_between_contact_and_contract: list[ConnectionBetweenContactAndContract] = field(
        metadata=field_options(alias="connectionBetweenContactAndContract")
    )
    logical_name: str = field(metadata=field_options(alias="logicalName"))
