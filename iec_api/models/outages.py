""" Outages model. """
from dataclasses import dataclass

from mashumaro import DataClassDictMixin
from mashumaro.codecs import BasicDecoder

from iec_api.models.response_descriptor import ResponseWithDescriptor

# GET https://iecapi.iec.co.il//api/outages/transactions/{account_id}/2
#
# # {
#     "data": []
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "00",
#         "description": ""
#     }
# }

# GET https://masa-faultsportalapi.iec.co.il/api/accounts/{{account_id}}/tranzactions/2
#
# # {
#     "dataCollection": []
# }


@dataclass
class Outage(DataClassDictMixin):
    """Outage dataclass."""


decoder = BasicDecoder(ResponseWithDescriptor[Outage])
