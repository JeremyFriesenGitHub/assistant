import logging
import json
from typing import Optional, Dict, Any

# ANSI escape codes
LOG_COLORS = {
    "DEBUG": "\033[94m",  # Blue
    "INFO": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "RESET": "\033[0m",  # Reset to default
}


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        level_color = LOG_COLORS.get(record.levelname, "")
        reset = LOG_COLORS["RESET"]
        record.msg = f"{level_color}{record.msg}{reset}"
        return super().format(record)


class SemanticLogger:
    def __init__(self, name: Optional[str] = None):
        self.logger = logging.getLogger(name or __name__)
        handler = logging.StreamHandler()

        formatter = ColorFormatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)

        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

    def info(self, event: str, **data: Any):
        self.logger.info(self._format(event, data))

    def warning(self, event: str, **data: Any):
        self.logger.warning(self._format(event, data))

    def error(self, event: str, **data: Any):
        self.logger.error(self._format(event, data))

    def debug(self, event: str, **data: Any):
        self.logger.debug(self._format(event, data))

    def _format(self, event: str, data: Dict[str, Any]) -> str:
        structured = {"event": event, **data}
        return json.dumps(structured)


# Usage
logger = SemanticLogger()
