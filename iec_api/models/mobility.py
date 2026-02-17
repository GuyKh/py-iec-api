"""Models for IEC mobility endpoint."""

from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

# GET https://iecapi.iec.co.il/api/Mobility/{contract_id}/{device_id}
#
# Response:
# {
#   "data": {
#     "isMobilityRequestExist": false,
#     "isMobilityInRange": false
#   },
#   "reponseDescriptor": {
#     "isSuccess": true,
#     "code": "00",
#     "description": ""
#   }
# }


@dataclass
class MobilityStatus(DataClassDictMixin):
    """Mobility eligibility and request status."""

    is_mobility_request_exist: bool = field(metadata=field_options(alias="isMobilityRequestExist"))
    is_mobility_in_range: bool = field(metadata=field_options(alias="isMobilityInRange"))


decoder = BasicDecoder(ResponseWithDescriptor[MobilityStatus])
