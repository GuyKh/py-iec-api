""" Meter Reading model. """

from dataclasses import dataclass, field
from mashumaro import DataClassDictMixin, field_options
from response_descriptor import ResponseDescriptor


@dataclass
class MeterReading(DataClassDictMixin):
    """ Meter Reading dataclass."""
    reading: int
    reading_code: str = field(metadata=field_options(alias="readingCode"))
    reading_date: str = field(metadata=field_options(alias="readingDate"))
    usage: str
    serial_number: str = field(metadata=field_options(alias="serialNumber"))


@dataclass
class MeterReadings(DataClassDictMixin):
    """ Meter Readings dataclass."""
    contract_account: str = field(metadata=field_options(alias="contractAccount"))
    last_meters: list[MeterReading] = field(metadata=field_options(alias="lastMeters"))
    serial_number: str = field(metadata=field_options(alias="serialNumber"))
    material_number: str = field(metadata=field_options(alias="materialNumber"))
    register_number: str = field(metadata=field_options(alias="registerNumber"))


@dataclass
class GetLastMeterReadingResponse(DataClassDictMixin):
    """ Get Last Meter Reading Response dataclass."""
    data: MeterReadings
    response_descriptor: ResponseDescriptor
