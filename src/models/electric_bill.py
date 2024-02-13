""" Electric Bills. """

from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options
from src.models.response_descriptor import ResponseDescriptor

# GET https://iecapi.iec.co.il//api/ElectricBillsDrawers/ElectricBills/{contract_id}/{bp_number}
#
# {
#     "data": {
#         "totalAmountToPay": 0,
#         "totalInvoicesToPay": 0,
#         "lastDateToPay": null,
#         "invoices": [
#             {
#                 "fullDate": "2024-01-01T00:00:00",
#                 "fromDate": "2023-11-15T00:00:00",
#                 "toDate": "2024-01-17T00:00:00",
#                 "amountOrigin": 100.00,
#                 "amountToPay": 0,
#                 "amountPaid": 100.00,
#                 "invoiceId": 12345,
#                 "contractNumber": 12345, //= contract_id
#                 "orderNumber": 0,
#                 "lastDate": "07/02/2024",
#                 "invoicePaymentStatus": 1,
#                 "documentID": "1",
#                 "daysPeriod": 64,
#                 "hasDirectDebit": false,
#                 "invoiceType": 0
#             }
#         ]
#     },
#     "reponseDescriptor": {
#         "isSuccess": false,
#         "code": null,
#         "description": null
#     }
# }




@dataclass
class Invoice(DataClassDictMixin):
    full_date: str = field(metadata=field_options(alias="fullDate"))
    from_date: str = field(metadata=field_options(alias="fromDate"))
    to_date: str = field(metadata=field_options(alias="toDate"))
    amount_origin: float = field(metadata=field_options(alias="amountOrigin"))
    amount_to_pay: float = field(metadata=field_options(alias="amountToPay"))
    amount_paid: float = field(metadata=field_options(alias="amountPaid"))
    invoice_id: int = field(metadata=field_options(alias="invoiceId"))
    contract_number: int = field(metadata=field_options(alias="contractNumber"))
    order_number: int = field(metadata=field_options(alias="orderNumber"))
    last_date: str = field(metadata=field_options(alias="lastDate"))
    invoice_payment_status: int = field(
        metadata=field_options(alias="invoicePaymentStatus")
    )
    document_id: str = field(metadata=field_options(alias="documentId"))
    days_period: str = field(metadata=field_options(alias="daysPeriod"))
    has_direct_debit: bool = field(metadata=field_options(alias="hasDirectDebit"))
    invoice_type: int = field(metadata=field_options(alias="invoiceType"))


@dataclass
class Invoices(DataClassDictMixin):
    total_amount_to_pay: float = field(metadata=field_options(alias="totalAmountToPay"))
    total_invoices_to_pay: int = field(
        metadata=field_options(alias="totalInvoicesToPay")
    )
    last_date_to_pay: str = field(metadata=field_options(alias="lastDateToPay"))
    invoices: list[Invoice]


@dataclass
class GetElectricBillResponse(DataClassDictMixin):
    data: Invoices
    response_descriptor: ResponseDescriptor = field(
        metadata=field_options(alias="responseDescriptor")
    )
