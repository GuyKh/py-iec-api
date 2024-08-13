from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masa-mainportalapi.iec.co.il/api/contacts/userprofile
#
# {
#     "governmentid": "1234566",
#     "idType": 279830001,
#     "email": "my.mail@gmail.com",
#     "phoneNumber": "123456",
#     "accounts": [
#         {
#             "name": "השם שלי",
#             "accountNumber": "12345",
#             "governmentNumber": "12345",
#             "accountType": 279830000,
#             "viewTypeCode": 1,
#             "identificationType": 279830001,
#             "consumptionOrderViewTypeCode": 1,
#             "id": "b67ea524-300f-4a85-9ef4-54d30a753452",
#             "logicalName": "account"
#         }
#     ],
#     "phonePrefix": "051",
#     "isConnectedToPrivateAccount": false,
#     "isAccountOwner": false,
#     "isAccountContact": false,
#     "id": "b67ea524-300f-4a85-9ef4-54d30a753452",
#     "logicalName": "contact"
# }


@dataclass
class UserProfileAccount(DataClassDictMixin):
    """
    Represents an account associated with a contact.

    Attributes:
        name (str): The name of the account.
        account_number (str): The account number.
        government_number (str): The government ID associated with the account.
        account_type (int): The type of the account.
        view_type_code (int): The view type code for the account.
        identification_type (int): The type of identification used for the account.
        consumption_order_view_type_code (int): The view type code for consumption order.
        id (UUID): The unique identifier for the account.
        logical_name (str): The logical name of the entity.
    """

    name: str = field(metadata=field_options(alias="name"))
    account_number: str = field(metadata=field_options(alias="accountNumber"))
    government_number: str = field(metadata=field_options(alias="governmentNumber"))
    account_type: int = field(metadata=field_options(alias="accountType"))
    view_type_code: int = field(metadata=field_options(alias="viewTypeCode"))
    identification_type: int = field(metadata=field_options(alias="identificationType"))
    consumption_order_view_type_code: int = field(metadata=field_options(alias="consumptionOrderViewTypeCode"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class MasaUserProfile(DataClassDictMixin):
    """
    Represents a contact with associated accounts.

    Attributes:
        government_id (str): The government ID of the contact.
        id_type (int): The type of ID used.
        email (str): The email address of the contact.
        phone_number (str): The phone number of the contact.
        accounts (List[Account]): A list of accounts associated with the contact.
        phone_prefix (str): The phone prefix of the contact.
        is_connected_to_private_account (bool): Indicates if the contact is connected to a private account.
        is_account_owner (bool): Indicates if the contact is the owner of the account.
        is_account_contact (bool): Indicates if the contact is an account contact.
        id (UUID): The unique identifier for the contact.
        logical_name (str): The logical name of the entity.
    """

    government_id: str = field(metadata=field_options(alias="governmentid"))
    id_type: int = field(metadata=field_options(alias="idType"))
    email: str = field(metadata=field_options(alias="email"))
    phone_number: str = field(metadata=field_options(alias="phoneNumber"))
    accounts: List[UserProfileAccount] = field(metadata=field_options(alias="accounts"))
    phone_prefix: str = field(metadata=field_options(alias="phonePrefix"))
    is_connected_to_private_account: bool = field(metadata=field_options(alias="isConnectedToPrivateAccount"))
    is_account_owner: bool = field(metadata=field_options(alias="isAccountOwner"))
    is_account_contact: bool = field(metadata=field_options(alias="isAccountContact"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
