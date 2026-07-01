"""
Central logging configuration for Cortexa.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from backend.config import settings

# Create logs directory
Path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)

LOG_FILE = settings.LOG_DIR / "cortexa.log"

logger = logging.getLogger("cortexa")

logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console Logger
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Logger
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)