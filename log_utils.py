import logging
from functools import wraps


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s - (%(filename)s - %(funcName)s - %(lineno)s) - %(message)s",
    encoding="utf-8"
)


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            logging.info("Completed successfully")
            return res
        except Exception as e:
            logging.error("Failed with exception", exc_info=True)
            raise e
    return wrapper


def log_info(message):
    logging.info(message)


def log_critical(message):
    logging.critical(message, exc_info=True)