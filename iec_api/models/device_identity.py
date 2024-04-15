# GET https://iecapi.iec.co.il//api/Tenant/Identify/{{device_id}}
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

# {
#     "data": {
#         "devicesDetails": [
#             {
#                 "deviceNumber": "12345",
#                 "deviceCode": "123",
#                 "address": "הרצל 5, חיפה",
#                 "lastReadingValue": "12345",
#                 "lastReadingType": "01",
#                 "lastReadingDate": "2024-03-01T00:00:00"
#             }
#         ],
#         "lastDate": "0001-01-01T00:00:00",
#         "privateProducer": false
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "26",
#         "description": "מונה אינו חד חד ערכי"
#     }
# }


@dataclass
class DeviceDetails(DataClassDictMixin):
    """Device Details dataclass"""

    device_number: str = field(metadata=field_options(alias="deviceNumber"))
    device_code: str = field(metadata=field_options(alias="deviceCode"))
    address: str = field(metadata=field_options(alias="address"))
    last_reading_value: str = field(metadata=field_options(alias="lastReadingValue"))
    last_reading_type: str = field(metadata=field_options(alias="lastReadingType"))
    last_reading_date: datetime = field(metadata=field_options(alias="lastReadingDate"))


@dataclass
class DeviceIdentity(DataClassDictMixin):
    """Devices dataclass."""

    device_details: Optional[list[DeviceDetails]] = field(metadata=field_options(alias="devicesDetails"))
    last_date: datetime = field(metadata=field_options(alias="lastDate"))
    is_private_producer: bool = field(metadata=field_options(alias="privateProducer"))


decoder = BasicDecoder(ResponseWithDescriptor[DeviceIdentity])
