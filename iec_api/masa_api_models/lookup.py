from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masaapi-wa.azurewebsites.net/lookup/all
#
#   {
#     "regions": [
#         {
#             "regionId": "909a5d57-d7db-ea11-a813-000d3aabca53",
#             "name": "חיפה והצפון",
#             "code": 7
#         } //...
#         ],
#     "connectionSizeTypes": [
#         {
#             "id": "7ddab873-671f-e911-a961-000d3a29f1fd",
#             "name": "6",
#             "sizeType": 279830001,
#             "voltType": 279830001,
#             "code": "Z01",
#             "description": "חד פאזי 6 אמפר (1X6)",
#             "index": 1,
#             "isEnlargeable": true,
#             "isAllowResidence": false
#         } //...
#         ],
#     "siteTypes": [
#         {
#             "key": 20,
#             "value": "_20",
#             "index": 0
#         }  //...
#         ],
#     "orderStatusState": [
#         {
#             "key": 279830000,
#             "value": "לא החל",
#             "index": 1
#         } //...,
#     ],
#     "actionCodes": [
#         {
#             "key": 1,
#             "value": "חיבורים חדשים",
#             "index": 1
#         } // ...
#     ],
#     "phonePrefixes": [
#         {
#             "key": 50,
#             "value": "050",
#             "index": 0
#         } // ...
#     ],
#     "orderPurposes": [
#         {
#             "desc": "מסחרי אחר",
#             "buildingType": 4,
#             "id": "811b52d8-68da-e911-a973-000d3a29f080",
#             "name": "מסחרי ואחר"
#         } // ...
#     ],
#     "meterSetupTypes": [
#         {
#             "id": "5c3544e4-68da-e911-a973-000d3a29f080",
#             "name": "ריכוז בכניסה לבניין ",
#             "desc": "ריכוז בכניסה לבניין",
#             "code": "Z1"
#         } // ...
#             ],
#     "stateMachineForOrderStage": null
# }


@dataclass
class Region(DataClassDictMixin):
    """
    Represents a geographic region.

    Attributes:
        region_id (UUID): The unique identifier for the region.
        name (str): The name of the region.
        code (int): The code associated with the region.
    """

    region_id: UUID = field(metadata=field_options(alias="regionId"))
    name: str = field(metadata=field_options(alias="name"))
    code: int = field(metadata=field_options(alias="code"))


@dataclass
class ConnectionSizeType(DataClassDictMixin):
    """
    Represents the type and specifications of a connection size.

    Attributes:
        id (UUID): The unique identifier for the connection size type.
        name (str): The name of the connection size type.
        size_type (int): The size type code.
        volt_type (int): The voltage type code.
        code (str): The code associated with the connection size type.
        description (str): A description of the connection size type.
        index (int): The index order of the connection size type.
        is_enlargeable (bool): Indicates if the connection size type can be enlarged.
        is_allow_residence (Optional[bool]): Indicates if the connection size type is allowed for residential use.
    """

    id: UUID = field(metadata=field_options(alias="id"))
    name: str = field(metadata=field_options(alias="name"))
    size_type: int = field(metadata=field_options(alias="sizeType"))
    volt_type: int = field(metadata=field_options(alias="voltType"))
    code: str = field(metadata=field_options(alias="code"))
    description: str = field(metadata=field_options(alias="description"))
    index: int = field(metadata=field_options(alias="index"))
    is_enlargeable: bool = field(metadata=field_options(alias="isEnlargeable"))
    is_allow_residence: Optional[bool] = field(metadata=field_options(alias="isAllowResidence"))


@dataclass
class SiteType(DataClassDictMixin):
    """
    Represents a type of site.

    Attributes:
        key (int): The unique key for the site type.
        value (str): The value or name of the site type.
        index (int): The index order of the site type.
    """

    key: int = field(metadata=field_options(alias="key"))
    value: str = field(metadata=field_options(alias="value"))
    index: int = field(metadata=field_options(alias="index"))


@dataclass
class OrderStatusState(DataClassDictMixin):
    """
    Represents the status of an order.

    Attributes:
        key (int): The unique key for the order status.
        value (str): The value or name of the order status.
        index (int): The index order of the order status.
    """

    key: int = field(metadata=field_options(alias="key"))
    value: str = field(metadata=field_options(alias="value"))
    index: int = field(metadata=field_options(alias="index"))


@dataclass
class ActionCode(DataClassDictMixin):
    """
    Represents an action code for operations.

    Attributes:
        key (int): The unique key for the action code.
        value (str): The value or name of the action code.
        index (int): The index order of the action code.
    """

    key: int = field(metadata=field_options(alias="key"))
    value: str = field(metadata=field_options(alias="value"))
    index: int = field(metadata=field_options(alias="index"))


@dataclass
class PhonePrefix(DataClassDictMixin):
    """
    Represents a phone prefix.

    Attributes:
        key (int): The unique key for the phone prefix.
        value (str): The value or number of the phone prefix.
        index (int): The index order of the phone prefix.
    """

    key: int = field(metadata=field_options(alias="key"))
    value: str = field(metadata=field_options(alias="value"))
    index: int = field(metadata=field_options(alias="index"))


@dataclass
class OrderPurpose(DataClassDictMixin):
    """
    Represents the purpose of an order.

    Attributes:
        desc (str): The description of the order purpose.
        building_type (Optional[int]): The type of building associated with the order purpose.
        id (UUID): The unique identifier for the order purpose.
        name (str): The name of the order purpose.
    """

    desc: str = field(metadata=field_options(alias="desc"))
    building_type: Optional[int] = field(metadata=field_options(alias="buildingType"))
    id: UUID = field(metadata=field_options(alias="id"))
    name: str = field(metadata=field_options(alias="name"))


@dataclass
class MeterSetupType(DataClassDictMixin):
    """
    Represents the setup type of a meter.

    Attributes:
        id (UUID): The unique identifier for the meter setup type.
        name (str): The name of the meter setup type.
        desc (str): A description of the meter setup type.
        code (str): The code associated with the meter setup type.
    """

    id: UUID = field(metadata=field_options(alias="id"))
    name: str = field(metadata=field_options(alias="name"))
    desc: str = field(metadata=field_options(alias="desc"))
    code: str = field(metadata=field_options(alias="code"))


@dataclass
class GetLookupResponse(DataClassDictMixin):
    """
    Represents the overall response structure containing various types of data.

    Attributes:
        regions (List[Region]): A list of geographic regions.
        connection_size_types (List[ConnectionSizeType]): A list of connection size types.
        site_types (List[SiteType]): A list of site types.
        order_status_state (List[OrderStatusState]): A list of order status states.
        action_codes (List[ActionCode]): A list of action codes.
        phone_prefixes (List[PhonePrefix]): A list of phone prefixes.
        order_purposes (List[OrderPurpose]): A list of order purposes.
        meter_setup_types (List[MeterSetupType]): A list of meter setup types.
        state_machine_for_order_stage (Optional[str]): A placeholder for the state machine for order stages.
    """

    regions: List[Region] = field(metadata=field_options(alias="regions"))
    connection_size_types: List[ConnectionSizeType] = field(metadata=field_options(alias="connectionSizeTypes"))
    site_types: List[SiteType] = field(metadata=field_options(alias="siteTypes"))
    order_status_state: List[OrderStatusState] = field(metadata=field_options(alias="orderStatusState"))
    action_codes: List[ActionCode] = field(metadata=field_options(alias="actionCodes"))
    phone_prefixes: List[PhonePrefix] = field(metadata=field_options(alias="phonePrefixes"))
    order_purposes: List[OrderPurpose] = field(metadata=field_options(alias="orderPurposes"))
    meter_setup_types: List[MeterSetupType] = field(metadata=field_options(alias="meterSetupTypes"))
    state_machine_for_order_stage: Optional[str] = field(metadata=field_options(alias="stateMachineForOrderStage"))
