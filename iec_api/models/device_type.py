from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options

from iec_api.models.response_descriptor import ResponseDescriptor

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
    device_balance: int | None = field(metadata=field_options(alias="deviceBalance"))
    device_type: int = field(metadata=field_options(alias="deviceType"))
    estimated_days_by_week: int | None = field(metadata=field_options(alias="estimatedDaysByWeek"))
    average_usage_cost_by_week: int | None = field(metadata=field_options(alias="averageUsageCostByWeek"))
    estimated_days_by_month: int | None = field(metadata=field_options(alias="estimatedDaysByMonth"))
    average_usage_cost_by_month: int | None = field(metadata=field_options(alias="averageUsageCostByMonth"))
    balance_time: str | None = field(metadata=field_options(alias="balanceTime"))
    balance_date: str | None = field(metadata=field_options(alias="balanceDate"))
    is_active: bool = field(metadata=field_options(alias="isActive"))
    number_of_devices: int = field(metadata=field_options(alias="numberOfDevices"))


@dataclass
class DeviceTypeResponse(DataClassDictMixin):
    """Device Type Response dataclass."""

    data: DeviceType
    response_descriptor: ResponseDescriptor = field(metadata=field_options(alias="reponseDescriptor"))
