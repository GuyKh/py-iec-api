from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.commons import convert_to_tz_aware_datetime
from iec_api.models.meter_reading import MeterReading
from iec_api.models.models_commons import FormattedDate
from iec_api.models.response_descriptor import ResponseWithDescriptor

# GET https://iecapi.iec.co.il//api/billingCollection/invoices/{bp_number}/{contract_number}
#
# {
#     "data": {
#         "property": {
#             "areaId": "111",
#             "districtId": 1
#         },
#         "invoices": [
#             {
#                 "consumption": 123.0,
#                 "readingCode": 1,
#                 "meterReadings": [
#                     {
#                         "reading": 123,
#                         "readingCode": null,
#                         "readingDate": "0001-01-01T00:00:00",
#                         "usage": null,
#                         "serialNumber": "000000000020008389"
#                     }
#                 ],
#                 "fullDate": "2020-11-01T00:00:00",
#                 "fromDate": "2020-09-09T00:00:00",
#                 "toDate": "2020-11-08T00:00:00",
#                 "amountOrigin": 123.51,
#                 "amountToPay": 0,
#                 "amountPaid": 123.51,
#                 "invoiceId": 123456,
#                 "contractNumber": 123456,
#                 "orderNumber": 0,
#                 "lastDate": "01/12/2020",
#                 "invoicePaymentStatus": 1,
#                 "documentID": "1",
#                 "daysPeriod": 61,
#                 "hasDirectDebit": false,
#                 "invoiceType": 0
#             }
#         ]
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "00",
#         "description": "OK"
#     }
# }


@dataclass
class Invoice(DataClassDictMixin):
    full_date: Optional[datetime] = field(metadata=field_options(alias="fullDate"))
    from_date: Optional[datetime] = field(metadata=field_options(alias="fromDate"))
    to_date: Optional[datetime] = field(metadata=field_options(alias="toDate"))
    amount_origin: float = field(metadata=field_options(alias="amountOrigin"))
    amount_to_pay: float = field(metadata=field_options(alias="amountToPay"))
    amount_paid: float = field(metadata=field_options(alias="amountPaid"))
    invoice_id: int = field(metadata=field_options(alias="invoiceId"))
    contract_number: int = field(metadata=field_options(alias="contractNumber"))
    order_number: int = field(metadata=field_options(alias="orderNumber"))
    last_date: Optional[date] = field(
        metadata=field_options(alias="lastDate", serialization_strategy=FormattedDate("%d/%m/%Y"))
    )
    invoice_payment_status: int = field(metadata=field_options(alias="invoicePaymentStatus"))
    document_id: str = field(metadata=field_options(alias="documentID"))
    days_period: str = field(metadata=field_options(alias="daysPeriod"))
    has_direct_debit: bool = field(metadata=field_options(alias="hasDirectDebit"))
    invoice_type: int = field(metadata=field_options(alias="invoiceType"))

    reading_code: int = field(metadata=field_options(alias="readingCode"), default=0)
    consumption: int = field(metadata=field_options(alias="consumption"), default=0)
    meter_readings: list[MeterReading] = field(
        metadata=field_options(alias="meterReadings"), default_factory=lambda: []
    )

    @classmethod
    def __post_deserialize__(cls, obj: "Invoice") -> "Invoice":
        obj.full_date = convert_to_tz_aware_datetime(obj.full_date)
        obj.from_date = convert_to_tz_aware_datetime(obj.from_date)
        obj.to_date = convert_to_tz_aware_datetime(obj.to_date)
        return obj


@dataclass
class Property(DataClassDictMixin):
    """Property Response dataclass."""

    area_id: str = field(metadata=field_options(alias="areaId"))
    district_id: int = field(metadata=field_options(alias="districtId"))


@dataclass
class GetInvoicesBody(DataClassDictMixin):
    """Get Invoices Response dataclass."""

    property: Property
    invoices: list[Invoice]


decoder = BasicDecoder(ResponseWithDescriptor[GetInvoicesBody])
