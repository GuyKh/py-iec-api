from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options

from iec_api.usage_calculator.electric_device import ElectricDevice
from iec_api.usage_calculator.rates import Rates


@dataclass
class GetCalculatorResponse(DataClassDictMixin):
    """Calculator Rates dataclass."""

    gadget_calculator_rates: Rates = field(metadata=field_options(alias="gadget_Calculator_Rates"))
    electric_devices: list[ElectricDevice] = field(metadata=field_options(alias="electric_Devices"))
