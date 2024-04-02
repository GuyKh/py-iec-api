""" Error response object """
from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options

# GET https://iecapi.iec.co.il//api/Device/123456
# {"Error": "Contract is not associated with you.", "Code": 401, "Rid": "800017a7-0003-f300-b63f-84710c7967bb"}


@dataclass
class IecErrorResponse(DataClassDictMixin):
    error: str = field(metadata=field_options(alias="Error"))
    code: int = field(metadata=field_options(alias="Code"))
    rid: str = field(metadata=field_options(alias="Rid"))
