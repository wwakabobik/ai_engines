""" This file contains an configuration for loggers. """

import logging
import sys

from utils.other import is_heroku_environment


def setup_logger(name, log_file, level=logging.DEBUG):
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not is_heroku_environment():
        logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
