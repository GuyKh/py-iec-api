from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

from iec_api.usage_calculator.electric_device import PowerUnit


@dataclass
class Consumption:
    """Consumption dataclass."""

    name: str
    power: float
    power_unit: PowerUnit
    duration: timedelta
    consumption: float
    cost: Decimal
