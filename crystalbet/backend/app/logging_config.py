# logging_config.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),           # Output logs to console
            logging.FileHandler("betting_api.log"),  # Output logs to a file
        ]
    )

logger = logging.getLogger(__name__)
