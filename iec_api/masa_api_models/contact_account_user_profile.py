from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masa-mainportalapi.iec.co.il/api/contacts/account/0/userprofile
#
# {
#  "governmentid": "123456789",
#  "idType": 279830001,
#  "firstName": "John",
#  "lastName": "Doe",
#  "email": "john.doe@example.com",
#  "phoneNumber": "1234567",
#  "accounts": [
#    {
#      "name": "John Doe",
#      "accountNumber": "123456789",
#      "governmentNumber": "123456789",
#      "viewTypeCode": 1,
#      "identificationType": 279830001,
#      "consumptionOrderViewTypeCode": 1,
#      "isRegisteredOnDigitalBit": true,
#      "kindOfAccountCode": 1,
#      "id": "00000000-0000-0000-0000-000000000001",
#      "logicalName": "account",
#      "stateCode": 0
#    }
#  ],
#  "phonePrefix": "050",
#  "isConnectedToPrivateAccount": true,
#  "isAccountOwner": true,
#  "isAccountContact": false,
#  "connectionBetweenContactAndContract": [
#    {
#      "contract": {
#        "isMatam": false,
#        "supplyCode": 1,
#        "isPrivateProducer": false,
#        "overloadRateSwitchBit": false,
#        "contractAccNumberInShoval": 123456789,
#        "account": {
#          "name": "John Doe",
#          "consumptionOrderViewTypeCode": 1,
#          "id": "00000000-0000-0000-0000-000000000001",
#          "logicalName": "account"
#        },
#        "id": "00000000-0000-0000-0000-000000000002",
#        "logicalName": "iec_contract",
#        "stateCode": 1
#      },
#      "account": {
#        "name": "John Doe",
#        "accountNumber": "123456789",
#        "governmentNumber": "123456789",
#        "viewTypeCode": 1,
#        "identificationType": 279830001,
#        "consumptionOrderViewTypeCode": 1,
#        "isRegisteredOnDigitalBit": true,
#        "kindOfAccountCode": 1,
#        "id": "00000000-0000-0000-0000-000000000001",
#        "logicalName": "account",
#        "stateCode": 0
#      },
#      "defaultContractBit": true,
#      "partConnectionCode": 1,
#      "tokenExpirationDate": "0001-01-01T00:00:00Z",
#      "id": "00000000-0000-0000-0000-000000000003",
#      "logicalName": "iec_connectionbetweencontactandcontract"
#    }
#  ],
#  "verificationStatus": true,
#  "id": "00000000-0000-0000-0000-000000000004",
#  "logicalName": "contact"
# }


@dataclass
class MainPortalStreet(DataClassDictMixin):
    """Represents a street in the main portal API.

    Attributes:
        name: The name of the street.
        shoval_street_code: The Shoval street code.
        id: The unique identifier for the street.
        logical_name: The logical name of the entity.
    """

    name: str = field(metadata=field_options(alias="name"))
    shoval_street_code: str = field(metadata=field_options(alias="shovalStreetCode"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class MainPortalCity(DataClassDictMixin):
    """Represents a city in the main portal API.

    Attributes:
        name: The name of the city.
        shoval_city_code: The Shoval city code.
        city_code: The city code.
        id: The unique identifier for the city.
        logical_name: The logical name of the entity.
    """

    name: str = field(metadata=field_options(alias="name"))
    shoval_city_code: str = field(metadata=field_options(alias="shovalCityCode"))
    city_code: int = field(metadata=field_options(alias="cityCode"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class MainPortalAddress(DataClassDictMixin):
    """Represents an address in the main portal API.

    Attributes:
        street: The street information.
        city: The city information.
        house_number: The house number.
        id: The unique identifier for the address.
        logical_name: The logical name of the entity.
    """

    street: MainPortalStreet = field(metadata=field_options(alias="street"))
    city: MainPortalCity = field(metadata=field_options(alias="city"))
    house_number: str = field(metadata=field_options(alias="houseNumber"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class MainPortalSite(DataClassDictMixin):
    """Represents a site in the main portal API.

    Attributes:
        full_address: The full address string.
        address: The address details.
        smart_code: The smart code.
        is_smart: Whether the site is smart.
        id: The unique identifier for the site.
        logical_name: The logical name of the entity.
    """

    full_address: str = field(metadata=field_options(alias="fullAddress"))
    address: MainPortalAddress = field(metadata=field_options(alias="address"))
    smart_code: int = field(metadata=field_options(alias="smartCode"))
    is_smart: bool = field(metadata=field_options(alias="isSmart"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class SimpleAccount(DataClassDictMixin):
    """Represents a simplified account reference in the main portal API.

    Attributes:
        name: The name of the account.
        consumption_order_view_type_code: The view type code for consumption order.
        id: The unique identifier for the account.
        logical_name: The logical name of the entity.
    """

    name: str = field(metadata=field_options(alias="name"))
    consumption_order_view_type_code: int = field(metadata=field_options(alias="consumptionOrderViewTypeCode"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class MainPortalContract(DataClassDictMixin):
    """Represents a contract in the main portal API.

    Attributes:
        site: The site information.
        is_matam: Whether the contract is matam.
        supply_code: The supply code.
        is_private_producer: Whether the contract is for a private producer.
        overload_rate_switch_bit: The overload rate switch bit.
        contract_acc_number_in_shoval: The contract account number in Shoval.
        account: The account reference.
        id: The unique identifier for the contract.
        logical_name: The logical name of the entity.
        state_code: The state code.
    """

    is_matam: bool = field(metadata=field_options(alias="isMatam"))
    supply_code: int = field(metadata=field_options(alias="supplyCode"))
    is_private_producer: bool = field(metadata=field_options(alias="isPrivateProducer"))
    overload_rate_switch_bit: bool = field(metadata=field_options(alias="overloadRateSwitchBit"))
    contract_acc_number_in_shoval: int = field(metadata=field_options(alias="contractAccNumberInShoval"))
    account: SimpleAccount = field(metadata=field_options(alias="account"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
    state_code: int = field(metadata=field_options(alias="stateCode"))
    site: Optional[MainPortalSite] = field(default=None, metadata=field_options(alias="site"))


@dataclass
class ConnectionType(DataClassDictMixin):
    """Represents a connection type in the main portal API.

    Attributes:
        name: The name of the connection type.
        connection_type_int: The connection type integer value.
        id: The unique identifier for the connection type.
        logical_name: The logical name of the entity.
    """

    name: str = field(metadata=field_options(alias="name"))
    connection_type_int: int = field(metadata=field_options(alias="connectionTypeInt"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class MainPortalFullAccount(DataClassDictMixin):
    """Represents a full account in the main portal API.

    Attributes:
        name: The name of the account.
        account_number: The account number.
        government_number: The government ID associated with the account.
        view_type_code: The view type code for the account.
        identification_type: The type of identification used for the account.
        consumption_order_view_type_code: The view type code for consumption order.
        is_registered_on_digital_bit: Whether the account is registered on Digital Bit.
        kind_of_account_code: The kind of account code.
        id: The unique identifier for the account.
        logical_name: The logical name of the entity.
        state_code: The state code.
    """

    name: str = field(metadata=field_options(alias="name"))
    account_number: str = field(metadata=field_options(alias="accountNumber"))
    government_number: str = field(metadata=field_options(alias="governmentNumber"))
    view_type_code: int = field(metadata=field_options(alias="viewTypeCode"))
    identification_type: int = field(metadata=field_options(alias="identificationType"))
    consumption_order_view_type_code: int = field(metadata=field_options(alias="consumptionOrderViewTypeCode"))
    is_registered_on_digital_bit: bool = field(metadata=field_options(alias="isRegisteredOnDigitalBit"))
    kind_of_account_code: int = field(metadata=field_options(alias="kindOfAccountCode"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
    state_code: int = field(metadata=field_options(alias="stateCode"))


@dataclass
class ConnectionBetweenContactAndContract(DataClassDictMixin):
    """Represents a connection between contact and contract in the main portal API.

    Attributes:
        contract: The contract information.
        account: The account information.
        default_contract_bit: Whether this is the default contract.
        part_connection_code: The part connection code.
        token_expiration_date: The token expiration date.
        id: The unique identifier for the connection.
        logical_name: The logical name of the entity.
        connection_type: The connection type information.
    """

    contract: MainPortalContract = field(metadata=field_options(alias="contract"))
    account: MainPortalFullAccount = field(metadata=field_options(alias="account"))
    default_contract_bit: bool = field(metadata=field_options(alias="defaultContractBit"))
    part_connection_code: int = field(metadata=field_options(alias="partConnectionCode"))
    token_expiration_date: str = field(metadata=field_options(alias="tokenExpirationDate"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
    connection_type: Optional[ConnectionType] = field(default=None, metadata=field_options(alias="connectionType"))


@dataclass
class MasaMainPortalContactAccountUserProfile(DataClassDictMixin):
    """Represents a contact's user profile with accounts and contract connections from MASA Main Portal API.

    Attributes:
        government_id: The government ID of the contact.
        id_type: The type of ID used.
        first_name: The first name of the contact.
        last_name: The last name of the contact.
        email: The email address of the contact.
        phone_number: The phone number of the contact.
        accounts: A list of accounts associated with the contact.
        phone_prefix: The phone prefix of the contact.
        is_connected_to_private_account: Indicates if the contact is connected to a private account.
        is_account_owner: Indicates if the contact is the owner of the account.
        is_account_contact: Indicates if the contact is an account contact.
        connection_between_contact_and_contract: A list of connections between contact and contracts.
        verification_status: The verification status of the contact.
        id: The unique identifier for the contact.
        logical_name: The logical name of the entity.
    """

    government_id: str = field(metadata=field_options(alias="governmentid"))
    id_type: int = field(metadata=field_options(alias="idType"))
    first_name: str = field(metadata=field_options(alias="firstName"))
    last_name: str = field(metadata=field_options(alias="lastName"))
    email: str = field(metadata=field_options(alias="email"))
    phone_number: str = field(metadata=field_options(alias="phoneNumber"))
    accounts: List[MainPortalFullAccount] = field(metadata=field_options(alias="accounts"))
    phone_prefix: str = field(metadata=field_options(alias="phonePrefix"))
    is_connected_to_private_account: bool = field(metadata=field_options(alias="isConnectedToPrivateAccount"))
    is_account_owner: bool = field(metadata=field_options(alias="isAccountOwner"))
    is_account_contact: bool = field(metadata=field_options(alias="isAccountContact"))
    connection_between_contact_and_contract: List[ConnectionBetweenContactAndContract] = field(
        metadata=field_options(alias="connectionBetweenContactAndContract")
    )
    verification_status: bool = field(metadata=field_options(alias="verificationStatus"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
