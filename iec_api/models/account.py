from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

# GET https://iecapi.iec.co.il//api/outages/accounts
#
#
# {
#     "data": [
#         {
#             "accountNumber": "123",
#             "accountType": 1234,
#             "id": "ebee08af-1111-2222-3333-3863bb358f68",
#             "email": null,
#             "telephone": null,
#             "governmentNumber": "200461929",
#             "name": "My Name",
#             "viewTypeCode": 1
#         }
#     ],
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "0",
#         "description": ""
#     }
# }


@dataclass
class Account(DataClassDictMixin):
    account_number: str = field(metadata=field_options(alias="accountNumber"))
    account_type: int = field(metadata=field_options(alias="accountType"))
    id: UUID
    email: Optional[str]
    telephone: Optional[str]
    government_number: str = field(metadata=field_options(alias="governmentNumber"))
    name: str
    view_type_code: int = field(metadata=field_options(alias="viewTypeCode"))


decoder = BasicDecoder(ResponseWithDescriptor[list[Account]])
