from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options
from mashumaro.config import BaseConfig


@dataclass
class GetPdfRequest(DataClassDictMixin):
    """
    Get PDF Request dataclass.
    """

    invoice_number: str = field(metadata=field_options(alias="invoiceNumber"))
    contract_id: str = field(metadata=field_options(alias="contractId"))
    bp_number: str = field(metadata=field_options(alias="bpNumber"))

    class Config(BaseConfig):
        serialize_by_alias = True
