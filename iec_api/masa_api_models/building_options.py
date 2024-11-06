from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masaapi-wa.azurewebsites.net/lookup/newConnection/buildingOptions
#
# {
#     "residenceOptions": [
#         {
#             "orderPurpose": {
#                 "desc": "בית בודד",
#                 "buildingType": 1,
#                 "id": "a31b52d8-68da-e911-a973-000d3a29f080",
#                 "name": "מגורים צמודי קרקע"
#             },
#             "connectionSizes": [
#                 {
#                     "id": "84dab873-671f-e911-a961-000d3a29f1fd",
#                     "name": "חד פאזי 40 אמפר (1X40)"
#                 } //..
#             ]
#         },
#         {
#             "orderPurpose": {
#                 "desc": "דו משפחתי",
#                 "buildingType": 1,
#                 "id": "ae1b52d8-68da-e911-a973-000d3a29f080",
#                 "name": "צ.קרקע אחד מדו-משפחתי"
#             },
#             "connectionSizes": [
#                 {
#                     "id": "84dab873-671f-e911-a961-000d3a29f1fd",
#                     "name": "חד פאזי 40 אמפר (1X40)"
#                 } //..
#             ]
#         }
#     ],
#     "commercialOptions": [
#         {
#             "orderPurpose": {
#                 "desc": "חיבור אחד בפילר/ מערכת מנייה",
#                 "buildingType": 3,
#                 "id": "ab1b52d8-68da-e911-a973-000d3a29f080",
#                 "name": "לא מגורים בפילר מונים"
#             },
#             "connectionSizes": [
#                 {
#                     "id": "7ddab873-671f-e911-a961-000d3a29f1fd",
#                     "name": "חד פאזי 6 אמפר (1X6)"
#                 } //..
#             ]
#         },
#         {
#             "orderPurpose": {
#                 "desc": "חיבור אחד בפילר לשני מונים",
#                 "buildingType": 1,
#                 "id": "b91b52d8-68da-e911-a973-000d3a29f080",
#                 "name": "לא מגורים בפילר-אחד מתוך דו-משפחתי"
#             },
#             "connectionSizes": [
#                 {
#                     "id": "84dab873-671f-e911-a961-000d3a29f1fd",
#                     "name": "חד פאזי 40 אמפר (1X40)"
#                 } //...
#             ]
#         }
#     ],
#     "tempOptions": [
#         {
#             "orderPurpose": {
#                 "desc": "חיבור זמני לאתר בניה",
#                 "buildingType": 6,
#                 "id": "8f1b52d8-68da-e911-a973-000d3a29f080",
#                 "name": "חיבור ארעי"
#             },
#             "connectionSizes": [
#                 {
#                     "id": "84dab873-671f-e911-a961-000d3a29f1fd",
#                     "name": "חד פאזי 40 אמפר (1X40)"
#                 } //...
#             ]
#         }
#     ],
#     "residenceSizeTypes": [
#         {
#             "id": "84dab873-671f-e911-a961-000d3a29f1fd",
#             "name": "חד פאזי 40 אמפר (1X40)"
#         } // ...
#     ],
#     "commercialSizeTypes": [
#         {
#             "id": "84dab873-671f-e911-a961-000d3a29f1fd",
#             "name": "חד פאזי 40 אמפר (1X40)"
#         },
#         {
#             "id": "85dab873-671f-e911-a961-000d3a29f1fd",
#             "name": "תלת פאזי 25 אמפר (3X25)"
#         } // ..
#     ],
#     "publicSizeTypes": [
#         {
#             "id": "84dab873-671f-e911-a961-000d3a29f1fd",
#             "name": "חד פאזי 40 אמפר (1X40)"
#         } //...
#     ],
#     "parkingSizeTypes": [
#         {
#             "id": "84dab873-671f-e911-a961-000d3a29f1fd",
#             "name": "חד פאזי 40 אמפר (1X40)"
#         } //...
#     ]
# }


@dataclass
class OrderPurpose(DataClassDictMixin):
    """
    Represents the purpose of an order related to building types.

    Attributes:
        desc (str): A description of the order purpose.
        building_type (int): The type of building associated with the order.
        id (UUID): The unique identifier for the order purpose.
        name (str): The name of the order purpose.
    """

    desc: str = field(metadata=field_options(alias="desc"))
    building_type: int = field(metadata=field_options(alias="buildingType"))
    id: UUID = field(metadata=field_options(alias="id"))
    name: str = field(metadata=field_options(alias="name"))


@dataclass
class ConnectionSize(DataClassDictMixin):
    """
    Represents a connection size option.

    Attributes:
        id (UUID): The unique identifier for the connection size.
        name (str): The name of the connection size, typically including phase and amperage details.
    """

    id: UUID = field(metadata=field_options(alias="id"))
    name: str = field(metadata=field_options(alias="name"))


@dataclass
class ResidenceOption(DataClassDictMixin):
    """
    Represents a residential option, including order purpose and available connection sizes.

    Attributes:
        order_purpose (OrderPurpose): The purpose of the order for a residential option.
        connection_sizes (List[ConnectionSize]): A list of connection sizes available for this residential option.
    """

    order_purpose: OrderPurpose = field(metadata=field_options(alias="orderPurpose"))
    connection_sizes: List[ConnectionSize] = field(metadata=field_options(alias="connectionSizes"))


@dataclass
class CommercialOption(DataClassDictMixin):
    """
    Represents a commercial option, including order purpose and available connection sizes.

    Attributes:
        order_purpose (OrderPurpose): The purpose of the order for a commercial option.
        connection_sizes (List[ConnectionSize]): A list of connection sizes available for this commercial option.
    """

    order_purpose: OrderPurpose = field(metadata=field_options(alias="orderPurpose"))
    connection_sizes: List[ConnectionSize] = field(metadata=field_options(alias="connectionSizes"))


@dataclass
class TempOption(DataClassDictMixin):
    """
    Represents a temporary option, including order purpose and available connection sizes.

    Attributes:
        order_purpose (OrderPurpose): The purpose of the order for a temporary option.
        connection_sizes (List[ConnectionSize]): A list of connection sizes available for this temporary option.
    """

    order_purpose: OrderPurpose = field(metadata=field_options(alias="orderPurpose"))
    connection_sizes: List[ConnectionSize] = field(metadata=field_options(alias="connectionSizes"))


@dataclass
class OptionSizeType(DataClassDictMixin):
    """
    Represents a size type option for various building categories.

    Attributes:
        id (UUID): The unique identifier for the size type.
        name (str): The name of the size type, typically including phase and amperage details.
    """

    id: UUID = field(metadata=field_options(alias="id"))
    name: str = field(metadata=field_options(alias="name"))


@dataclass
class GetBuildingOptionsResponse(DataClassDictMixin):
    """
    Represents the overall response structure containing various options for residential, commercial,
    and temporary connections.

    Attributes:
        residence_options (List[ResidenceOption]): A list of residential options available.
        commercial_options (List[CommercialOption]): A list of commercial options available.
        temp_options (List[TempOption]): A list of temporary options available.
        residence_size_types (List[OptionSizeType]): A list of size types available for residential buildings.
        commercial_size_types (List[OptionSizeType]): A list of size types available for commercial buildings.
        public_size_types (List[OptionSizeType]): A list of size types available for public buildings.
        parking_size_types (List[OptionSizeType]): A list of size types available for parking facilities.
    """

    residence_options: List[ResidenceOption] = field(metadata=field_options(alias="residenceOptions"))
    commercial_options: List[CommercialOption] = field(metadata=field_options(alias="commercialOptions"))
    temp_options: List[TempOption] = field(metadata=field_options(alias="tempOptions"))
    residence_size_types: List[OptionSizeType] = field(metadata=field_options(alias="residenceSizeTypes"))
    commercial_size_types: List[OptionSizeType] = field(metadata=field_options(alias="commercialSizeTypes"))
    public_size_types: List[OptionSizeType] = field(metadata=field_options(alias="publicSizeTypes"))
    parking_size_types: List[OptionSizeType] = field(metadata=field_options(alias="parkingSizeTypes"))
