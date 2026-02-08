from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options

# GET https://iecapi.iec.co.il/api/DeviceIn/{bp_number}
#
# Return format is:
# {
#     "status": 0,
#     "isActive": true,
#     "devices": [
#         {
#             "isActive": true,
#             "deviceType": 3,
#             "deviceNumber": "12345",
#             "deviceCode": "1",
#             "meterKind": "Consumption"
#         }
#     ]
# }


@dataclass
class DeviceInDevice(DataClassDictMixin):
    """Device information from DeviceIn endpoint."""

    is_active: bool = field(metadata=field_options(alias="isActive"))
    device_type: int = field(metadata=field_options(alias="deviceType"))
    device_number: str = field(metadata=field_options(alias="deviceNumber"))
    device_code: str = field(metadata=field_options(alias="deviceCode"))
    meter_kind: str = field(metadata=field_options(alias="meterKind"))


@dataclass
class DeviceInResponse(DataClassDictMixin):
    """DeviceIn endpoint response."""

    status: int
    is_active: bool = field(metadata=field_options(alias="isActive"))
    devices: list[DeviceInDevice]
