from dataclasses import dataclass, field
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

# GET https://iecapi.iec.co.il//api/District/cities
#
# {
#     "data": {
#         "dataCollection": [
#             {
#                 "name": "אלון תבור",
#                 "shovalCityCode": "2054",
#                 "logicalName": "iec_city",
#                 "id": "34698a40-28ec-ea11-a817-000d3a239ca0"
#             },]},
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "0",
#         "description": ""
#     }
# }
#
#
#
# GET https://iecapi.iec.co.il//api/District/streets/{city_id}
#
# {
#     "data": {
#         "streets": [
#             {
#                 "name": "רח 2369",
#                 "shovalStreetCode": "100000759",
#                 "logicalName": "iec_street",
#                 "id": "d02b9dcc-9094-ea11-a811-000d3a228dfc"
#             },
#         "logicalName": "iec_city",
#         "id": "a80a89b9-29e0-e911-a972-000d3a29fb7a"
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "0",
#         "description": ""
#     }
# }
#
#


@dataclass
class City(DataClassDictMixin):
    name: str = field(metadata=field_options(alias="name"))
    shoval_city_code: str = field(metadata=field_options(alias="shovalCityCode"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
    id: UUID = field(metadata=field_options(alias="id"))


@dataclass
class GetCitiesResponse(DataClassDictMixin):
    data_collection: list[City] = field(metadata=field_options(alias="dataCollection"))


get_cities_decoder = BasicDecoder(ResponseWithDescriptor[GetCitiesResponse])


@dataclass
class Street(DataClassDictMixin):
    name: str = field(metadata=field_options(alias="name"))
    shoval_street_code: str = field(metadata=field_options(alias="shovalStreetCode"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
    id: UUID = field(metadata=field_options(alias="id"))


@dataclass
class GetCityStreetsResponse(DataClassDictMixin):
    streets: list[Street] = field(metadata=field_options(alias="streets"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
    id: UUID = field(metadata=field_options(alias="id"))


get_city_streets_decoder = BasicDecoder(ResponseWithDescriptor[GetCityStreetsResponse])
