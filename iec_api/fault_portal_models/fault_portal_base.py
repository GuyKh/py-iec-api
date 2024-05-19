from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from mashumaro import DataClassDictMixin, field_options


@dataclass
class FaultPortalBase(DataClassDictMixin):
    """Base Class for Fault Portal Address"""

    id: Optional[UUID] = field(metadata=field_options(alias="id"))
    logical_name: Optional[str] = field(metadata=field_options(alias="logicalName"))
