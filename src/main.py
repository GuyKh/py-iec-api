from logging import getLogger
from logging.config import fileConfig as logConfig

logConfig("./logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)


def hello() -> str:
    logger.info("Hello")
    return "Hello"


if __name__ == "__main__":  # pragma: no cover
    print(hello())
