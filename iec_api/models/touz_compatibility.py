from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options

# TOU = Time-Of-Use
#
# GET https://iecapi.iec.co.il/api/calculator/touz/{contract_id}/{bp_number}/compatible
#
# Return format is:
# {
#     "status": 2,
#     "isCompatible": false
# }


@dataclass
class TouzCompatibility(DataClassDictMixin):
    """
    Represents the TOU (Time of Use) tariff compatibility information.
    """

    status: int = field(metadata=field_options(alias="status"))
    is_compatible: bool = field(metadata=field_options(alias="isCompatible"))
