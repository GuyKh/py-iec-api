import base64
from decimal import Decimal

from aiohttp import ClientSession

from iec_api import commons
from iec_api.const import GET_KWH_TARIFF_URL, GET_PREIOD_CALCULATOR_URL
from iec_api.usage_calculator.calculator import UsageCalculator

usage_calculator = UsageCalculator()
cache = {}
distribution_1p_tariff_key = "distribution_1p_tariff"
distribution_3p_tariff_key = "distribution_3p_tariff"
delivery_1p_tariff_key = "delivery_1p_tariff"
delivery_3p_tariff_key = "delivery_3p_tariff"
kwh_tariff_key = "kwh_tariff"
kva_tariff_key = "kva_tariff"
connection_to_power_size_key = "connection_to_power_size"
vat_key = "vat"


async def get_usage_calculator(session: ClientSession) -> UsageCalculator:
    """Get Usage Calculator from IEC API data."""

    if not usage_calculator.is_loaded:
        await usage_calculator.load_data(session)

    return usage_calculator


async def get_kwh_tariff(session: ClientSession) -> float:
    if kwh_tariff_key not in cache:
        calculator = await get_usage_calculator(session)
        kwh_tariff = calculator.get_kwh_tariff()
        cache[kwh_tariff_key] = kwh_tariff

    return cache[kwh_tariff_key]


async def _get_tariffs(session: ClientSession) -> tuple[float, float, float, float, float]:
    """Get Device Type data response from IEC API."""
    response = await commons.send_get_request(session=session, url=GET_KWH_TARIFF_URL)
    kwh_tariff_str = response["components"][1]["table"][1][2]["value"]
    kwh_tariff = float(base64.b64decode(kwh_tariff_str).decode("utf-8"))

    distribution_1p_tariff_str = response["components"][2]["table"][1][2]["value"]
    distribution_1p_tariff = float(base64.b64decode(distribution_1p_tariff_str).decode("utf-8"))
    distribution_3p_tariff_str = response["components"][2]["table"][2][2]["value"]
    distribution_3p_tariff = float(base64.b64decode(distribution_3p_tariff_str).decode("utf-8"))

    delivery_1p_tariff_str = response["components"][3]["table"][1][2]["value"]
    delivery_3p_tariff_str = response["components"][3]["table"][2][2]["value"]
    delivery_1p_tariff = float(base64.b64decode(delivery_1p_tariff_str).decode("utf-8"))
    delivery_3p_tariff = float(base64.b64decode(delivery_3p_tariff_str).decode("utf-8"))

    kva_tariff_str = response["components"][5]["table"][1][2]["value"]
    kva_tariff = float(base64.b64decode(kva_tariff_str).decode("utf-8"))

    cache[distribution_1p_tariff_key] = distribution_1p_tariff
    cache[distribution_3p_tariff_key] = distribution_3p_tariff
    cache[delivery_1p_tariff_key] = delivery_1p_tariff
    cache[delivery_3p_tariff_key] = delivery_3p_tariff
    cache[kva_tariff_key] = kva_tariff

    return kwh_tariff, distribution_1p_tariff, distribution_3p_tariff, delivery_1p_tariff, delivery_3p_tariff


async def get_distribution_tariff(session: ClientSession, phase_count: int) -> float:
    """Get distribution tariff (incl. VAT) from IEC API."""

    key = distribution_3p_tariff_key if phase_count == 3 else distribution_1p_tariff_key
    if key not in cache:
        await _get_tariffs(session)

    return cache[key]


async def get_delivery_tariff(session: ClientSession, phase_count: int) -> float:
    """Get delivery tariff (incl. VAT) from IEC API."""

    key = delivery_3p_tariff_key if phase_count == 3 else delivery_1p_tariff_key
    if key not in cache:
        await _get_tariffs(session)

    return cache[key]


async def get_kva_tariff(session: ClientSession) -> float:
    """Get KVA tariff (incl. VAT) from IEC API."""

    key = kva_tariff_key
    if key not in cache:
        await _get_tariffs(session)

    return cache[key]


async def _get_vat(session: ClientSession) -> Decimal:
    """Get VAT from IEC API."""

    key = vat_key
    if key not in cache:
        calculator = await get_usage_calculator(session)
        cache[key] = calculator.get_vat()

    return cache[key]


async def _get_connection_to_power_size(session: ClientSession) -> dict[str, float]:
    """Get Device Type data response from IEC API."""
    resp = await commons.send_get_request(session=session, url=GET_PREIOD_CALCULATOR_URL)
    connection_to_power_size_map = resp["period_Calculator_Rates"]["connectionToPowerSize"]

    cache[connection_to_power_size_key] = connection_to_power_size_map
    return connection_to_power_size_map


async def get_power_size(session: ClientSession, connection: str) -> float:
    """Get PowerSize by Connection (incl. VAT) from IEC API."""

    key = connection_to_power_size_key
    if key not in cache:
        await _get_connection_to_power_size(session)

    connection_to_power_size_map = cache[key]

    # If connection is not found, return 0
    power_size = connection_to_power_size_map.get(connection, 0)

    vat = await _get_vat(session)
    return round(power_size * (1 + float(vat)), 2)
