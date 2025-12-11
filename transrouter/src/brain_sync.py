"""Brain sync stub for the Transrouter.

Responsible for syncing Transrouter rules, prompts, and domain configs from the
authoritative brain store (e.g., workflow_specs, AGENT_POLICY). Placeholder only.
"""

from typing import Any, Dict


def load_brain_snapshot() -> Dict[str, Any]:
    """Load the latest routing/intent rules from disk or remote store.

    TODO: implement pull from workflow_specs and caching strategy.
    """
    raise NotImplementedError


def refresh_brain_cache() -> None:
    """Force-refresh the cached brain snapshot.

    TODO: implement reload hooks and change detection.
    """
    raise NotImplementedError
