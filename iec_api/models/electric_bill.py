""" Electric Bills. """

from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.invoice import Invoice
from iec_api.models.response_descriptor import ResponseWithDescriptor

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
#         "isSuccess": true,
#         "code": null,
#         "description": null
#     }
# }


@dataclass
class ElectricBill(DataClassDictMixin):
    total_amount_to_pay: float = field(metadata=field_options(alias="totalAmountToPay"))
    total_invoices_to_pay: int = field(
        metadata=field_options(alias="totalInvoicesToPay")
    )
    last_date_to_pay: str = field(metadata=field_options(alias="lastDateToPay"))
    invoices: list[Invoice]


decoder = BasicDecoder(ResponseWithDescriptor[ElectricBill])
