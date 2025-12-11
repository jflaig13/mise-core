"""Logging utilities stub for the Transrouter.

Provides standardized logging hooks and structured events. Placeholder only.
"""

import logging
from typing import Any, Dict


def get_logger(name: str = "transrouter") -> logging.Logger:
    """Return a module-scoped logger with default formatting."""
    # TODO: configure structured logging and correlation IDs.
    return logging.getLogger(name)


def log_event(logger: logging.Logger, event: str, payload: Dict[str, Any]) -> None:
    """Log a structured event."""
    # TODO: emit JSON-formatted logs and respect verbosity flags.
    logger.info("event=%s payload=%s", event, payload)
