from dataclasses import dataclass, field
from enum import IntEnum

from mashumaro import DataClassDictMixin, field_options


class CalculationResolution(IntEnum):
    """Calculation Resolution enum."""

    MINUTE = 1
    HOUR = 2


class PowerUnit(IntEnum):
    """Power Unit enum."""

    KiloWatt = 1
    Watt = 2
    HorsePower = 3
    Ampere = 4


@dataclass
class ElectricDevice(DataClassDictMixin):
    """Electric Device dataclass."""

    name: str = field(metadata=field_options(alias="name"))
    calculation_resolution: CalculationResolution = field(metadata=field_options(alias="calculationResolution"))
    power: int = field(metadata=field_options(alias="power"))
    power_unit: PowerUnit = field(metadata=field_options(alias="powerUnit"))
    average_duration_time_of_operation_in_minutes: float = field(
        metadata=field_options(alias="avarageDurationTimeOfOperationInMinutes")
    )
