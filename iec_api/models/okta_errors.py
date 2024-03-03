from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options


@dataclass
class OktaErrorCause(DataClassDictMixin):
    error_summary: str = field(metadata=field_options(alias="errorSummary"))


@dataclass
class OktaError(DataClassDictMixin):
    error_code: str = field(metadata=field_options(alias="errorCode"))
    error_summary: str = field(metadata=field_options(alias="errorSummary"))
    error_link: str = field(metadata=field_options(alias="errorLink"))
    error_id: str = field(metadata=field_options(alias="errorId"))
    error_causes: list[OktaErrorCause] = field(metadata=field_options(alias="errorCauses"))
