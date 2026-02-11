# Accounts Transactions Model

from dataclasses import dataclass, field
from typing import List

from mashumaro import DataClassDictMixin, field_options

# POST https://masa-faultsportalapi.iec.co.il/api/accounts/tranzactions
#
# Request:
# {
#  "Accounts": [
#    "00000000-0000-0000-0000-000000000001",
#    "00000000-0000-0000-0000-000000000002"
#  ],
#  "StateCode": 0
# }
#
# Response:
# {
#  "consumptionOrderViewTypeCode": 1,
#  "logicalName": "account"
# }


@dataclass
class AccountsTransactionsRequest(DataClassDictMixin):
    """Request model for accounts transactions endpoint.

    Attributes:
        accounts: List of account UUIDs to query.
        state_code: The state code filter.
    """

    accounts: List[str] = field(metadata=field_options(alias="Accounts"))
    state_code: int = field(metadata=field_options(alias="StateCode"))


@dataclass
class AccountsTransactionsResponse(DataClassDictMixin):
    """Response model for accounts transactions endpoint.

    Attributes:
        consumption_order_view_type_code: The consumption order view type code.
        logical_name: The logical name of the entity.
    """

    consumption_order_view_type_code: int = field(metadata=field_options(alias="consumptionOrderViewTypeCode"))
    logical_name: str = field(metadata=field_options(alias="logicalName"))
