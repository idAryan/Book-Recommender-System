import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate log file name with timestamp
LOG_FILE = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO
)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger for the given module or file name.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
        logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger
