""" Customer model. """

# URL:
# POST https://iecapi.iec.co.il/api/customer
# Headers: Authorization: Bearer ...

# Response: 
# {
#     "bpNumber": "...",
#     "idType": 1,
#     "accounts": [
#         {
#             "mainContractId": "...",
#             "mainContractIdType": 1,
#             "companyId": "...",
#             "name": "...",
#             "lastName": "...",
#             "bpNumber": "...",
#             "bpType": 1,
#             "isActiveAccount": true,
#             "customerRole": 0,
#             "accountType": 1
#         }
#     ],
#     "customerStatus": 1,
#     "idNumber": "...",
#     "firstName": "...",
#     "lastName": "...",
#     "mobilePhone": "...",
#     "email": "..."
# } 

from dataclasses import dataclass, field
from response_descriptor import ResponseDescriptor
from mashumaro import DataClassDictMixin, field_options


@dataclass
class Contract(DataClassDictMixin):
    address: str
    contract_id: str = field(metadata=field_options(alias="contractId"))
    due_date: str = field(metadata=field_options(alias="dueDate"))
    total_debt: float = field(metadata=field_options(alias="totalDebt"))
    frequency: int
    status: int
    from_pativte_producer: bool = field(metadata=field_options(alias="fromPativteProducer"))
    city_code: str = field(metadata=field_options(alias="cityCode"))
    city_name: str = field(metadata=field_options(alias="cityName"))
    street_code: str = field(metadata=field_options(alias="streetCode"))
    street_name: str = field(metadata=field_options(alias="streetName"))
    house_number: str = field(metadata=field_options(alias="houseNumber"))
    debt_for_invoices_due_date_not_passed: float = field(metadata=field_options(alias="debtForInvoicesDueDateNotPassed"))
    is_touz: bool = field(metadata=field_options(alias="isTouz"))
    smart_meter: bool = field(metadata=field_options(alias="smartMeter"))
    producer_type: int = field(metadata=field_options(alias="producerType"))


@dataclass
class Contracts(DataClassDictMixin):
    contracts: list[Contract]
    contract_amount: int
    total_to_pay: float


@dataclass
class GetContractResponse(DataClassDictMixin):
    data: Contracts
    response_descriptor: ResponseDescriptor = field(metadata=field_options(alias="responseDescriptor"))
