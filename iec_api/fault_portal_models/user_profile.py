# User Profile Model

from dataclasses import dataclass, field
from typing import Optional

from mashumaro import field_options

from iec_api.fault_portal_models.fault_portal_base import FaultPortalBase

# GET https://masa-mainportalapi.iec.co.il/api/contacts/userprofile
#
# {
#     "governmentid": "123456",
#     "idType": 12345,
#     "email": "my@mail.com",
#     "phoneNumber": "1234567",
#     "accounts": [
#         {
#             "name": "my_name",
#             "accountNumber": "123456",
#             "governmentNumber": "12345",
#             "accountType": 123456,
#             "viewTypeCode": 1,
#             "identificationType": 123456,
#             "consumptionOrderViewTypeCode": 1,
#             "id": "123456-1232-1312-1112-3563bb357f98",
#             "logicalName": "account"
#         }
#     ],
#     "phonePrefix": "050",
#     "isConnectedToPrivateAccount": false,
#     "isAccountOwner": false,
#     "isAccountContact": false,
#     "id": "123456-1232-1312-1112-3563bb357f98",
#     "logicalName": "contact"
# }


@dataclass
class FaultPortalAccount(FaultPortalBase):
    name: Optional[str] = field(metadata=field_options(alias="name"))
    account_number: Optional[str] = field(metadata=field_options(alias="accountNumber"))
    government_number: Optional[str] = field(metadata=field_options(alias="governmentNumber"))
    account_type: Optional[int] = field(metadata=field_options(alias="accountType"))
    view_type_code: Optional[int] = field(metadata=field_options(alias="viewTypeCode"))
    identification_type: Optional[int] = field(metadata=field_options(alias="identificationType"))
    consumption_order_view_type_code: Optional[int] = field(
        metadata=field_options(alias="consumptionOrderViewTypeCode")
    )


@dataclass
class UserProfile(FaultPortalBase):
    government_id: Optional[str] = field(metadata=field_options(alias="governmentId"))
    id_type: Optional[int] = field(metadata=field_options(alias="idType"))
    email: Optional[str] = field(metadata=field_options(alias="email"))
    phone_prefix: Optional[str] = field(metadata=field_options(alias="phonePrefix"))
    phone_number: Optional[str] = field(metadata=field_options(alias="phoneNumber"))
    accounts: Optional[list[FaultPortalAccount]] = field(metadata=field_options(alias="accounts"))
    is_connected_to_private_account: Optional[bool] = field(metadata=field_options(alias="isConnectedToPrivateAccount"))
    is_account_owner: Optional[bool] = field(metadata=field_options(alias="isAccountOwner"))
    is_account_contact: Optional[bool] = field(metadata=field_options(alias="isAccountContact"))
