from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masa-mainportalapi.iec.co.il/api/cities
#
# {
#     "dataCollection": [
#         {
#             "area": {
#                 "name": "עמקים",
#                 "shovalAreaCode": 702,
#                 "id": "15414b54-d8db-ea11-a813-000d3aabca53",
#                 "logicalName": "iec_area"
#             },
#             "region": {
#                 "name": "חיפה והצפון",
#                 "shovalRegionCode": 7,
#                 "id": "909a5d57-d7db-ea11-a813-000d3aabca53",
#                 "logicalName": "iec_region"
#             },
#             "name": "אלון תבור",
#             "shovalCityCode": "2054",
#             "id": "34698a40-28ec-ea11-a817-000d3a239ca0",
#             "logicalName": "iec_city"
#         } // ...
#     ]
# }


@dataclass
class Area(DataClassDictMixin):
    """
    Represents an area within a region.

    Attributes:
        name (str): The name of the area.
        shoval_area_code (int): The Shoval area code.
        id (UUID): The unique identifier for the area.
        logical_name (str): The logical name of the area entity.
    """

    name: str = field(metadata=field_options(alias="name"))
    shoval_area_code: int = field(metadata=field_options(alias="shovalAreaCode"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class Region(DataClassDictMixin):
    """
    Represents a region.

    Attributes:
        name (str): The name of the region.
        shoval_region_code (int): The Shoval region code.
        id (UUID): The unique identifier for the region.
        logical_name (str): The logical name of the region entity.
    """

    name: str = field(metadata=field_options(alias="name"))
    shoval_region_code: int = field(metadata=field_options(alias="shovalRegionCode"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class City(DataClassDictMixin):
    """
    Represents a city within a region and area.

    Attributes:
        area (Area): The area to which the city belongs.
        region (Region): The region to which the city belongs.
        name (str): The name of the city.
        shoval_city_code (str): The Shoval city code.
        id (UUID): The unique identifier for the city.
        logical_name (str): The logical name of the city entity.
    """

    area: Area = field(metadata=field_options(alias="area"))
    region: Region = field(metadata=field_options(alias="region"))
    name: str = field(metadata=field_options(alias="name"))
    shoval_city_code: str = field(metadata=field_options(alias="shovalCityCode"))
    id: UUID = field(metadata=field_options(alias="id"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))


@dataclass
class CitiesResponse(DataClassDictMixin):
    """
    Represents the response containing a list of cities.

    Attributes:
        data_collection (List[City]): A list of cities.
    """

    data_collection: List[City] = field(metadata=field_options(alias="dataCollection"))
