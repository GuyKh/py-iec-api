from dataclasses import dataclass, field
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options
from mashumaro.config import BaseConfig

from iec_api.masa_api_models.masa_types import IDWrapper

# POST https://masa-mainportalapi.iec.co.il/api/connectionbetweencontactandcontract/remove
#
# Request:
# {
#   "Id": "00000000-0000-0000-0000-000000000005",
#   "contact": {
#     "id": "00000000-0000-0000-0000-000000000006"
#   },
#   "contract": {
#     "id": "00000000-0000-0000-0000-000000000002"
#   },
#   "primaryContact": {
#     "id": "00000000-0000-0000-0000-000000000001"
#   }
# }
#
# Response (HTTP 201):
# null


@dataclass
class RemoveContactFromSharedAccountRequest(DataClassDictMixin):
    id: UUID = field(metadata=field_options(alias="Id"))
    contact: IDWrapper = field(metadata=field_options(alias="contact"))
    contract: IDWrapper = field(metadata=field_options(alias="contract"))
    primary_contact: IDWrapper = field(metadata=field_options(alias="primaryContact"))

    class Config(BaseConfig):
        serialize_by_alias = True
