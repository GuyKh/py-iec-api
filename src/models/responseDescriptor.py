""" Response Descriptor """
from mashumaro import DataClassDictMixin, field_options
from dataclasses import dataclass, field


@dataclass
class ResponseDescriptor(DataClassDictMixin):
    """ Response Descriptor"""
    is_success: bool = field(metadata=field_options(alias="isSuccess"))
    code: str
    description: str

@dataclass
class ErrorResponseDescriptor(DataClassDictMixin):
    """ Error Response Descriptor """
    error: str = field(metadata=field_options(alias="Error"))
    code: int = field(metadata=field_options(alias="Code"))
    rid: str = field(metadata=field_options(alias="Rid"))
