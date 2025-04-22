"""App level logger"""

import logging
from enum import StrEnum
from rich.logging import RichHandler


LOG_FORMAT = "%(message)s"


class LogLevels(StrEnum):
    """LogLevels enum"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def configure_logging(log_level: str = LogLevels.ERROR):
    """
    Configures log levels.
    If no level is provided, error is used as default.
    If a level not from the enum is provided, default to info.
    """
    log_level = str(log_level.upper())
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        log_level = LogLevels.INFO
        return

    logging.basicConfig(
        level=log_level, format=LOG_FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
