from dataclasses import dataclass, field
from datetime import datetime

from mashumaro import DataClassDictMixin, field_options
from mashumaro.codecs import BasicDecoder
from mashumaro.config import BaseConfig

from iec_api.models.response_descriptor import ResponseWithDescriptor

#   EFS stands for EFS service (Email, Fax, SMS) Messages
#
#   POST https://iecapi.iec.co.il//api/customer/efs
#   BODY {
#       "contractNumber":"123456",
#       "processType":1,
#       "serviceCode": "EFS004" <- optional
#   }
#
#   Response:
#
# {
#     "data": [
#         {
#             "serviceDescription": "הודעה על הפסקה מתוכננת",
#             "partner": "123456",
#             "contractNumber": "123456",
#             "service": "EFS004",
#             "subscribeDate": "2023-06-30T00:00:00",
#             "subscribeTime": "0001-01-01T13:00:01",
#             "isActive": true,
#             "bpSubscription": false,
#             "isSms": false,
#             "communicationMethod": 1,
#             "email": "",
#             "sms": "055555555",
#             "fax": "0000000000",
#             "unsubscribeDate": "0001-01-01T00:00:00",
#             "registrationStatus": 0
#         }
#     ],
#     "reponseDescriptor": {
#         "isSuccess": true,
#         "code": "300",
#         "description": ""
#     }
# }


@dataclass
class EfsRequestAllServices(DataClassDictMixin):
    contract_number: str = field(metadata=field_options(alias="contractNumber"))
    process_type: int = field(metadata=field_options(alias="processType"))

    class Config(BaseConfig):
        serialize_by_alias = True


@dataclass
class EfsRequestSingleService(EfsRequestAllServices):
    service_code: str = field(metadata=field_options(alias="serviceCode"))


@dataclass
class EfsMessage(DataClassDictMixin):
    service_description: str = field(metadata=field_options(alias="serviceDescription"))
    partner: str = field(metadata=field_options(alias="partner"))
    contract_number: str = field(metadata=field_options(alias="contractNumber"))
    service: str = field(metadata=field_options(alias="service"))
    subscribe_date: datetime = field(metadata=field_options(alias="subscribeDate"))
    subscribe_time: datetime = field(metadata=field_options(alias="subscribeTime"))
    is_active: bool = field(metadata=field_options(alias="isActive"))
    bp_subscription: bool = field(metadata=field_options(alias="bpSubscription"))
    is_sms: bool = field(metadata=field_options(alias="isSms"))
    communication_method: int = field(metadata=field_options(alias="communicationMethod"))
    email: str = field(metadata=field_options(alias="email"))
    sms: str = field(metadata=field_options(alias="sms"))
    fax: str = field(metadata=field_options(alias="fax"))
    unsubscribe_date: datetime = field(metadata=field_options(alias="unsubscribeDate"))
    registration_status: int = field(metadata=field_options(alias="registrationStatus"))


decoder = BasicDecoder(ResponseWithDescriptor[list[EfsMessage]])
