import logging
import sys
from pathlib import Path
from typing import TextIO, Any


def setup_logging(log_level: str = "INFO", log_file: str | None = None) -> None:
    """Configure logging for the FastAPI application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging output
    """
    # Create logs directory if logging to file
    if log_file:
        log_path: Path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Define log format
    log_format: str = "{asctime} - {name} - {levelname} - {message}"
    date_format: str = "%Y-%m-%d %H:%M:%S"

    # Configure handlers
    handlers: list[logging.StreamHandler[TextIO | Any] | Any] = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    # Basic configuration
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
        force=True,
        style="{",
    )


logger = logging.getLogger(__name__)

setup_logging(log_level="DEBUG", log_file=None)

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
