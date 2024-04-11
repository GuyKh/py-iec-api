from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder
from mashumaro.config import BaseConfig

from iec_api.models.response_descriptor import ResponseWithDescriptor

#
#   POST https://iecapi.iec.co.il//api/outages/transactionsByAddress
#   BODY {
#       "cityCode":"34698a40-28ec-ea11-a817-000d3a239ca0",
#       "streetCode":"d02b9dcc-9094-ea11-a811-000d3a228dfc"
#       "houseNumber":"2"
#   }
#
#   Response:
# {
#     "data": {
#         "readDataTime": "2024-04-08T06:41:57.1502783+00:00",
#         "transaction": {
#             "disconnectionType": "",
#             "estimateTreatmentDate": null,
#             "messageToDisplay": null
#         }
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "0",
#         "description": ""
#     }
# }
#


@dataclass
class GetOutageByAddressRequest(DataClassDictMixin):
    city_code: UUID = field(metadata=field_options(alias="cityCode"))
    house_code: UUID = field(metadata=field_options(alias="streetCode"))
    logical_name: str = field(metadata=field_options(alias="houseNumber"))

    class Config(BaseConfig):
        serialize_by_alias = True


@dataclass
class OutageTransaction(DataClassDictMixin):
    disconnection_type: Optional[str] = field(metadata=field_options(alias="disconnectionType"))
    estimate_treatment_date: Optional[datetime] = field(metadata=field_options(alias="estimateTreatmentDate"))
    message_to_display: Optional[str] = field(metadata=field_options(alias="messageToDisplay"))


@dataclass
class GetOutageByAddressResponse(DataClassDictMixin):
    read_data_time: datetime = field(metadata=field_options(alias="readDataTime"))
    transaction: OutageTransaction = field(metadata=field_options(alias="transaction"))


decoder = BasicDecoder(ResponseWithDescriptor[GetOutageByAddressResponse])
