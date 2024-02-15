from dataclasses import dataclass

from mashumaro import DataClassDictMixin


@dataclass
class JWT(DataClassDictMixin):
    """ Okta JWT Token """
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: str
