import logging.config

from .logging import config

# Global private-ish flag for logging setup.
_IS_LOGGING_SET_UP = False


def setup_logging(logger_name):
    global _IS_LOGGING_SET_UP

    # Load the logger configuration only once.
    if not _IS_LOGGING_SET_UP:
        logging.config.dictConfig(config=config)
        _IS_LOGGING_SET_UP = True

    return logging.getLogger(logger_name)
