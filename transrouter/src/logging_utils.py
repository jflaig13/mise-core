"""Logging utilities for the Transrouter.

Provides standardized logging with:
- Console output (human-readable)
- File output (human-readable, rotating)
- JSON structured logs (machine-readable, for analytics)
"""

import json
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional

# Log directory - relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = REPO_ROOT / "logs"

# Ensure log directory exists
LOG_DIR.mkdir(exist_ok=True)

# Log files
MAIN_LOG_FILE = LOG_DIR / "transrouter.log"
JSON_LOG_FILE = LOG_DIR / "transrouter.json.log"
TRANSCRIPT_LOG_FILE = LOG_DIR / "transcripts.log"

# Track if logging has been configured
_logging_configured = False


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "event"):
            log_data["event"] = record.event
        if hasattr(record, "payload"):
            log_data["payload"] = record.payload
        if hasattr(record, "transcript"):
            log_data["transcript"] = record.transcript
        if hasattr(record, "extraction"):
            log_data["extraction"] = record.extraction

        return json.dumps(log_data, default=str)


class TranscriptFormatter(logging.Formatter):
    """Format transcript logs for easy reading."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [f"\n{'='*80}", f"[{timestamp}] {record.getMessage()}"]

        if hasattr(record, "transcript"):
            lines.append(f"\nTRANSCRIPT:\n{record.transcript}")

        if hasattr(record, "extraction"):
            lines.append(f"\nEXTRACTED DATA:")
            extraction = record.extraction
            if isinstance(extraction, dict):
                for key, value in extraction.items():
                    lines.append(f"  {key}: {value}")

        if hasattr(record, "result"):
            lines.append(f"\nRESULT:")
            result = record.result
            if isinstance(result, dict):
                for key, value in result.items():
                    if key != "raw_response":  # Skip raw response (too long)
                        lines.append(f"  {key}: {value}")

        lines.append("=" * 80)
        return "\n".join(lines)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure logging for the entire application.

    Sets up:
    - Console handler (INFO level, human-readable)
    - File handler (DEBUG level, human-readable, rotating)
    - JSON file handler (DEBUG level, structured)
    - Transcript file handler (for detailed transcript logging)
    """
    global _logging_configured

    if _logging_configured:
        return

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    root_logger.handlers = []

    # Console handler - human readable, INFO level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler - human readable, DEBUG level, rotating
    file_handler = RotatingFileHandler(
        MAIN_LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # JSON file handler - structured, DEBUG level
    json_handler = RotatingFileHandler(
        JSON_LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    json_handler.setLevel(logging.DEBUG)
    json_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(json_handler)

    _logging_configured = True


def get_logger(name: str = "transrouter") -> logging.Logger:
    """Return a module-scoped logger with proper configuration."""
    configure_logging()
    return logging.getLogger(name)


def get_transcript_logger() -> logging.Logger:
    """Get a dedicated logger for transcript details."""
    configure_logging()

    logger = logging.getLogger("transrouter.transcripts")

    # Add transcript file handler if not already added
    has_transcript_handler = any(
        isinstance(h, logging.FileHandler) and TRANSCRIPT_LOG_FILE.name in str(h.baseFilename)
        for h in logger.handlers
    )

    if not has_transcript_handler:
        transcript_handler = RotatingFileHandler(
            TRANSCRIPT_LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding="utf-8",
        )
        transcript_handler.setLevel(logging.INFO)
        transcript_handler.setFormatter(TranscriptFormatter())
        logger.addHandler(transcript_handler)

    return logger


def log_event(logger: logging.Logger, event: str, payload: Dict[str, Any]) -> None:
    """Log a structured event with payload."""
    # Create a log record with extra fields for JSON formatter
    extra = {"event": event, "payload": payload}
    logger.info("event=%s payload=%s", event, payload, extra=extra)


def log_transcript(
    filename: str,
    transcript: str,
    extraction: Dict[str, Any],
    result: Optional[Dict[str, Any]] = None,
) -> None:
    """Log detailed transcript processing information.

    This creates a detailed log entry showing:
    - The original transcript
    - What was extracted (entities, amounts, names)
    - The final result
    """
    logger = get_transcript_logger()

    extra = {
        "transcript": transcript,
        "extraction": extraction,
    }
    if result:
        extra["result"] = result

    # Use LogRecord with extra fields
    record = logger.makeRecord(
        logger.name,
        logging.INFO,
        __file__,
        0,
        f"Processing: {filename}",
        (),
        None,
    )
    for key, value in extra.items():
        setattr(record, key, value)

    logger.handle(record)


def log_parsing_detail(
    logger: logging.Logger,
    stage: str,
    input_text: str,
    output_data: Any,
    source_spans: Optional[Dict[str, str]] = None,
) -> None:
    """Log detailed parsing information showing what was extracted from where.

    Args:
        logger: Logger instance
        stage: Processing stage (e.g., "entity_extraction", "claude_parsing")
        input_text: The input text being processed
        output_data: The extracted/parsed data
        source_spans: Optional mapping of output fields to source text spans
    """
    detail = {
        "stage": stage,
        "input_length": len(input_text),
        "output": output_data,
    }
    if source_spans:
        detail["source_spans"] = source_spans

    logger.debug(
        "Parsing detail: stage=%s input_chars=%d",
        stage,
        len(input_text),
        extra={"event": "parsing_detail", "payload": detail},
    )
