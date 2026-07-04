from dataclasses import dataclass, field
from typing import Optional

from mashumaro import DataClassDictMixin, field_options

# Historically this data came from:
#   GET https://iecapi.iec.co.il/api/DeviceIn/{contract_id}
#
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
#
# As of 2025 that endpoint returns HTTP 400 ("Token should be provide") unless a
# reCAPTCHA token (`RecaptchToken` header) is supplied, which isn't feasible for
# headless clients. The equivalent device list is now sourced from the
# reCAPTCHA-free `GET /api/Device/{contract_id}` endpoint (see data.get_device_in).
# That endpoint returns the same fields except `meterKind`, so it defaults to
# "Consumption" (the value the RemoteReadingRange request expects anyway).

# Default meter kind used when the source endpoint does not report one.
DEFAULT_METER_KIND = "Consumption"


@dataclass
class DeviceInDevice(DataClassDictMixin):
    """Device information (device list entry for a contract)."""

    is_active: bool = field(default=True, metadata=field_options(alias="isActive"))
    device_type: Optional[int] = field(default=None, metadata=field_options(alias="deviceType"))
    device_number: Optional[str] = field(default=None, metadata=field_options(alias="deviceNumber"))
    device_code: Optional[str] = field(default=None, metadata=field_options(alias="deviceCode"))
    meter_kind: str = field(default=DEFAULT_METER_KIND, metadata=field_options(alias="meterKind"))


@dataclass
class DeviceInResponse(DataClassDictMixin):
    """Device list response (compatible with the legacy DeviceIn payload)."""

    status: int = 0
    is_active: bool = field(default=True, metadata=field_options(alias="isActive"))
    devices: list[DeviceInDevice] = field(default_factory=list)
