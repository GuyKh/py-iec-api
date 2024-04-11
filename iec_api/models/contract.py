""" Contract model. """

from dataclasses import dataclass, field
from datetime import date

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

# GET https://iecapi.iec.co.il//api/customer/contract/{bp_number}?count=1
#
#
# {
#     "data": {
#         "contracts": [
#             {
#                 "address": "הכתובת שלי",
#                 "contractId": "0001234",
#                 "dueDate": "1900-01-01",
#                 "totalDebt": 0.0,
#                 "frequency": 2,
#                 "status": 1,
#                 "fromPativteProducer": false,
#                 "cityCode": "000000001864",
#                 "cityName": "תל אביב - יפו",
#                 "streetCode": "00000000111",
#                 "streetName": "נמיר",
#                 "houseNumber": "22",
#                 "debtForInvoicesDueDateNotPassed": 0.0,
#                 "isTouz": false,
#                 "smartMeter": false,
#                 "producerType": 1
#             }
#         ],
#         "contractAmount": 1,
#         "totalToPay": 0.0
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "0",
#         "description": ""
#     }
# }


@dataclass
class Contract(DataClassDictMixin):
    address: str
    contract_id: str = field(metadata=field_options(alias="contractId"))
    due_date: date = field(metadata=field_options(alias="dueDate"))
    total_debt: float = field(metadata=field_options(alias="totalDebt"))
    frequency: int
    status: int
    from_private_producer: bool = field(metadata=field_options(alias="fromPativteProducer"))
    city_code: str = field(metadata=field_options(alias="cityCode"))
    city_name: str = field(metadata=field_options(alias="cityName"))
    street_code: str = field(metadata=field_options(alias="streetCode"))
    street_name: str = field(metadata=field_options(alias="streetName"))
    house_number: str = field(metadata=field_options(alias="houseNumber"))
    debt_for_invoices_due_date_not_passed: float = field(
        metadata=field_options(alias="debtForInvoicesDueDateNotPassed")
    )
    is_touz: bool = field(metadata=field_options(alias="isTouz"))
    smart_meter: bool = field(metadata=field_options(alias="smartMeter"))
    producer_type: int = field(metadata=field_options(alias="producerType"))


@dataclass
class Contracts(DataClassDictMixin):
    contracts: list[Contract]
    contract_amount: int = field(metadata=field_options(alias="contractAmount"))
    total_to_pay: float = field(metadata=field_options(alias="totalToPay"))


decoder = BasicDecoder(ResponseWithDescriptor[Contracts])
