""" Meter Reading model. """
from dataclasses import dataclass, field
from datetime import datetime

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder

from iec_api.commons import convert_to_tz_aware_datetime
from iec_api.models.response_descriptor import ResponseWithDescriptor

# GET https://iecapi.iec.co.il//api/Device/LastMeterReading/{contract_id}/{bp_number}
#
# # {
#     "data": {
#         "contractAccount": "12345", // = contract_id
#         "lastMeters": [
#             {
#                 "meterReadings": [
#                     {
#                         "reading": 1234,
#                         "readingCode": "01",
#                         "readingDate": "2024-01-17T00:00:00",
#                         "usage": "111",
#                         "serialNumber": null
#                     }
#                 ],
#                 "serialNumber": "000000000000000001",
#                 "materialNumber": "000000000000000001",
#                 "registerNumber": "000000000000000001"
#             }
#         ]
#     },
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "00",
#         "description": ""
#     }
# }


@dataclass
class MeterReading(DataClassDictMixin):
    """Meter Reading dataclass."""

    reading: int = field(metadata=field_options(alias="reading"))
    reading_code: str = field(metadata=field_options(alias="readingCode"))
    reading_date: datetime = field(metadata=field_options(alias="readingDate"))
    usage: str
    serial_number: str = field(metadata=field_options(alias="serialNumber"))

    @classmethod
    def __post_deserialize__(cls, obj: "MeterReading") -> "MeterReading":
        obj.reading_date = convert_to_tz_aware_datetime(obj.reading_date)
        return obj


@dataclass
class LastMeter(DataClassDictMixin):
    """Last Meters"""

    meter_readings: list[MeterReading] = field(metadata=field_options(alias="meterReadings"))
    serial_number: str = field(metadata=field_options(alias="serialNumber"))
    material_number: str = field(metadata=field_options(alias="materialNumber"))
    register_number: str = field(metadata=field_options(alias="registerNumber"))


@dataclass
class MeterReadings(DataClassDictMixin):
    """Meter Readings dataclass."""

    contract_account: str = field(metadata=field_options(alias="contractAccount"))
    last_meters: list[LastMeter] = field(metadata=field_options(alias="lastMeters"))


decoder = BasicDecoder(ResponseWithDescriptor[MeterReadings])
