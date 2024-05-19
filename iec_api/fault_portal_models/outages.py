# Outages model

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from mashumaro import DataClassDictMixin, field_options

from iec_api.fault_portal_models.fault_portal_base import FaultPortalBase

# GET https://masa-faultsportalapi.iec.co.il/api/accounts/{account_id}}/tranzactions/2
#
# {
#   "dataCollection":
#       [
# {
#             "siteKeyDesc": "603147332",
#             "disconnectDate": "2024-05-17T22:32:16Z",
#             "disconnect": {
#                 "disconnectKey": "17701HESD58403",
#                 "disconnectTreatmentState": {
#                     "displayName": "החזרת אספקה",
#                     "code": "6",
#                     "isConnectIndicationBit": false,
#                     "disconnectTreatmentStatePortal": 3,
#                     "id": "7eaecdd3-859a-ea11-a812-000d3a239136",
#                     "logicalName": "iec_disconnecttreatmentstate"
#                 },
#                 "disconnectType": {
#                     "displayName": "תקלה איזורית",
#                     "code": 1,
#                     "id": "b146f469-819a-ea11-a811-000d3a239ca0",
#                     "logicalName": "iec_disconnecttype"
#                 },
#                 "energizedDate": "2024-05-18T11:09:41Z",
#                 "disconnectDate": "2024-05-17T22:12:08Z",
#                 "id": "1d9a36ef-9a14-ef11-9f89-7c1e52290237",
#                 "logicalName": "iec_disconnect"
#             },
#             "site": {
#                 "contractNumber": "346496424",
#                 "address": {
#                     "area": {
#                         "name": "חיפה",
#                         "id": "0d93fbef-d7db-ea11-a813-000d3aabca53",
#                         "logicalName": "iec_area"
#                     },
#                     "region": {
#                         "name": "חיפה והצפון",
#                         "id": "909a5d57-d7db-ea11-a813-000d3aabca53",
#                         "logicalName": "iec_region"
#                     },
#                     "city": {
#                         "name": "טירת כרמל",
#                         "shovalCityCode": "778",
#                         "id": "fb0a89b9-29e0-e911-a972-000d3a29fb7a",
#                         "logicalName": "iec_city"
#                     },
#                     "houseNumber": "11",
#                     "streetStr": "הגל",
#                     "id": "f5453a99-0472-e811-8106-3863bb358f68",
#                     "logicalName": "iec_address"
#                 },
#                 "id": "8eb5c7da-e0a5-ea11-a812-000d3aaebb51",
#                 "logicalName": "iec_site"
#             },
#             "id": "e95a1233-9b14-ef11-9f89-7c1e52290237",
#             "logicalName": "iec_tranzaction",
#             "stateCode": 1
#         }
#       ]
#   }
# }


@dataclass
class FaultPortalAddress(FaultPortalBase):
    """Address Model for Area/Region/City"""

    name: Optional[str] = field(metadata=field_options(alias="name"))


@dataclass
class FaultPortalCity(FaultPortalAddress):
    """Address Model for Area/Region/City"""

    shoval_city_code: Optional[str] = field(metadata=field_options(alias="shovalCityCode"))


@dataclass
class FaultPortalFullAddress(FaultPortalBase):
    """Full Address Model"""

    area: Optional[FaultPortalAddress] = field(metadata=field_options(alias="area"))
    region: Optional[FaultPortalAddress] = field(metadata=field_options(alias="region"))
    city: Optional[FaultPortalCity] = field(metadata=field_options(alias="city"))
    house_number: Optional[str] = field(metadata=field_options(alias="houseNumber"))
    street_str: Optional[str] = field(metadata=field_options(alias="streetStr"))


@dataclass
class Site(FaultPortalBase):
    """Site Model"""

    contract_number: Optional[str] = field(metadata=field_options(alias="contractNumber"))
    address: Optional[FaultPortalFullAddress] = field(metadata=field_options(alias="address"))


@dataclass
class DisconnectTreatmentState(FaultPortalBase):
    """Disconnect Treatment State Model"""

    display_name: Optional[str] = field(metadata=field_options(alias="displayName"))
    code: Optional[int] = field(metadata=field_options(alias="code"))
    is_connect_indication_bit: Optional[bool] = field(metadata=field_options(alias="isConnectIndicationBit"))
    disconnect_treatment_state_portal: Optional[int] = field(
        metadata=field_options(alias="disconnectTreatmentStatePortal")
    )


@dataclass
class DisconnectType(FaultPortalBase):
    """Disconnect Type Model"""

    display_name: Optional[str] = field(metadata=field_options(alias="displayName"))
    code: Optional[int] = field(metadata=field_options(alias="code"))


@dataclass
class Disconnect(FaultPortalBase):
    """Disconnect Model"""

    disconnect_key: Optional[str] = field(metadata=field_options(alias="disconnectKey"))
    disconnect_type: Optional[DisconnectType] = field(metadata=field_options(alias="disconnectType"))
    energized_date: Optional[datetime] = field(metadata=field_options(alias="energizedDate"))
    disconnect_date: Optional[datetime] = field(metadata=field_options(alias="disconnectDate"))
    disconnect_treatment_state: Optional[DisconnectTreatmentState] = field(
        metadata=field_options(alias="disconnectTreatmentState")
    )


@dataclass
class FaultPortalOutage(FaultPortalBase):
    """Outage Model"""

    site_key_desc: Optional[str] = field(metadata=field_options(alias="siteKeyDesc"))
    disconnect_date: Optional[datetime] = field(metadata=field_options(alias="disconnectDate"))
    state_code: Optional[int] = field(metadata=field_options(alias="stateCode"))
    site: Optional[Site] = field(metadata=field_options(alias="site"))
    disconnect: Optional[Disconnect] = field(metadata=field_options(alias="disconnect"))


@dataclass
class OutagesResponse(DataClassDictMixin):
    data_collection: Optional[List[FaultPortalOutage]] = field(metadata=field_options(alias="dataCollection"))
