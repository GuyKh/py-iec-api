""" Login Requests Model. """
from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options


@dataclass
class LoginResponse(DataClassDictMixin):
    """Login Response dataclass."""

    phone_number: str = field(metadata=field_options(alias="phoneNumber"))
    phone_prefix: str = field(metadata=field_options(alias="phonePrefix"))
    phone_suffix: str = field(metadata=field_options(alias="phoneSuffix"))
    href: str
    state_token: str = field(metadata=field_options(alias="stateToken"))
    first_name: str = field(metadata=field_options(alias="firstName"))
    user_status: int = field(metadata=field_options(alias="userStatus"))
    multi_factor_type: int = field(metadata=field_options(alias="multiFactorType"))


@dataclass
class ValidateSMSResponse(DataClassDictMixin):
    """Validate SMS Response dataclass."""

    token: str


@dataclass
class OTPRequest:
    """OTP Validation Request dataclass."""

    href: str
    token: str
    code: str


@dataclass
class OTPResponse(DataClassDictMixin):
    """OTP Validation Response dataclass."""

    href: str
    token: str
    code: str
