"""Intent classifier for the Transrouter.

Classifies domain_agent and intent_type from a transcript using simple rules.
"""

import re
from typing import Any, Dict, Tuple

PAYROLL_KEYWORDS = {
    "payroll",
    "pay stub",
    "wage",
    "hour",
    "hours",
    "overtime",
    "paycheck",
    "tips",
    "tipsheet",
    "timecard",
    "timesheet",
    "pay",
}

INVENTORY_KEYWORDS = {
    "inventory",
    "stock",
    "item",
    "items",
    "count",
    "counts",
    "supply",
    "supplies",
    "sku",
    "product",
    "catalog",
    "quantity",
}


def _score_keywords(transcript_lower: str, keywords) -> int:
    return sum(1 for kw in keywords if kw in transcript_lower)


def classify_intent(transcript: str, meta: Dict[str, Any]) -> Tuple[str, str, float]:
    """Return (domain_agent, intent_type, confidence)."""
    normalized = transcript.strip().lower()
    payroll_score = _score_keywords(normalized, PAYROLL_KEYWORDS)
    inventory_score = _score_keywords(normalized, INVENTORY_KEYWORDS)

    if payroll_score == 0 and inventory_score == 0:
        domain = "payroll"
        confidence = 0.5
    elif payroll_score >= inventory_score:
        domain = "payroll"
        confidence = min(1.0, 0.6 + 0.1 * payroll_score)
    else:
        domain = "inventory"
        confidence = min(1.0, 0.6 + 0.1 * inventory_score)

    intent_type = "query" if re.search(r"\bhow\b|\bwhat\b|\bwhen\b|\bwhere\b|\bwhy\b|\bwho\b", normalized) else "update"
    return domain, intent_type, confidence
