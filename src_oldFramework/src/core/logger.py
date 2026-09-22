import logging
import os
from datetime import datetime

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Console handler
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        # Logs directory
        logs_dir = os.path.join(os.getcwd(), "reports", "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Daily log file name: Executionlog_DD-MM-YYYY.log
        log_file = os.path.join(
            logs_dir, f"Executionlog_{datetime.now().strftime('%d-%m-%Y')}.log"
        )

        # File handler (append mode so multiple runs in same day go to same file)
        file_handler = logging.FileHandler(log_file, mode="a")
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger

