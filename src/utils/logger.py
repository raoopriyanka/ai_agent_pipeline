import logging
import os
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    """
    Configures a production-ready logger.
    Writes DEBUG and higher to a file, and INFO and higher to the console.
    """
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Create a log file stamped with today's date
    log_filename = f"logs/workflow_{datetime.now().strftime('%Y%m%d')}.log"

    logger = logging.getLogger(name)

    # Prevent duplicate logs if the logger is instantiated multiple times
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Standardize the log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
        )

        # File Handler (Captures everything, including granular debug traces)
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Console Handler (Only shows important info/errors to the terminal)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
