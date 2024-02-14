from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options

#
# GET https://iecapi.iec.co.il//api/Device/00012345
#
# [
#     {
#         "isActive": true,
#         "deviceType": 3,
#         "deviceNumber": "23231111",
#         "deviceCode": "503"
#     }
#
#


@dataclass
class Device(DataClassDictMixin):
    """Device dataclass."""

    device_type: int = field(metadata=field_options(alias="deviceType"))
    device_number: str = field(metadata=field_options(alias="deviceNumber"))
    device_code: str = field(metadata=field_options(alias="deviceCode"))
    is_active: bool = field(metadata=field_options(alias="isActive"))
