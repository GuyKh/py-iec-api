from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masaapi-wa.azurewebsites.net/equipments/get?accountId={account_id}&pageNumber=1&pageSize=10

# {
#     {
#     "pageSize": 10,
#     "pageNumber": 1,
#     "moreRecords": false,
#     "totalRecords": 1,
#     "pageCookie": 0,
#     "items": [
#         {
#             "accountId": "b67ea524-300f-4a85-9ef4-54d30a753452",
#             "accountType": 279830001,
#             "accountName": "זינגר מיטל",
#             "addressId": "b67ea524-300f-4a85-9ef4-54d30a753452",
#             "areaId": "b67ea524-300f-4a85-9ef4-54d30a753452",
#             "regionId": "b67ea524-300f-4a85-9ef4-54d30a753452",
#             "fullAddress": "פרישמן 47  ,תל אביב - יפו, קומה ב",
#             "siteId": "b67ea524-300f-4a85-9ef4-54d30a753452",
#             "iec_ContractNumber": "346669815",
#             "siteType": 18,
#             "activeConnections": 1,
#             "connections": [
#                 {
#                     "connectionId": "b67ea524-300f-4a85-9ef4-54d30a753452",
#                     "connectionNumber": "12345",
#                     "hasOpenOrders": false,
#                     "shovalOpenOrder": null,
#                     "powerConnectionSize": 279830006,
#                     "isLowVolte": true,
#                     "isCanIncrease": false,
#                     "meterId": "b67ea524-300f-4a85-9ef4-54d30a753452",
#                     "meterNumber": "1234",
#                     "voltType": 279830001,
#                     "currentReader": "17.32",
#                     "currentAmpere": null,
#                     "currentVoltLevel": {
#                         "id": null,
#                         "name": null
#                     }
#                 }
#             ],
#             "possible2ShiftBit": false,
#             "building": {
#                 "id": "b67ea524-300f-4a85-9ef4-54d30a753452",
#                 "name": "700045035",
#                 "hasSAOrders": null,
#                 "shovalSAOrder": null,
#                 "multiResidentialBuilding": true,
#                 "isMaxPublicSitesSum": false,
#                 "isResidentialBuilding": false,
#                 "numOfRelatedSitesInt": 9
#             },
#             "backuplineOrder": null,
#             "hasBackuplineOrders": false
#         }
#     ]
# }
# }


@dataclass
class VoltLevel(DataClassDictMixin):
    """
    Represents the voltage level details of a connection.

    Attributes:
        id (Optional[str]): The ID of the voltage level.
        name (Optional[str]): The name of the voltage level.
    """

    id: Optional[str] = field(metadata=field_options(alias="id"))
    name: Optional[str] = field(metadata=field_options(alias="name"))


@dataclass
class Connection(DataClassDictMixin):
    """
    Represents a connection within an account item.

    Attributes:
        connection_id (UUID): The ID of the connection.
        connection_number (str): The number of the connection.
        has_open_orders (bool): Whether the connection has open orders.
        shoval_open_order (Optional[str]): The open order associated with the connection.
        power_connection_size (int): The size of the power connection.
        is_low_volte (bool): Indicates if the connection is low voltage.
        is_can_increase (bool): Indicates if the power connection size can be increased.
        meter_id (UUID): The ID of the meter associated with the connection.
        meter_number (str): The number of the meter.
        volt_type (int): The type of voltage.
        current_reader (str): The current reading of the connection.
        current_ampere (Optional[str]): The current ampere value.
        current_volt_level (VoltLevel): The voltage level details of the connection.
    """

    connection_id: UUID = field(metadata=field_options(alias="connectionId"))
    connection_number: str = field(metadata=field_options(alias="connectionNumber"))
    has_open_orders: bool = field(metadata=field_options(alias="hasOpenOrders"))
    shoval_open_order: Optional[str] = field(metadata=field_options(alias="shovalOpenOrder"))
    power_connection_size: int = field(metadata=field_options(alias="powerConnectionSize"))
    is_low_volte: bool = field(metadata=field_options(alias="isLowVolte"))
    is_can_increase: bool = field(metadata=field_options(alias="isCanIncrease"))
    meter_id: UUID = field(metadata=field_options(alias="meterId"))
    meter_number: str = field(metadata=field_options(alias="meterNumber"))
    volt_type: int = field(metadata=field_options(alias="voltType"))
    current_reader: str = field(metadata=field_options(alias="currentReader"))
    current_ampere: Optional[str] = field(metadata=field_options(alias="currentAmpere"))
    current_volt_level: VoltLevel = field(metadata=field_options(alias="currentVoltLevel"))


@dataclass
class Building(DataClassDictMixin):
    """
    Represents the building details associated with an account item.

    Attributes:
        id (UUID): The ID of the building.
        name (str): The name of the building.
        has_sa_orders (Optional[str]): Indicates if there are SA orders for the building.
        shoval_sa_order (Optional[str]): The SA order associated with the building.
        multi_residential_building (bool): Indicates if the building is a multi-residential building.
        is_max_public_sites_sum (bool): Indicates if the building has reached the maximum public sites sum.
        is_residential_building (bool): Indicates if the building is residential.
        num_of_related_sites_int (int): The number of related sites within the building.
    """

    id: UUID = field(metadata=field_options(alias="id"))
    name: str = field(metadata=field_options(alias="name"))
    has_sa_orders: Optional[str] = field(metadata=field_options(alias="hasSAOrders"))
    shoval_sa_order: Optional[str] = field(metadata=field_options(alias="shovalSAOrder"))
    multi_residential_building: bool = field(metadata=field_options(alias="multiResidentialBuilding"))
    is_max_public_sites_sum: bool = field(metadata=field_options(alias="isMaxPublicSitesSum"))
    is_residential_building: bool = field(metadata=field_options(alias="isResidentialBuilding"))
    num_of_related_sites_int: int = field(metadata=field_options(alias="numOfRelatedSitesInt"))


@dataclass
class Item(DataClassDictMixin):
    """
    Represents an individual account item within the response.

    Attributes:
        account_id (UUID): The ID of the account.
        account_type (int): The type of the account.
        account_name (str): The name of the account holder.
        address_id (UUID): The ID of the address associated with the account.
        area_id (UUID): The ID of the area associated with the account.
        region_id (UUID): The ID of the region associated with the account.
        full_address (str): The full address of the account holder.
        site_id (UUID): The ID of the site associated with the account.
        iec_contract_number (str): The IEC contract number.
        site_type (int): The type of the site.
        active_connections (int): The number of active connections associated with the account.
        connections (List[Connection]): A list of connections associated with the account.
        possible_2_shift_bit (bool): Indicates if the account is eligible for possible shift bit.
        building (Building): The building details associated with the account.
        backupline_order (Optional[str]): The backupline order associated with the account.
        has_backupline_orders (bool): Indicates if the account has backupline orders.
    """

    account_id: UUID = field(metadata=field_options(alias="accountId"))
    account_type: int = field(metadata=field_options(alias="accountType"))
    account_name: str = field(metadata=field_options(alias="accountName"))
    address_id: UUID = field(metadata=field_options(alias="addressId"))
    area_id: UUID = field(metadata=field_options(alias="areaId"))
    region_id: UUID = field(metadata=field_options(alias="regionId"))
    full_address: str = field(metadata=field_options(alias="fullAddress"))
    site_id: UUID = field(metadata=field_options(alias="siteId"))
    iec_contract_number: str = field(metadata=field_options(alias="iec_ContractNumber"))
    site_type: int = field(metadata=field_options(alias="siteType"))
    active_connections: int = field(metadata=field_options(alias="activeConnections"))
    connections: List[Connection] = field(metadata=field_options(alias="connections"))
    possible_2_shift_bit: bool = field(metadata=field_options(alias="possible2ShiftBit"))
    building: Building = field(metadata=field_options(alias="building"))
    backupline_order: Optional[str] = field(metadata=field_options(alias="backuplineOrder"))
    has_backupline_orders: bool = field(metadata=field_options(alias="hasBackuplineOrders"))


@dataclass
class GetEquipmentResponse(DataClassDictMixin):
    """
    Represents the overall response structure.

    Attributes:
        page_size (int): The number of items per page.
        page_number (int): The current page number.
        more_records (bool): Indicates if there are more records available.
        total_records (int): The total number of records available.
        page_cookie (int): A cookie value for pagination.
        items (List[Item]): A list of account items included in the response.
    """

    page_size: int = field(metadata=field_options(alias="pageSize"))
    page_number: int = field(metadata=field_options(alias="pageNumber"))
    more_records: bool = field(metadata=field_options(alias="moreRecords"))
    total_records: int = field(metadata=field_options(alias="totalRecords"))
    page_cookie: int = field(metadata=field_options(alias="pageCookie"))
    items: List[Item] = field(metadata=field_options(alias="items"))
