# Customer Mobile Model

from dataclasses import dataclass, field
from typing import List

from mashumaro import DataClassDictMixin, field_options

# GET https://iecapi.iec.co.il/api/customer/mobile/{contractNumber}
#
# {
#  "customer": {
#    "bpNumber": "123456789",
#    "idType": 1,
#    "accounts": [
#      {
#        "mainContractId": "123456789",
#        "mainContractIdType": 1,
#        "companyId": "123456789",
#        "name": "John Doe",
#        "bpNumber": "123456789",
#        "bpType": 1,
#        "isActiveAccount": true,
#        "customerRole": 0,
#        "accountType": 1
#      }
#    ],
#    "customerStatus": 1,
#    "idNumber": "123456789",
#    "firstName": "John",
#    "lastName": "Doe",
#    "mobilePhone": "0501234567",
#    "email": "john.doe@example.com"
#  },
#  "contract": {
#    "address": "Example Street 1, Example City",
#    "contractId": "123456789",
#    "totalDebt": 0.0,
#    "frequency": 0,
#    "status": 0,
#    "fromPativteProducer": true,
#    "cityCode": "1234",
#    "cityName": "Example City",
#    "streetCode": "1234",
#    "streetName": "Example Street",
#    "houseNumber": "1",
#    "debtForInvoicesDueDateNotPassed": 0.0,
#    "isTouz": false,
#    "smartMeter": true,
#    "producerType": 0,
#    "isDomestic": false
#  }
# }


@dataclass
class CustomerMobileAccount(DataClassDictMixin):
    """Account information in customer mobile response.

    Attributes:
        main_contract_id: The main contract ID.
        main_contract_id_type: The main contract ID type.
        company_id: The company ID.
        name: The account holder name.
        bp_number: The BP number.
        bp_type: The BP type.
        is_active_account: Whether the account is active.
        customer_role: The customer role.
        account_type: The account type.
    """

    main_contract_id: str = field(metadata=field_options(alias="mainContractId"))
    main_contract_id_type: int = field(metadata=field_options(alias="mainContractIdType"))
    company_id: str = field(metadata=field_options(alias="companyId"))
    name: str = field(metadata=field_options(alias="name"))
    bp_number: str = field(metadata=field_options(alias="bpNumber"))
    bp_type: int = field(metadata=field_options(alias="bpType"))
    is_active_account: bool = field(metadata=field_options(alias="isActiveAccount"))
    customer_role: int = field(metadata=field_options(alias="customerRole"))
    account_type: int = field(metadata=field_options(alias="accountType"))


@dataclass
class CustomerMobileInfo(DataClassDictMixin):
    """Customer information in mobile response.

    Attributes:
        bp_number: The BP number.
        id_type: The ID type.
        accounts: List of customer accounts.
        customer_status: The customer status.
        id_number: The ID number.
        first_name: The first name.
        last_name: The last name.
        mobile_phone: The mobile phone number.
        email: The email address.
    """

    bp_number: str = field(metadata=field_options(alias="bpNumber"))
    id_type: int = field(metadata=field_options(alias="idType"))
    accounts: List[CustomerMobileAccount] = field(metadata=field_options(alias="accounts"))
    customer_status: int = field(metadata=field_options(alias="customerStatus"))
    id_number: str = field(metadata=field_options(alias="idNumber"))
    first_name: str = field(metadata=field_options(alias="firstName"))
    last_name: str = field(metadata=field_options(alias="lastName"))
    mobile_phone: str = field(metadata=field_options(alias="mobilePhone"))
    email: str = field(metadata=field_options(alias="email"))


@dataclass
class CustomerMobileContract(DataClassDictMixin):
    """Contract information in customer mobile response.

    Attributes:
        address: The full address.
        contract_id: The contract ID.
        total_debt: The total debt amount.
        frequency: The frequency.
        status: The status.
        from_private_producer: Whether from private producer.
        city_code: The city code.
        city_name: The city name.
        street_code: The street code.
        street_name: The street name.
        house_number: The house number.
        debt_for_invoices_due_date_not_passed: Debt for invoices not yet due.
        is_touz: Whether is TOUZ.
        smart_meter: Whether has smart meter.
        producer_type: The producer type.
        is_domestic: Whether is domestic.
    """

    address: str = field(metadata=field_options(alias="address"))
    contract_id: str = field(metadata=field_options(alias="contractId"))
    total_debt: float = field(metadata=field_options(alias="totalDebt"))
    frequency: int = field(metadata=field_options(alias="frequency"))
    status: int = field(metadata=field_options(alias="status"))
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
    is_domestic: bool = field(metadata=field_options(alias="isDomestic"))


@dataclass
class CustomerMobileResponse(DataClassDictMixin):
    """Response model for customer mobile endpoint.

    Attributes:
        customer: The customer information.
        contract: The contract information.
    """

    customer: CustomerMobileInfo = field(metadata=field_options(alias="customer"))
    contract: CustomerMobileContract = field(metadata=field_options(alias="contract"))
