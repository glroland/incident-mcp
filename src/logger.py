import functools
import logging

from settings import settings


def configure_logging() -> None:
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def log_call(func):
    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        params = ", ".join(
            [*(repr(a) for a in args), *(f"{k}={v!r}" for k, v in kwargs.items())]
        )
        logger.info("%s(%s)", func.__name__, params)
        result = func(*args, **kwargs)
        logger.info("%s → %r", func.__name__, result)
        return result

    return wrapper
