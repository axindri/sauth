import logging
import sys

from app.core.settings import settings

LOG_FORMAT = "[%(asctime)s]-[%(levelname)s]-[%(name)s]: %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    root = logging.getLogger()
    root.handlers.clear()

    level = logging.DEBUG if settings.app.debug else logging.INFO
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFMT))

    root.addHandler(handler)

    for _, logger in logging.root.manager.loggerDict.items():
        if isinstance(logger, logging.Logger):
            logger.handlers.clear()
            logger.propagate = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
