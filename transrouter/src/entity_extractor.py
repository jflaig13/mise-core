"""Entity extraction for the Transrouter.

Deterministic regex-based extraction for dates, numbers, and simple names.
"""

import re
from typing import Any, Dict, Tuple, List

DATE_PATTERNS = [
    r"\b\d{4}-\d{2}-\d{2}\b",  # ISO date
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",  # MM/DD/YYYY
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}(?:,\s*\d{4})?\b",
]

NUMBER_PATTERN = r"\b\d+(?:\.\d+)?\b"
MONEY_PATTERN = r"\$\s*\d+(?:\.\d+)?"


def _extract_dates(text: str) -> List[str]:
    results = []
    for pattern in DATE_PATTERNS:
        results.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return results


def _extract_numbers(text: str) -> List[str]:
    results = re.findall(MONEY_PATTERN, text)
    results.extend(re.findall(NUMBER_PATTERN, text))
    # deduplicate while preserving order
    seen = set()
    unique = []
    for val in results:
        if val not in seen:
            seen.add(val)
            unique.append(val)
    return unique


def _extract_names(text: str) -> List[str]:
    # naive heuristic: capitalized words preceded by "for" or "to"
    names = re.findall(r"\b(?:for|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", text)
    return names


def extract_entities(transcript: str, meta: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
    """Return (entities, confidence)."""
    dates = _extract_dates(transcript)
    numbers = _extract_numbers(transcript)
    names = _extract_names(transcript)

    entities: Dict[str, Any] = {}
    if dates:
        entities["dates"] = dates
    if numbers:
        entities["numbers"] = numbers
    if names:
        entities["names"] = names

    confidence = 0.5
    if entities:
        confidence = min(1.0, 0.5 + 0.1 * len(entities))

    return entities, confidence
