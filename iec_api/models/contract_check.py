from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

#   Type = 4/6
#
#   GET https://iecapi.iec.co.il//api/customer/checkContract/{{contract_id}}/{type}
#
#   Response:
#
# {
#     "data": {
#         "contractNumber": "123456",
#         "deviceNumber": "1234566",
#         "bpKind": "0001",
#         "bp": "12345",
#         "address": "הכתובת שלי",
#         "city": "תל אביב - יפו",
#         "cityCode": "000000001234",
#         "streetCode": "000000001234",
#         "houseNumber": "01",
#         "bpType": "01",
#         "isPrivate": "",
#         "hasDirectDebit": false,
#         "isMatam": false,
#         "frequency": 2    // 1 = Monthly, 2 = BiMonthly
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "00",
#         "description": ""
#     }
# }
#


class InvoiceFrequency(IntEnum):
    MONTHLY = 1
    BIMONTHLY = 2


@dataclass
class ContractCheck(DataClassDictMixin):
    contract_number: str = field(metadata=field_options(alias="contractNumber"))
    device_number: str = field(metadata=field_options(alias="deviceNumber"))
    bp_kind: str = field(metadata=field_options(alias="bpKind"))
    bp: str = field(metadata=field_options(alias="bp"))
    address: str = field(metadata=field_options(alias="address"))
    city: str = field(metadata=field_options(alias="city"))
    city_code: str = field(metadata=field_options(alias="cityCode"))  # based on CityCode request
    street_code: str = field(metadata=field_options(alias="streetCode"))  # based on StreetCode request
    house_number: str = field(metadata=field_options(alias="houseNumber"))
    bp_type: str = field(metadata=field_options(alias="bpType"))
    is_private: str = field(metadata=field_options(alias="isPrivate"))  # "X" if private producer
    has_direct_debit: bool = field(metadata=field_options(alias="hasDirectDebit"))
    is_matam: bool = field(metadata=field_options(alias="isMatam"))
    frequency: Optional[InvoiceFrequency] = field(metadata=field_options(alias="frequency"))


decoder = BasicDecoder(ResponseWithDescriptor[ContractCheck])
