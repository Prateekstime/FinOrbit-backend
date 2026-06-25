import logging
import sys
from logging.handlers import RotatingFileHandler
from config import settings


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging():
    """
    Setup logging configuration
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # Remove existing handlers
    logger.handlers = []

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(
        logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    )
    logger.addHandler(console_handler)

    # Create file handler
    if settings.LOG_FILE:
        file_handler = RotatingFileHandler(
            settings.LOG_FILE,
            maxBytes=10_485_760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(settings.LOG_LEVEL)
        file_handler.setFormatter(
            logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        )
        logger.addHandler(file_handler)

    # Set log levels for third-party libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logger


logger = setup_logging()