"""Remote Reading model."""

# Request:
# curl 'https://iecapi.iec.co.il//api/Consumption/RemoteReadingRange/{contract_id}' \
#   -H 'accept: application/json, text/plain, */*' \
#   -H 'authorization: Bearer <base64_token>' \
#   -H 'content-type: application/json' \
#   --data-raw '{"contractNumber":"XXXXXXXXXXXX","lastInvoiceDate":"2000-01-01",
#                "fromDate":"2023-07-20","resolution":1,
#                "smartMetersList":[{"meterKind":"Consumption","meterCode":"123",
#                "meterSerial":"XXXXXXXX"}]}'
#
# Response:
# {
#   "reportStatus": 0,
#   "contractNumber": "XXXXXXXXXXXX",
#   "meterList": [{
#     "meterKind": 1,
#     "meterSerial": "XXXXXXXX",
#     "meterCode": "123",
#     "futureConsumptionInfo": {
#       "lastInvoiceDate": null,
#       "currentDate": "2023-07-23",
#       "futureConsumption": 14.857,
#       "totalImport": 35.598,
#       "totalImportDate": "2023-07-23"
#     },
#     "startDate": "2023-07-20",
#     "endDate": "2023-07-20",
#     "totalConsumptionForPeriod": 0.325,
#     "totalImportDateForPeriod": "2023-07-20",
#     "meterStartDate": "2023-04-13",
#     "totalImport": 35.273,
#     "periodConsumptions": [
#       { "interval": "2023-07-20T00:00:00+00:00", "consumption": 0.325, "backStream": 0, "status": 0 }
#     ]
#   }],
#   "taozList": []
# }
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import IntEnum
from typing import Optional

from mashumaro import DataClassDictMixin, field_options
from mashumaro.config import BaseConfig

from iec_api.commons import convert_to_tz_aware_datetime


class ReadingResolution(IntEnum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


@dataclass
class SmartMeter(DataClassDictMixin):
    """Smart Meter dataclass."""

    meter_kind: str = field(default="Consumption", metadata=field_options(alias="meterKind"))
    meter_code: str = field(default="", metadata=field_options(alias="meterCode"))
    meter_serial: str = field(default="", metadata=field_options(alias="meterSerial"))

    class Config(BaseConfig):
        serialize_by_alias = True


@dataclass
class RemoteReadingRequest(DataClassDictMixin):
    """Remote Reading Request."""

    contract_number: str = field(metadata=field_options(alias="contractNumber"))
    from_date: str = field(metadata=field_options(alias="fromDate"))
    resolution: ReadingResolution = field(metadata=field_options(alias="resolution"))
    smart_meters_list: list[SmartMeter] = field(metadata=field_options(alias="smartMetersList"))
    last_invoice_date: Optional[str] = field(default=None, metadata=field_options(alias="lastInvoiceDate"))

    class Config(BaseConfig):
        serialize_by_alias = True


@dataclass
class FutureConsumptionInfo(DataClassDictMixin):
    """Future Consumption Info dataclass."""

    last_invoice_date: Optional[str] = field(default=None, metadata=field_options(alias="lastInvoiceDate"))
    current_date: Optional[date] = field(default=None, metadata=field_options(alias="currentDate"))
    future_consumption: Optional[float] = field(default=None, metadata=field_options(alias="futureConsumption"))
    total_import: Optional[float] = field(default=None, metadata=field_options(alias="totalImport"))
    total_import_date: Optional[date] = field(default=None, metadata=field_options(alias="totalImportDate"))
    future_back_stream: Optional[float] = field(default=None, metadata=field_options(alias="futureBackStream"))
    multiplier_factor: Optional[float] = field(default=None, metadata=field_options(alias="multiplierFactor"))
    total_export: Optional[float] = field(default=None, metadata=field_options(alias="totalExport"))


@dataclass(frozen=True)
class RemoteReading(DataClassDictMixin):
    """Remote Reading Data dataclass."""

    status: int
    date: datetime
    value: float

    @classmethod
    def __post_deserialize__(cls, obj: "RemoteReading") -> "RemoteReading":
        object.__setattr__(obj, "date", convert_to_tz_aware_datetime(obj.date))
        return obj


@dataclass
class RemoteReadingResponse(DataClassDictMixin):
    """Remote Reading Response dataclass."""

    report_status: int = field(metadata=field_options(alias="reportStatus"))
    contract_number: str = field(default="", metadata=field_options(alias="contractNumber"))
    meter_list: list["MeterReadingData"] = field(default_factory=list, metadata=field_options(alias="meterList"))
    taoz_list: list = field(default_factory=list, metadata=field_options(alias="taozList"))
    report_status_text: Optional[str] = field(default=None, metadata=field_options(alias="reportStatusText"))


@dataclass(frozen=True)
class PeriodConsumption(DataClassDictMixin):
    """Period Consumption dataclass."""

    interval: datetime
    consumption: float
    back_stream: float = field(default=0.0, metadata=field_options(alias="backStream"))
    status: int = 0

    @classmethod
    def __post_deserialize__(cls, obj: "PeriodConsumption") -> "PeriodConsumption":
        object.__setattr__(obj, "interval", convert_to_tz_aware_datetime(obj.interval))
        return obj


@dataclass
class MeterReadingData(DataClassDictMixin):
    """Meter Reading Data dataclass."""

    meter_kind: Optional[int] = field(default=None, metadata=field_options(alias="meterKind"))
    report_result_status: Optional[int] = field(default=None, metadata=field_options(alias="reportResultStatus"))
    meter_serial: str = field(default="", metadata=field_options(alias="meterSerial"))
    meter_code: str = field(default="", metadata=field_options(alias="meterCode"))
    future_consumption_info: Optional[FutureConsumptionInfo] = field(
        default=None, metadata=field_options(alias="futureConsumptionInfo")
    )
    start_date: Optional[date] = field(default=None, metadata=field_options(alias="startDate"))
    end_date: Optional[date] = field(default=None, metadata=field_options(alias="endDate"))
    number_of_period_aggregated: Optional[int] = field(
        default=None, metadata=field_options(alias="numberOfPeriodAggregated")
    )
    total_consumption_for_period: Optional[float] = field(
        default=None, metadata=field_options(alias="totalConsumptionForPeriod")
    )
    total_back_stream_for_period: Optional[float] = field(
        default=None, metadata=field_options(alias="totalBackStreamForPeriod")
    )
    total_import: Optional[float] = field(default=None, metadata=field_options(alias="totalImport"))
    total_export: Optional[float] = field(default=None, metadata=field_options(alias="totalExport"))
    total_import_date_for_period: Optional[date] = field(
        default=None, metadata=field_options(alias="totalImportDateForPeriod")
    )
    status_for_period: Optional[int] = field(default=None, metadata=field_options(alias="statusForPeriod"))
    meter_start_date: Optional[date] = field(default=None, metadata=field_options(alias="meterStartDate"))
    report_result_status_text: Optional[str] = field(
        default=None, metadata=field_options(alias="reportResultStatusText")
    )
    period_consumptions: list[PeriodConsumption] = field(
        default_factory=list, metadata=field_options(alias="periodConsumptions")
    )

    @classmethod
    def __post_deserialize__(cls, obj: "MeterReadingData") -> "MeterReadingData":
        if obj.period_consumptions:
            obj.period_consumptions.sort(key=lambda pc: pc.interval)
        return obj
