from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options
from mashumaro.config import BaseConfig

# POST https://iecapi.iec.co.il/api/Consumption/SendConsumptionReportToMail/{{contract_id}}
# {
#     "emailAddress": "sefi.ninio@gmail.com",
#     "meterCode": "{{device_code}}",
#     "meterSerial": "{{device_id}}"
# }
#
#
# True
#


@dataclass
class SendConsumptionReportToMailRequest(DataClassDictMixin):
    """
    Send Consumption Report To Mail Request dataclass.
    """

    email_address: str = field(metadata=field_options(alias="emailAddress"))
    meter_code: str = field(metadata=field_options(alias="meterCode"))
    meter_serial: str = field(metadata=field_options(alias="meterSerial"))

    class Config(BaseConfig):
        serialize_by_alias = True
