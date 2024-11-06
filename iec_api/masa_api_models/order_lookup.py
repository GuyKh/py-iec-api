from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masaapi-wa.azurewebsites.net/api/orderLookup
#
# {
#     "orderCategories": [
#         {
#             "name": "הגדלת חיבור ממתח נמוך למתח גבוה",
#             "typeCodeInt": 1,
#             "id": "234b41b5-61c4-ee11-907a-000d3a2e4333"
#         } //...
#     ]
# }


@dataclass
class OrderCategory(DataClassDictMixin):
    """
    Represents a category of an order.

    Attributes:
        name (str): The name of the order category.
        type_code_int (int): The type code associated with the order category.
        id (UUID): The unique identifier for the order category.
    """

    name: str = field(metadata=field_options(alias="name"))
    type_code_int: int = field(metadata=field_options(alias="typeCodeInt"))
    id: UUID = field(metadata=field_options(alias="id"))


@dataclass
class OrderLookupResponse(DataClassDictMixin):
    """
    Represents the response containing a list of order categories.

    Attributes:
        order_categories (List[OrderCategory]): A list of order categories.
    """

    order_categories: List[OrderCategory] = field(metadata=field_options(alias="orderCategories"))
