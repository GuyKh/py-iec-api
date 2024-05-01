""" Remote Reading model. """

# Request:
# curl 'https://iecapi.iec.co.il//api/Consumption/RemoteReadingRange' \
#   -H 'accept: application/json, text/plain, /' \
#   -H 'authorization: Bearer <base64_token>' \
#   -H 'content-type: application/json' \
#   --data-raw '{"meterSerialNumber":"XXXXXXXX","meterCode":"123","lastInvoiceDate":"2000-01-01"\
#                   ,"fromDate":"2023-07-20","resolution":1}'
#
# Response:
# {
#   "status": 0,
#   "futureConsumptionInfo": {
#     "lastInvoiceDate": null,
#     "currentDate": "2023-07-23",
#     "futureConsumption": 14.857,
#     "totalImport": 35.598,
#     "totalImportDate": "2023-07-23"
#   },
#   "fromDate": "2023-07-20",
#   "toDate": "2023-07-20",
#   "totalConsumptionForPeriod": 0.325,
#   "totalImportDateForPeriod": "2023-07-20",
#   "meterStartDate": "2023-04-13",
#   "totalImport": 35.273,
#   "data": [{ "status": 8192, "date": "2023-07-20T00:00:00.000000", "value": 0 }]
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
class RemoteReadingRequest(DataClassDictMixin):
    """Remote Reading Request ."""

    meter_serial_number: str = field(metadata=field_options(alias="meterSerialNumber"))
    meter_code: str = field(metadata=field_options(alias="meterCode"))
    last_invoice_date: str = field(metadata=field_options(alias="lastInvoiceDate"))
    from_date: str = field(metadata=field_options(alias="fromDate"))
    resolution: ReadingResolution = field(metadata=field_options(alias="resolution"))

    class Config(BaseConfig):
        serialize_by_alias = True


@dataclass
class FutureConsumptionInfo(DataClassDictMixin):
    """Future Consumption Info dataclass."""

    last_invoice_date: Optional[str] = field(metadata=field_options(alias="lastInvoiceDate"))
    current_date: Optional[date] = field(metadata=field_options(alias="currentDate"))
    future_consumption: Optional[float] = field(metadata=field_options(alias="futureConsumption"))
    total_import: Optional[float] = field(metadata=field_options(alias="totalImport"))
    total_import_date: Optional[date] = field(metadata=field_options(alias="totalImportDate"))


@dataclass
class RemoteReading(DataClassDictMixin):
    """Remote Reading Data dataclass."""

    status: int
    date: datetime
    value: float

    def __hash__(self):
        """Compute the hash value the remote reading, based on all fields."""
        return hash((self.status, self.date, self.value))

    @classmethod
    def __post_deserialize__(cls, obj: "RemoteReading") -> "RemoteReading":
        obj.date = convert_to_tz_aware_datetime(obj.date)
        return obj


@dataclass
class RemoteReadingResponse(DataClassDictMixin):
    """Remote Reading Response dataclass."""

    status: int
    future_consumption_info: FutureConsumptionInfo = field(metadata=field_options(alias="futureConsumptionInfo"))
    from_date: Optional[date] = field(metadata=field_options(alias="fromDate"))
    to_date: Optional[date] = field(metadata=field_options(alias="toDate"))
    total_consumption_for_period: Optional[float] = field(metadata=field_options(alias="totalConsumptionForPeriod"))
    total_import_date_for_period: Optional[date] = field(metadata=field_options(alias="totalImportDateForPeriod"))
    meter_start_date: Optional[date] = field(metadata=field_options(alias="meterStartDate"))
    total_import: Optional[float] = field(metadata=field_options(alias="totalImport"))
    data: list[RemoteReading]
