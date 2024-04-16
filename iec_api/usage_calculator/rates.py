from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from mashumaro import DataClassDictMixin, field_options


@dataclass
class Rates(DataClassDictMixin):
    """Calculator Rates dataclass."""

    last_updated: datetime = field(metadata=field_options(alias="lastUpdated"))
    home_rate: Decimal = field(metadata=field_options(alias="homeRate"))
    general_rate: Decimal = field(metadata=field_options(alias="generalRate"))
    vat: Decimal = field(metadata=field_options(alias="vat"))
