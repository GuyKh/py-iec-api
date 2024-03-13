""" Response Descriptor """
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

from mashumaro import DataClassDictMixin, field_options


@dataclass
class ResponseDescriptor(DataClassDictMixin):
    """Response Descriptor"""

    is_success: bool = field(metadata=field_options(alias="isSuccess"))
    code: Optional[str]
    description: Optional[str]


@dataclass
class ErrorResponseDescriptor(DataClassDictMixin):
    """Error Response Descriptor"""

    error: str = field(metadata=field_options(alias="Error"))
    code: int = field(metadata=field_options(alias="Code"))
    rid: str = field(metadata=field_options(alias="Rid"))


RESPONSE_DESCRIPTOR_FIELD = "reponseDescriptor"


T = TypeVar("T")


@dataclass
class ResponseWithDescriptor(Generic[T], DataClassDictMixin):
    """Response With Descriptor"""

    data: Optional[T]
    response_descriptor: ResponseDescriptor = field(metadata=field_options(alias=RESPONSE_DESCRIPTOR_FIELD))
