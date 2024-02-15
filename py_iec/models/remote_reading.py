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

from mashumaro import DataClassDictMixin, field_options


@dataclass
class RemoteReadingRequest:
    """Remote Reading Request ."""
    meterSerialNumber: str  # noqa: N815
    meterCode: int  # noqa: N815
    lastInvoiceDate: str  # noqa: N815
    fromDate: str  # noqa: N815
    resolution: int


@dataclass
class FutureConsumptionInfo(DataClassDictMixin):
    """Future Consumption Info dataclass."""

    last_invoice_date: str = field(metadata=field_options(alias="lastInvoiceDate"))
    current_date: str = field(metadata=field_options(alias="currentDate"))
    future_consumption: float = field(metadata=field_options(alias="futureConsumption"))
    total_import: float = field(metadata=field_options(alias="totalImport"))
    total_import_date: str = field(metadata=field_options(alias="totalImportDate"))


@dataclass
class RemoteReadingData(DataClassDictMixin):
    """Remote Reading Data dataclass."""

    status: int
    date: str
    value: float


@dataclass
class RemoteReadingResponse(DataClassDictMixin):
    """Remote Reading Response dataclass."""

    status: int
    future_consumption_info: FutureConsumptionInfo = field(
        metadata=field_options(alias="futureConsumptionInfo")
    )
    from_date: str = field(metadata=field_options(alias="from_date"))
    to_date: str = field(metadata=field_options(alias="to_date"))
    total_consumption_for_period: float = field(
        metadata=field_options(alias="totalConsumptionForPeriod")
    )
    total_import_date_for_period: str = field(
        metadata=field_options(alias="totalImportDateForPeriod")
    )
    meter_start_date: str = field(metadata=field_options(alias="meterStartDate"))
    total_import: float = field(metadata=field_options(alias="totalImport"))
    data: RemoteReadingData
