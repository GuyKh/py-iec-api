from dataclasses import dataclass, field
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options


@dataclass
class IDWrapper(DataClassDictMixin):
    """Represents {"id": "<uuid>"} structures used by MASA endpoints."""

    id: UUID = field(metadata=field_options(alias="id"))
