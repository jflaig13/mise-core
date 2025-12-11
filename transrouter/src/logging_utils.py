"""Logging utilities stub for the Transrouter.

Provides standardized logging hooks and structured events.
"""

import logging
from typing import Any, Dict


def get_logger(name: str = "transrouter") -> logging.Logger:
    """Return a module-scoped logger with default formatting."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log_event(logger: logging.Logger, event: str, payload: Dict[str, Any]) -> None:
    """Log a structured event."""
    logger.info("event=%s payload=%s", event, payload)
