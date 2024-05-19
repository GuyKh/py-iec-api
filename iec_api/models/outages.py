""" Outages model. """
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

# GET https://iecapi.iec.co.il//api/outages/transactions/{account_id}/2
#
# {
#     "data": [
#         {
#             "transactionsInfo": [
#                 {
#                     "disconnectDate": "2024-05-17T22:32:16Z",
#                     "disconnect": {
#                         "disconnectKey": "17701HESD5840",
#                         "disconnectType": {
#                             "displayName": "תקלה איזורית",
#                             "code": 1,
#                             "id": "b146f469-819a-ea11-a811-000d3a239ca0"
#                         },
#                         "disconnectTreatmentState": {
#                             "displayName": "החזרת אספקה",
#                             "code": "6",
#                             "isConnectIndicationBit": false,
#                             "id": "7eaecdd3-859a-ea11-a812-000d3a239136"
#                         },
#                         "id": "1d9a36ef-9a14-ef11-9f89-7c1e52290237",
#                         "estimateTreatmentDate": null,
#                         "energizedDate": "2024-05-18T11:09:41Z"
#                     },
#                     "disconnectType": 1
#                 }
#             ],
#             "site": {
#                 "contractNumber": "346496424",
#                 "address": {
#                     "region": {
#                         "name": "חיפה והצפון",
#                         "id": "909a5d57-d7db-ea11-a813-000d3aabca53"
#                     },
#                     "area": {
#                         "name": "חיפה",
#                         "id": "0d93fbef-d7db-ea11-a813-000d3aabca53"
#                     },
#                     "street": "הגל",
#                     "houseNumber": "12",
#                     "city": {
#                         "name": "טירה",
#                         "shovalCityCode": "778",
#                         "logicalName": null,
#                         "id": "fb0a89b9-29e0-e911-a972-000d3a29fb7a"
#                     },
#                     "id": "f5453a99-0472-e811-8106-3863bb358f68"
#                 },
#                 "id": "8eb5c7da-e0a5-ea11-a812-000d3aaebb51",
#                 "x": null,
#                 "y": null
#             }
#         }
#     ],
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "0",
#         "description": ""
#     }
# }

# GET https://masa-faultsportalapi.iec.co.il/api/accounts/{{account_id}}/tranzactions/2
#
# # {
#     "dataCollection": []
# }


@dataclass
class DisconnectType(DataClassDictMixin):
    """DisconnectType dataclass"""

    display_name: str = field(metadata=field_options(alias="displayName"))
    code: int = field(metadata=field_options(alias="code"))
    id: UUID = field(metadata=field_options(alias="id"))


@dataclass
class DisconnectTreatmentState(DataClassDictMixin):
    """DisconnectTreatmentState dataclass"""

    display_name: str = field(metadata=field_options(alias="displayName"))
    code: str = field(metadata=field_options(alias="code"))
    is_connect_indication_bit: bool = field(metadata=field_options(alias="isConnectIndicationBit"))
    id: UUID = field(metadata=field_options(alias="id"))


@dataclass
class Disconnect(DataClassDictMixin):
    """Disconnect dataclass."""

    id: UUID = field(metadata=field_options(alias="id"))
    estimate_treatment_date: Optional[datetime] = field(metadata=field_options(alias="estimateTreatmentDate"))
    energized_date: Optional[str] = field(metadata=field_options(alias="energizedDate"))
    disconnect_key: Optional[str] = field(metadata=field_options(alias="disconnectKey"))
    disconnect_type: Optional[DisconnectType] = field(metadata=field_options(alias="disconnectType"))
    disconnect_treatment_state: Optional[DisconnectTreatmentState] = field(
        metadata=field_options(alias="disconnectTreatmentState")
    )


@dataclass
class TransactionsInfo(DataClassDictMixin):
    """Transactions Info dataclass."""

    disconnect_date: datetime = field(metadata=field_options(alias="disconnectDate"))
    disconnect: Disconnect = field(metadata=field_options(alias="disconnect"))
    disconnect_type: int = field(metadata=field_options(alias="disconnectType"))


@dataclass
class OutageAddress(DataClassDictMixin):
    """Outage Address dataclass."""

    name: str = field(metadata=field_options(alias="name"))
    id: UUID = field(metadata=field_options(alias="id"))


@dataclass
class OutageAddressCity(OutageAddress):
    """Outage Address dataclass."""

    logical_name: str = field(metadata=field_options(alias="logicalName"))
    shoval_city_code: str = field(metadata=field_options(alias="shovalCityCode"))


@dataclass
class OutageAddressFull(DataClassDictMixin):
    """Full Outage Address dataclass."""

    region: OutageAddress = field(metadata=field_options(alias="region"))
    area: OutageAddress = field(metadata=field_options(alias="area"))
    street: str = field(metadata=field_options(alias="street"))
    house_number: str = field(metadata=field_options(alias="houseNumber"))
    city: OutageAddress = field(metadata=field_options(alias="city"))
    id: UUID = field(metadata=field_options(alias="id"))


@dataclass
class Site(DataClassDictMixin):
    """Site dataclass."""

    contract_number: str = field(metadata=field_options(alias="contractNumber"))
    address: OutageAddressFull = field(metadata=field_options(alias="address"))
    id: UUID = field(metadata=field_options(alias="id"))
    x: Optional[float] = field(metadata=field_options(alias="x"))
    y: Optional[float] = field(metadata=field_options(alias="y"))


@dataclass
class Outage(DataClassDictMixin):
    """Outage dataclass."""

    transactions_info: List[TransactionsInfo] = field(metadata=field_options(alias="transactionsInfo"))
    site: Site = field(metadata=field_options(alias="site"))


decoder = BasicDecoder(ResponseWithDescriptor[List[Outage]])
