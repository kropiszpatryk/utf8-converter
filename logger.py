import logging
import os
from logging import Logger


def init_logger() -> Logger:
    """
    Initializes a logger that logs debug messages to a file and info messages to the terminal.

    Returns:
        Logger: Configured logger instance with file and stream handlers.
    """
    logger = logging.getLogger("TextFileConverter")
    logger.setLevel(logging.DEBUG)

    log_path = os.path.join(os.getcwd(), "conversion.log")

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_formatter = logging.Formatter('%(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger
