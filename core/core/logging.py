config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s  %(name)-16s  %(levelname)-8s  %(message)s",
            "datefmt": None,
        },
        "simple": {
            "format": "%(asctime)s  %(levelname)-8s  %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "filename": "logs/log.txt",
            "when": "midnight",
        },
    },
    "loggers": {
        "my_logger": {"level": "DEBUG", "handlers": ["console"], "propagate": False}
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file"]},
}
