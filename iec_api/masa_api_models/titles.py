from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options

# GET https://masaapi-wa.azurewebsites.net/api/accounts/{account_id}/orders/titles

#
# {"orders":[],"id":"ebee08af-9972-e811-8106-3863bb358f68"}


@dataclass
class Order(DataClassDictMixin):
    """
    Represents an order.

    Attributes:
        ?
    """


@dataclass
class GetTitleResponse(DataClassDictMixin):
    """
    Represents a title response

    Attributes:
        id (UUID): id
        orders (List[Order]) : list of orders
    """

    id: UUID = field(metadata=field_options(alias="id"))
    orders: List[Order] = field(metadata=field_options(alias="orders"))
