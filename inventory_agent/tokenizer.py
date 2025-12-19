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
    "three quarters",
    "bottle",
    "bottles",
    "can",
    "cans",
    "pack",
    "packs",
    "case",
    "cases",
    "keg",
    "kegs",
    "barrel",
    "barrels",
    "bbl",
    "bbls",
    "ounce",
    "ounces",
    "oz",
}


def _looks_like_quantity(segment: str) -> bool:
    seg = normalize_text(segment)
    if re.search(r"\d", seg):
        return True
    for tok in QUANTITY_TOKENS:
        if tok in seg:
            return True
    return False


def _split_on_quantity_tokens(line: str) -> List[str]:
    """Split when multiple quantity phrases appear in one line (handles hyphenated pack/case)."""

    quantity_pattern = (
        r"(?=("  # positive lookahead start
        r"(?:\b\d+(?:\.\d+)?|\bone\b|\btwo\b|\bthree\b|\bfour\b|\bfive\b|\bsix\b|\bseven\b|\beight\b|\bnine\b|\bten\b|\bhalf\b|\bquarter\b|\bthree\s+quarters?)"
        r"\s+(?:\d+[ -]?)?"  # optional numeric prefix for pack sizes like 24-pack
        r"(?:bottles?|bottle|cans?|can|packs?|pack|cases?|case|kegs?|keg|barrels?|bbls?|ounces?|ounce|oz)"  # unit
        r"))"
    )
    matches = [m.start() for m in re.finditer(quantity_pattern, line, flags=re.IGNORECASE)]
    if len(matches) <= 1:
        return [line.strip()]

    parts: List[str] = []
    for i, start in enumerate(matches):
        end = matches[i + 1] if i + 1 < len(matches) else len(line)
        chunk = line[start:end].strip(",;. ").strip()
        if chunk:
            # Drop leading connectors and trailing connectors like "and"/"&"
            chunk = re.sub(r"^(?:and|&)\s+", "", chunk, flags=re.IGNORECASE).strip()
            chunk = re.sub(r"(?:\s+(?:and|&))+\s*$", "", chunk, flags=re.IGNORECASE).strip()
        if chunk:
            parts.append(chunk)
    return parts if parts else [line.strip()]


def split_line_into_segments(line: str) -> List[str]:
    """Split a narrative line into segments when it clearly contains multiple items.

    Heuristic: first try repeated quantity splitting; if not, fall back to splitting on
    'and' or commas only when each piece looks like it carries a quantity token. Otherwise
    keep the line intact.
    """

    if not line:
        return []

    # First, look for multiple quantity phrases in a single sentence and split on them.
    qty_chunks = _split_on_quantity_tokens(line)
    if len(qty_chunks) > 1:
        return qty_chunks

    # Try ampersand / "and" separation when each part looks like a quantity phrase.
    parts = re.split(r"\s+(?:and|&)\s+", line)
    if len(parts) > 1 and all(_looks_like_quantity(p) for p in parts):
        return [p.strip() for p in parts if p.strip()]

    # Try comma separation with the same guard.
    comma_parts = [p.strip() for p in re.split(r",\s*", line) if p.strip()]
    if len(comma_parts) > 1 and all(_looks_like_quantity(p) for p in comma_parts):
        return comma_parts

    return [line.strip()]
