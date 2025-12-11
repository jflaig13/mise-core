"""Entity extraction stub for the Transrouter.

Responsible for pulling out structured entities (dates, totals, names, locations)
from transcripts after intent classification. Placeholder only; no real logic yet.
"""

from typing import Any, Dict, Tuple


def extract_entities(transcript: str, meta: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
    """Return (entities, confidence).

    TODO: implement deterministic extraction rules per domain + shared roster/normalizers.
    """
    raise NotImplementedError
