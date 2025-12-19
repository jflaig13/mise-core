"""Text normalization utilities for inventory parsing."""

from __future__ import annotations

from unidecode import unidecode


def normalize_text(text: str) -> str:
    """Lowercase, remove accents, and trim whitespace for stable matching."""

    return unidecode(text or "").strip().lower()
