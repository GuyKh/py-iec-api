from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

#
# GET https://iecapi.iec.co.il//api/Device/{contract_id}
#
# [
#     {
#         "isActive": true,
#         "deviceType": 3,
#         "deviceNumber": "23231111",
#         "deviceCode": "503"
#     }
#
# -----------
# GET https://iecapi.iec.co.il//api/Device/{bp_number}/{contract_id}
# {
#     "data": {
#         "counterDevices": [
#             {
#                 "device": "00000000002000111",
#                 "register": "001",
#                 "lastMR": "00000000000011111",
#                 "lastMRDate": "2024-01-11",
#                 "lastMRType": "01",
#                 "lastMRTypeDesc": "קריאת מונה לפי שגרות מערכת",
#                 "connectionSize": {
#                     "size": 25,
#                     "phase": 3,
#                     "representativeConnectionSize": "3X20"
#                 }
#             }
#         ],
#         "mrType": "01"
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "00",
#         "description": null
#     }
# }


@dataclass
class Device(DataClassDictMixin):
    """Device dataclass."""

    is_active: bool = field(metadata=field_options(alias="isActive"))
    device_type: Optional[int] = field(default=None, metadata=field_options(alias="deviceType"))
    device_number: Optional[str] = field(default=None, metadata=field_options(alias="deviceNumber"))
    device_code: Optional[str] = field(default=None, metadata=field_options(alias="deviceCode"))


@dataclass
class ConnectionSize(DataClassDictMixin):
    """Connection dataclass."""

    size: int = field(metadata=field_options(alias="size"))
    phase: int = field(metadata=field_options(alias="phase"))
    representative_connection_size: str = field(metadata=field_options(alias="representativeConnectionSize"))


@dataclass
class CounterDevice(DataClassDictMixin):
    """Counter Device dataclass."""

    device: str = field(metadata=field_options(alias="device"))
    register: str = field(metadata=field_options(alias="register"))
    last_mr: str = field(metadata=field_options(alias="lastMR"))
    last_mr_type: str = field(metadata=field_options(alias="lastMRType"))
    last_mr_type_desc: str = field(metadata=field_options(alias="lastMRTypeDesc"))
    connection_size: ConnectionSize = field(metadata=field_options(alias="connectionSize"))
    last_mr_date: Optional[date] = field(default=None, metadata=field_options(alias="lastMRDate"))


@dataclass
class Devices(DataClassDictMixin):
    """Devices dataclass."""

    mr_type: str = field(metadata=field_options(alias="mrType"))
    counter_devices: Optional[list[CounterDevice]] = field(default=None, metadata=field_options(alias="counterDevices"))


decoder = BasicDecoder(ResponseWithDescriptor[Devices])
