from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options
from mashumaro.config import BaseConfig

from iec_api.masa_api_models.masa_types import IDWrapper

# POST https://masa-mainportalapi.iec.co.il/api/connectionbetweencontactandcontract/createconnectionrequest
#
# Request:
# {
#   "contact": {
#     "id": "00000000-0000-0000-0000-000000000001"
#   },
#   "contract": {
#     "id": "00000000-0000-0000-0000-000000000002"
#   }
# }
#
# Response (HTTP 201):
# "https://link.iec.co.il/ABC123SANITIZED"


@dataclass
class SendSharedAccountInvitationRequest(DataClassDictMixin):
    contact: IDWrapper = field(metadata=field_options(alias="contact"))
    contract: IDWrapper = field(metadata=field_options(alias="contract"))

    class Config(BaseConfig):
        serialize_by_alias = True
