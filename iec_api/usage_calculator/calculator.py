from datetime import timedelta
from typing import Optional

from iec_api.usage_calculator.consumption import Consumption
from iec_api.usage_calculator.electric_device import ElectricDevice, PowerUnit
from iec_api.usage_calculator.get_calculator_response import GetCalculatorResponse
from iec_api.usage_calculator.rates import Rates


class UsageCalculator:
    def __init__(self, get_response: dict):
        response = GetCalculatorResponse.from_dict(get_response)
        self.devices: list[ElectricDevice] = response.electric_devices
        self.rates: Rates = response.gadget_calculator_rates

    def get_kwh_tariff(self) -> float:
        return self.rates.home_rate * self.rates.vat

    def get_device_names(self) -> list[str]:
        return list(map(lambda device: device.name, self.devices))

    def get_device_info_by_name(self, name: str) -> Optional[ElectricDevice]:
        for device in self.devices:
            if device.name == name:
                return device
        return None

    def get_consumption_by_device_and_time(
        self, name: str, time_delta: timedelta, custom_unit: Optional[float]
    ) -> Optional[Consumption]:
        device = self.get_device_info_by_name(name)
        if not device:
            return None

        minutes = time_delta.total_seconds() / 60

        consumption = self._convert_to_kwh(device, custom_unit)
        rate = self.rates.home_rate * self.rates.vat

        return Consumption(
            name=name,
            power=custom_unit if custom_unit else device.power,
            power_unit=device.power_unit,
            consumption=consumption,
            cost=consumption * rate,
            duration=timedelta(minutes=minutes),
        )

    @staticmethod
    def _convert_to_kwh(device: ElectricDevice, custom_value: Optional[float] = None) -> float:
        # From IEC Logic

        power = custom_value if custom_value else device.power

        match device.power_unit:
            case PowerUnit.KiloWatt:
                return power
            case PowerUnit.Watt:
                return power * 0.001
            case PowerUnit.HorsePower:
                return power * 0.736
            case PowerUnit.Ampere:
                return power * 0.23
