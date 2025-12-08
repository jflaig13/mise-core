"""Basic tokenizer to split multi-item narrative lines into parseable segments."""

from __future__ import annotations

import re
from typing import List

from .normalizer import normalize_text


QUANTITY_TOKENS = {
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "half",
    "quarter",
    "full",
    "pack",
    "bottle",
    "can",
    "case",
    "percent",
}


def _looks_like_quantity(segment: str) -> bool:
    seg = normalize_text(segment)
    if re.search(r"\d", seg):
        return True
    for tok in QUANTITY_TOKENS:
        if tok in seg:
            return True
    return False


def split_line_into_segments(line: str) -> List[str]:
    """Split a narrative line into segments when it clearly contains multiple items.

    Heuristic: split on 'and' or '&' or commas only if each piece looks like it carries
    its own quantity token. Otherwise, keep the line intact.
    """

    if not line:
        return []

    # Try ampersand / "and" separation
    parts = re.split(r"\s+(?:and|&)\s+", line)
    if len(parts) > 1 and all(_looks_like_quantity(p) for p in parts):
        return [p.strip() for p in parts if p.strip()]

    # Try comma separation
    comma_parts = [p.strip() for p in re.split(r",\s*", line) if p.strip()]
    if len(comma_parts) > 1 and all(_looks_like_quantity(p) for p in comma_parts):
        return comma_parts

    return [line.strip()]
