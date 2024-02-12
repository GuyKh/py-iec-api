""" Main IEC Python API module. """

from logging import getLogger
from logging.config import fileConfig as logConfig
from src.const import HEADERS_WITH_AUTH
from src.data import get_consumer

from src.login import IECLoginError

logConfig("./logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)

if __name__ == "__main__":  # pragma: no cover
    try:
        # token = get_authorization_token()
        token = input("Input bearer token:")
        print(f"Token: {token}")
        HEADERS_WITH_AUTH["Authorization"] = "Bearer " + token
        print(HEADERS_WITH_AUTH)

        consumer = get_consumer()
        print(f"Consumer: {consumer}")

    except IECLoginError as err:
        logger.error("Failed Login: (Code %d): %s", err.code, err.error)
