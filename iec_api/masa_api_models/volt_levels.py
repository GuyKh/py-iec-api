from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masaapi-wa.azurewebsites.net/api/voltLevels/active
#
# {
#     "dataCollection": [
#         {
#             "name": "12.6",
#             "minVoltLevel": 29,
#             "maxVoltLevel": 400,
#             "id": "1b7d1650-4eb1-ed11-9885-000d3a2e4333"
#         },
#         {
#             "name": "22",
#             "minVoltLevel": 17,
#             "maxVoltLevel": 400,
#             "id": "1d7d1650-4eb1-ed11-9885-000d3a2e4333"
#         },
#         {
#             "name": "33",
#             "minVoltLevel": 11,
#             "maxVoltLevel": 400,
#             "id": "1f7d1650-4eb1-ed11-9885-000d3a2e4333"
#         }
#     ]
# }


@dataclass
class VoltLevel(DataClassDictMixin):
    """
    Represents a voltage level.

    Attributes:
        name (str): The name or label of the voltage level.
        min_volt_level (int): The minimum voltage level.
        max_volt_level (int): The maximum voltage level.
        id (UUID): The unique identifier for the voltage level.
    """

    name: str = field(metadata=field_options(alias="name"))
    min_volt_level: int = field(metadata=field_options(alias="minVoltLevel"))
    max_volt_level: int = field(metadata=field_options(alias="maxVoltLevel"))
    id: UUID = field(metadata=field_options(alias="id"))


@dataclass
class VoltLevelsResponse(DataClassDictMixin):
    """
    Represents the response containing a list of voltage levels.

    Attributes:
        data_collection (List[VoltLevel]): A list of voltage levels.
    """

    data_collection: List[VoltLevel] = field(metadata=field_options(alias="dataCollection"))
