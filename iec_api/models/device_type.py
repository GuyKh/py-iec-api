from dataclasses import dataclass, field
from typing import Optional

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

#
# GET https://iecapi.iec.co.il//api/Device/type/{bp_number}/{contract_id}/false
#
# {
#     "data": {
#         "deviceNumber": "20008389",
#         "deviceBalance": null,
#         "deviceType": 0,
#         "estimatedDaysByWeek": null,
#         "averageUsageCostByWeek": null,
#         "estimatedDaysByMonth": null,
#         "averageUsageCostByMonth": null,
#         "balanceTime": null,
#         "balanceDate": null,
#         "isActive": true,
#         "numberOfDevices": 1
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "00",
#         "description": ""
#     }
# }
#


@dataclass
class DeviceType(DataClassDictMixin):
    """Device dataclass."""

    device_number: str = field(metadata=field_options(alias="deviceNumber"))
    device_balance: Optional[int] = field(metadata=field_options(alias="deviceBalance"))
    device_type: int = field(metadata=field_options(alias="deviceType"))
    estimated_days_by_week: Optional[int] = field(metadata=field_options(alias="estimatedDaysByWeek"))
    average_usage_cost_by_week: Optional[int] = field(metadata=field_options(alias="averageUsageCostByWeek"))
    estimated_days_by_month: Optional[int] = field(metadata=field_options(alias="estimatedDaysByMonth"))
    average_usage_cost_by_month: Optional[int] = field(metadata=field_options(alias="averageUsageCostByMonth"))
    balance_time: Optional[str] = field(metadata=field_options(alias="balanceTime"))
    balance_date: Optional[str] = field(metadata=field_options(alias="balanceDate"))
    is_active: bool = field(metadata=field_options(alias="isActive"))
    number_of_devices: int = field(metadata=field_options(alias="numberOfDevices"))


decoder = BasicDecoder(ResponseWithDescriptor[DeviceType])
