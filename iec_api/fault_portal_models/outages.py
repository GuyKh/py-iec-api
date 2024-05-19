# Outages model

# GET https://masa-faultsportalapi.iec.co.il/api/accounts/{account_id}}/tranzactions/2
#
# {
#   "dataCollection":
#       [
#       ]
#   }
# }


from dataclasses import dataclass, field
from typing import List, Optional

from mashumaro import DataClassDictMixin, field_options


@dataclass
class FaultPortalOutage(DataClassDictMixin):
    """Outage Model"""


@dataclass
class OutagesResponse(DataClassDictMixin):
    data_collection: Optional[List[FaultPortalOutage]] = field(metadata=field_options(alias="dataCollection"))
