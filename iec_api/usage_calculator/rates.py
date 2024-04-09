from dataclasses import dataclass, field
from datetime import datetime

from mashumaro import DataClassDictMixin, field_options


@dataclass
class Rates(DataClassDictMixin):
    """Calculator Rates dataclass."""

    last_updated: datetime = field(metadata=field_options(alias="lastUpdated"))
    home_rate: float = field(metadata=field_options(alias="homeRate"))
    general_rate: float = field(metadata=field_options(alias="generalRate"))
    vat: float = field(metadata=field_options(alias="vat"))
