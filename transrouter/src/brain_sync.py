"""Brain sync for the Transrouter.

Mise is a FILE-BASED INTELLIGENCE SYSTEM. The brain is ALL files within
/mise-core. This module syncs routing rules, workflow specs, and domain
configs from the authoritative brain store.

Responsibilities:
- Load workflow specs for each domain (LPM, CPM, LIM, Swarm, etc.)
- Load brain docs from docs/brain/
- Load shared resources (roster, critical paths)
- Provide clean interface for domain agents to access their brain
- Cache loaded brain for performance, refresh on demand
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)

# Base paths
MISE_CORE_ROOT = Path(__file__).resolve().parent.parent.parent
WORKFLOW_SPECS_DIR = MISE_CORE_ROOT / "workflow_specs"
BRAIN_DOCS_DIR = MISE_CORE_ROOT / "docs" / "brain"
ROSTER_PATH = WORKFLOW_SPECS_DIR / "roster" / "employee_roster.json"

# Domain to workflow spec mapping
DOMAIN_WORKFLOW_SPECS = {
    "payroll": {
        "master": WORKFLOW_SPECS_DIR / "LPM" / "LPM_Workflow_Master.txt",
        "readme": WORKFLOW_SPECS_DIR / "LPM" / "README.md",
        "changes_dir": WORKFLOW_SPECS_DIR / "LPM" / "workflow_changes",
    },
    "payroll_cloud": {
        "master": WORKFLOW_SPECS_DIR / "CPM" / "CPM_Workflow_Master.txt",
        "readme": WORKFLOW_SPECS_DIR / "CPM" / "README.md",
        "changes_dir": WORKFLOW_SPECS_DIR / "CPM" / "workflow_changes",
    },
    "inventory": {
        "master": WORKFLOW_SPECS_DIR / "LIM" / "LIM_Workflow_Master.txt",
        "readme": WORKFLOW_SPECS_DIR / "LIM" / "README.md",
        "changes_dir": WORKFLOW_SPECS_DIR / "LIM" / "workflow_changes",
    },
    "transrouter": {
        "master": WORKFLOW_SPECS_DIR / "transrouter" / "Transrouter_Workflow_Master.txt",
        "readme": WORKFLOW_SPECS_DIR / "transrouter" / "README.md",
        "changes_dir": WORKFLOW_SPECS_DIR / "transrouter" / "workflow_changes",
    },
    "swarm": {
        "master": WORKFLOW_SPECS_DIR / "SWARM" / "SWARM_Workflow_Master.txt",
        "readme": WORKFLOW_SPECS_DIR / "SWARM" / "README.md",
        "changes_dir": WORKFLOW_SPECS_DIR / "SWARM" / "workflow_changes",
    },
}


@dataclass
class DomainBrain:
    """Brain content for a specific domain."""

    domain: str
    workflow_master: str = ""
    workflow_readme: str = ""
    workflow_changes: List[str] = field(default_factory=list)

    def is_loaded(self) -> bool:
        """Check if brain has meaningful content."""
        return bool(self.workflow_master)


@dataclass
class MiseBrain:
    """Complete brain state for Mise.

    Contains all loaded workflow specs, brain docs, and shared resources.
    This is the single source of truth for agent knowledge.
    """

    # Domain-specific brains
    domains: Dict[str, DomainBrain] = field(default_factory=dict)

    # Shared resources
    employee_roster: Dict[str, str] = field(default_factory=dict)
    brain_docs: Dict[str, str] = field(default_factory=dict)
    critical_paths: str = ""

    # Meta
    loaded: bool = False
    load_errors: List[str] = field(default_factory=list)

    def get_domain_brain(self, domain: str) -> Optional[DomainBrain]:
        """Get brain for a specific domain."""
        return self.domains.get(domain)

    def get_canonical_names(self) -> List[str]:
        """Get list of canonical employee names from roster."""
        return sorted(set(self.employee_roster.values()))


# Global brain instance
_brain: Optional[MiseBrain] = None


def _read_file_safe(path: Path) -> str:
    """Read file contents, returning empty string on error."""
    if not path.exists():
        log.debug("File not found: %s", path)
        return ""
    try:
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        log.warning("Failed to read %s: %s", path, exc)
        return ""


def _read_json_safe(path: Path) -> Dict[str, Any]:
    """Read JSON file, returning empty dict on error."""
    if not path.exists():
        log.debug("JSON file not found: %s", path)
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        log.warning("Failed to read JSON %s: %s", path, exc)
        return {}


def _load_domain_brain(domain: str, spec_paths: Dict[str, Path]) -> DomainBrain:
    """Load brain for a specific domain."""
    brain = DomainBrain(domain=domain)

    # Load master spec
    master_path = spec_paths.get("master")
    if master_path:
        brain.workflow_master = _read_file_safe(master_path)
        if brain.workflow_master:
            log.info("Loaded %s workflow master (%d chars)", domain, len(brain.workflow_master))

    # Load readme
    readme_path = spec_paths.get("readme")
    if readme_path:
        brain.workflow_readme = _read_file_safe(readme_path)

    # Load workflow changes
    changes_dir = spec_paths.get("changes_dir")
    if changes_dir and changes_dir.exists():
        for change_file in sorted(changes_dir.glob("*.txt")):
            content = _read_file_safe(change_file)
            if content:
                brain.workflow_changes.append(f"=== {change_file.name} ===\n{content}")

    return brain


def _load_brain_docs() -> Dict[str, str]:
    """Load all brain docs from docs/brain/."""
    brain_docs = {}

    if not BRAIN_DOCS_DIR.exists():
        log.warning("Brain docs directory not found: %s", BRAIN_DOCS_DIR)
        return brain_docs

    for doc_file in sorted(BRAIN_DOCS_DIR.glob("*.md")):
        content = _read_file_safe(doc_file)
        if content:
            brain_docs[doc_file.stem] = content
            log.debug("Loaded brain doc: %s", doc_file.name)

    log.info("Loaded %d brain docs", len(brain_docs))
    return brain_docs


def load_brain_snapshot() -> MiseBrain:
    """Load the complete brain from disk.

    This is the main entry point for loading the brain. It reads:
    - All domain workflow specs
    - All brain docs
    - Employee roster
    - Critical paths

    Returns:
        MiseBrain with all loaded content.
    """
    global _brain

    log.info("Loading Mise brain snapshot...")
    brain = MiseBrain()
    errors = []

    # Load domain brains
    for domain, spec_paths in DOMAIN_WORKFLOW_SPECS.items():
        try:
            domain_brain = _load_domain_brain(domain, spec_paths)
            brain.domains[domain] = domain_brain
        except Exception as exc:
            error_msg = f"Failed to load {domain} brain: {exc}"
            log.error(error_msg)
            errors.append(error_msg)

    # Load employee roster
    brain.employee_roster = _read_json_safe(ROSTER_PATH)
    if brain.employee_roster:
        log.info("Loaded employee roster (%d entries)", len(brain.employee_roster))

    # Load brain docs
    brain.brain_docs = _load_brain_docs()

    # Load critical paths
    critical_paths_file = WORKFLOW_SPECS_DIR / "CRITICAL_PATHS.md"
    brain.critical_paths = _read_file_safe(critical_paths_file)

    brain.loaded = True
    brain.load_errors = errors

    _brain = brain
    log.info("Brain snapshot loaded (domains=%d, brain_docs=%d, roster=%d)",
             len(brain.domains), len(brain.brain_docs), len(brain.employee_roster))

    return brain


def get_brain() -> MiseBrain:
    """Get the current brain, loading if necessary.

    This is the recommended way to access the brain. It ensures
    the brain is loaded before use.
    """
    global _brain

    if _brain is None or not _brain.loaded:
        return load_brain_snapshot()

    return _brain


def refresh_brain_cache() -> MiseBrain:
    """Force-refresh the brain from disk.

    Use this when you know files have changed and need to reload.
    """
    global _brain
    _brain = None
    return load_brain_snapshot()


def get_domain_workflow_master(domain: str) -> str:
    """Get the workflow master spec for a domain.

    Convenience function for quick access to domain specs.

    Args:
        domain: Domain name (payroll, inventory, etc.)

    Returns:
        Workflow master content, or empty string if not found.
    """
    brain = get_brain()
    domain_brain = brain.get_domain_brain(domain)
    if domain_brain:
        return domain_brain.workflow_master
    return ""


def get_employee_roster() -> Dict[str, str]:
    """Get the employee roster mapping.

    Returns:
        Dict mapping transcription variants to canonical names.
    """
    brain = get_brain()
    return brain.employee_roster


def get_brain_doc(doc_name: str) -> str:
    """Get a specific brain doc by name (without .md extension).

    Args:
        doc_name: Document name (e.g., "121224__system-truth-how-mise-works")

    Returns:
        Document content, or empty string if not found.
    """
    brain = get_brain()
    return brain.brain_docs.get(doc_name, "")


def get_all_brain_docs() -> Dict[str, str]:
    """Get all brain docs.

    Returns:
        Dict mapping doc names to content.
    """
    brain = get_brain()
    return brain.brain_docs
