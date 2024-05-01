import logging
from datetime import timedelta
from decimal import Decimal
from typing import Optional

from aiohttp import ClientSession

from iec_api import commons
from iec_api.const import GET_CALCULATOR_GADGET_URL
from iec_api.usage_calculator.consumption import Consumption
from iec_api.usage_calculator.electric_device import ElectricDevice, PowerUnit
from iec_api.usage_calculator.get_calculator_response import GetCalculatorResponse
from iec_api.usage_calculator.rates import Rates

logger = logging.getLogger(__name__)


class UsageCalculator:
    """Usage Calculator"""

    def __init__(self):
        self.devices: list[ElectricDevice] = []
        self.rates: Rates | None = None
        self.is_loaded = False

    async def load_data(self, session: ClientSession):
        if not self.is_loaded:
            iec_api_data = await commons.send_get_request(session=session, url=GET_CALCULATOR_GADGET_URL)
            response = GetCalculatorResponse.from_dict(iec_api_data)
            self.devices: list[ElectricDevice] = response.electric_devices
            self.rates: Rates | None = response.gadget_calculator_rates
            self.is_loaded = True
        else:
            logger.info("Usage calculator data was already loaded")

    def get_kwh_tariff(self) -> float:
        if not self.is_loaded:
            raise ValueError("Usage calculator data is not loaded")
        return float(self.rates.home_rate * (1 + self.rates.vat / 100))

    def get_device_names(self) -> list[str]:
        if not self.is_loaded:
            raise ValueError("Usage calculator data is not loaded")
        return list(map(lambda device: device.name, self.devices))

    def get_device_info_by_name(self, name: str) -> Optional[ElectricDevice]:
        if not self.is_loaded:
            raise ValueError("Usage calculator data is not loaded")
        for device in self.devices:
            if device.name == name:
                return device
        return None

    def get_consumption_by_device_and_time(
        self, name: str, time_delta: timedelta, custom_usage_value: Optional[float]
    ) -> Optional[Consumption]:
        device = self.get_device_info_by_name(name)
        if not device:
            return None

        minutes = time_delta.total_seconds() / 60

        consumption = self._convert_to_kwh(device, custom_usage_value)
        rate = float(self.rates.home_rate * (1 + self.rates.vat / 100))

        return Consumption(
            name=name,
            power=custom_usage_value if custom_usage_value else device.power,
            power_unit=device.power_unit,
            consumption=consumption,
            cost=Decimal.from_float(consumption) * rate,
            duration=timedelta(minutes=minutes),
        )

    @staticmethod
    def _convert_to_kwh(device: ElectricDevice, custom_usage_value: Optional[float] = None) -> float:
        # From IEC Logic

        power = custom_usage_value if custom_usage_value else device.power

        match device.power_unit:
            case PowerUnit.KiloWatt:
                return power
            case PowerUnit.Watt:
                return power * 0.001
            case PowerUnit.HorsePower:
                return power * 0.736
            case PowerUnit.Ampere:
                return power * 0.23
