"""
Module: src.logger

Description:
    - Set up logging
"""

import logging
from logging import Formatter, StreamHandler


def get_logger(name: str) -> logging.Logger:
    # set up formatter
    formatter = Formatter(
        r"%(levelname)-8s %(asctime)s [%(name)s - %(funcName)s] %(message)s"
    )

    # setup handler
    console = StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)

    # initiate logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # add handlers
    logger.addHandler(console)

    return logger
