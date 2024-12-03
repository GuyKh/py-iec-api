"""Customer model."""

# URL:
# POST https://iecapi.iec.co.il/api/customer
# Headers: Authorization: Bearer ...

# Response:
# {
#     "bpNumber": "...",
#     "idType": 1,
#     "accounts": [
#         {
#             "mainContractId": "...",
#             "mainContractIdType": 1,
#             "companyId": "...",
#             "name": "...",
#             "lastName": "...",
#             "bpNumber": "...",
#             "bpType": 1,
#             "isActiveAccount": true,
#             "customerRole": 0,
#             "accountType": 1
#         }
#     ],
#     "customerStatus": 1,
#     "idNumber": "...",
#     "firstName": "...",
#     "lastName": "...",
#     "mobilePhone": "...",
#     "email": "..."
# }

from dataclasses import dataclass, field
from typing import Optional

from mashumaro import DataClassDictMixin, field_options


@dataclass
class CustomerAccount(DataClassDictMixin):
    main_contract_id: str = field(metadata=field_options(alias="mainContractId"))
    main_contract_id_type: int = field(metadata=field_options(alias="mainContractIdType"))
    company_id: str = field(metadata=field_options(alias="companyId"))
    bp_number: str = field(metadata=field_options(alias="bpNumber"))
    bp_type: int = field(metadata=field_options(alias="bpType"))
    is_active_account: bool = field(metadata=field_options(alias="isActiveAccount"))
    customer_role: int = field(metadata=field_options(alias="customerRole"))
    account_type: int = field(metadata=field_options(alias="accountType"))
    name: Optional[str] = field(default=None, metadata=field_options(alias="name"))
    last_name: Optional[str] = field(default=None, metadata=field_options(alias="lastName"))


@dataclass
class Customer(DataClassDictMixin):
    bp_number: str = field(metadata=field_options(alias="bpNumber"))
    id_type: int = field(metadata=field_options(alias="idType"))
    accounts: list[CustomerAccount]
    customer_status: int = field(metadata=field_options(alias="customerStatus"))
    id_number: str = field(metadata=field_options(alias="idNumber"))
    first_name: str = field(metadata=field_options(alias="firstName"))
    last_name: str = field(metadata=field_options(alias="lastName"))
    mobile_phone: str = field(metadata=field_options(alias="mobilePhone"))
    email: str
