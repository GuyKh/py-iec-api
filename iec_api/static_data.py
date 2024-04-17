from aiohttp import ClientSession

from iec_api.usage_calculator.calculator import UsageCalculator

usage_calculator = UsageCalculator()


async def get_usage_calculator(session: ClientSession) -> UsageCalculator:
    """Get Usage Calculator from IEC API data."""

    if not usage_calculator.is_loaded:
        await usage_calculator.load_data(session)

    return usage_calculator


async def get_kwh_tariff(session: ClientSession) -> float:
    calculator = await get_usage_calculator(session)
    return calculator.get_kwh_tariff()
