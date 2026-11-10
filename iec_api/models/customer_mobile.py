# Customer Mobile Model

from dataclasses import dataclass, field
from typing import List, Optional

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

    main_contract_id: Optional[str] = field(default=None, metadata=field_options(alias="mainContractId"))
    main_contract_id_type: Optional[int] = field(default=None, metadata=field_options(alias="mainContractIdType"))
    company_id: Optional[str] = field(default=None, metadata=field_options(alias="companyId"))
    name: Optional[str] = field(default=None, metadata=field_options(alias="name"))
    bp_number: Optional[str] = field(default=None, metadata=field_options(alias="bpNumber"))
    bp_type: Optional[int] = field(default=None, metadata=field_options(alias="bpType"))
    is_active_account: Optional[bool] = field(default=None, metadata=field_options(alias="isActiveAccount"))
    customer_role: Optional[int] = field(default=None, metadata=field_options(alias="customerRole"))
    account_type: Optional[int] = field(default=None, metadata=field_options(alias="accountType"))


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

    bp_number: Optional[str] = field(default=None, metadata=field_options(alias="bpNumber"))
    id_type: Optional[int] = field(default=None, metadata=field_options(alias="idType"))
    accounts: Optional[List[CustomerMobileAccount]] = field(default=None, metadata=field_options(alias="accounts"))
    customer_status: Optional[int] = field(default=None, metadata=field_options(alias="customerStatus"))
    id_number: Optional[str] = field(default=None, metadata=field_options(alias="idNumber"))
    first_name: Optional[str] = field(default=None, metadata=field_options(alias="firstName"))
    last_name: Optional[str] = field(default=None, metadata=field_options(alias="lastName"))
    mobile_phone: Optional[str] = field(default=None, metadata=field_options(alias="mobilePhone"))
    email: Optional[str] = field(default=None, metadata=field_options(alias="email"))


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

    address: Optional[str] = field(default=None, metadata=field_options(alias="address"))
    contract_id: Optional[str] = field(default=None, metadata=field_options(alias="contractId"))
    total_debt: Optional[float] = field(default=None, metadata=field_options(alias="totalDebt"))
    frequency: Optional[int] = field(default=None, metadata=field_options(alias="frequency"))
    status: Optional[int] = field(default=None, metadata=field_options(alias="status"))
    from_private_producer: Optional[bool] = field(default=None, metadata=field_options(alias="fromPativteProducer"))
    city_code: Optional[str] = field(default=None, metadata=field_options(alias="cityCode"))
    city_name: Optional[str] = field(default=None, metadata=field_options(alias="cityName"))
    street_code: Optional[str] = field(default=None, metadata=field_options(alias="streetCode"))
    street_name: Optional[str] = field(default=None, metadata=field_options(alias="streetName"))
    house_number: Optional[str] = field(default=None, metadata=field_options(alias="houseNumber"))
    debt_for_invoices_due_date_not_passed: Optional[float] = field(
        default=None, metadata=field_options(alias="debtForInvoicesDueDateNotPassed")
    )
    is_touz: Optional[bool] = field(default=None, metadata=field_options(alias="isTouz"))
    smart_meter: Optional[bool] = field(default=None, metadata=field_options(alias="smartMeter"))
    producer_type: Optional[int] = field(default=None, metadata=field_options(alias="producerType"))
    is_domestic: Optional[bool] = field(default=None, metadata=field_options(alias="isDomestic"))


@dataclass
class CustomerMobileResponse(DataClassDictMixin):
    """Response model for customer mobile endpoint.

    Attributes:
        customer: The customer information.
        contract: The contract information.
    """

    customer: Optional[CustomerMobileInfo] = field(default=None, metadata=field_options(alias="customer"))
    contract: Optional[CustomerMobileContract] = field(default=None, metadata=field_options(alias="contract"))
