import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format."""

    def format(self, record: logging.LogRecord) -> str:
        """Formats a logging record into a JSON string."""
        log_record: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "line": record.lineno,
        }

        # Include exception info if available
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Include extra fields if passed via logger.info("msg", extra={"key": "val"})
        if hasattr(record, "extra_fields"):
            log_record.update(record.extra_fields)

        return json.dumps(log_record)


def setup_logging(log_level: str = "INFO", log_file: str | None = None) -> None:
    """Sets up the logging configuration for the application."""
    if log_file:
        log_path: Path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configure handlers
    json_formatter = JsonFormatter()

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(json_formatter)

    handlers: list[logging.Handler] = [stdout_handler]

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(json_formatter)
        handlers.append(file_handler)

    # Basic configuration
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        handlers=handlers,
        force=True,
    )
