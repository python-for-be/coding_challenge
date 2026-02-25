import logging

# Define log format
log_format: str = "{asctime} - {name} - {levelname} - {message}"
date_format: str = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(level="DEBUG", format=log_format, datefmt=date_format, style="{")

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")
