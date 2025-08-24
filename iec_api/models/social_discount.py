from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from mashumaro import DataClassDictMixin, field_options

# GET https://iecapi.iec.co.il/api/SocialDiscount/{{bp_number}}
#
# {
#    "discountExists": false,
#    "discountStatusCode": 99,
#    "contractNumber": "00123456",
#    "discountStartDate": "0001-01-01T00:00:00",
#    "discountEndDate": "0001-01-01T00:00:00"
# }
#


@dataclass
class SocialDiscount(DataClassDictMixin):
    """
    Represents the social discount information for a user.

    Attributes:
        discount_exists (bool): Indicates if a social discount exists.
        discount_status_code (int): The status code of the discount.
        contract_number (str): The Contract Number
        discount_start_date (datetime): The start date of the discount.
        discount_end_date (datetime): The end date of the discount.
    """

    discount_exists: bool = field(metadata=field_options(alias="discountExists"))
    discount_status_code: int = field(metadata=field_options(alias="discountStatusCode"))
    contract_number: Optional[str] = field(metadata=field_options(alias="contractNumber"), default=None)
    discount_start_date: datetime = field(metadata=field_options(alias="discountStartDate"))
    discount_end_date: datetime = field(metadata=field_options(alias="discountEndDate"))
