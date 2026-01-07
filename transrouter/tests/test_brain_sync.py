"""Tests for brain_sync module."""

import json
from pathlib import Path

from transrouter.src import brain_sync


def test_load_brain_snapshot_returns_mise_brain():
    """Test that load_brain_snapshot returns a MiseBrain object."""
    brain = brain_sync.load_brain_snapshot()

    assert isinstance(brain, brain_sync.MiseBrain)
    assert brain.loaded is True


def test_brain_has_payroll_domain():
    """Test that payroll domain is loaded."""
    brain = brain_sync.get_brain()

    payroll_brain = brain.get_domain_brain("payroll")
    assert payroll_brain is not None
    assert payroll_brain.domain == "payroll"
    assert payroll_brain.is_loaded()
    assert len(payroll_brain.workflow_master) > 0


def test_brain_has_inventory_domain():
    """Test that inventory domain is loaded."""
    brain = brain_sync.get_brain()

    inventory_brain = brain.get_domain_brain("inventory")
    assert inventory_brain is not None
    assert inventory_brain.domain == "inventory"


def test_employee_roster_loaded():
    """Test that employee roster is loaded."""
    brain = brain_sync.get_brain()

    assert len(brain.employee_roster) > 0
    # Check for known employee mappings
    assert "austin" in brain.employee_roster or "Austin Kelley" in brain.employee_roster.values()


def test_get_canonical_names():
    """Test that canonical names are extracted from roster."""
    brain = brain_sync.get_brain()

    names = brain.get_canonical_names()
    assert isinstance(names, list)
    assert len(names) > 0
    # Names should be unique and sorted
    assert names == sorted(set(names))


def test_brain_docs_loaded():
    """Test that brain docs are loaded."""
    brain = brain_sync.get_brain()

    assert len(brain.brain_docs) > 0
    # Check for known brain doc
    assert any("system-truth" in key for key in brain.brain_docs.keys())


def test_get_domain_workflow_master():
    """Test convenience function for getting workflow master."""
    master = brain_sync.get_domain_workflow_master("payroll")

    assert len(master) > 0
    assert "LPM" in master or "payroll" in master.lower()


def test_get_employee_roster_convenience():
    """Test convenience function for getting roster."""
    roster = brain_sync.get_employee_roster()

    assert isinstance(roster, dict)
    assert len(roster) > 0


def test_refresh_brain_cache():
    """Test that refresh_brain_cache reloads the brain."""
    # Get initial brain
    brain1 = brain_sync.get_brain()

    # Refresh
    brain2 = brain_sync.refresh_brain_cache()

    # Should be a new instance
    assert brain2.loaded is True
    assert len(brain2.domains) == len(brain1.domains)


def test_unknown_domain_returns_none():
    """Test that unknown domain returns None."""
    brain = brain_sync.get_brain()

    unknown = brain.get_domain_brain("nonexistent_domain")
    assert unknown is None


def test_get_brain_doc():
    """Test getting a specific brain doc."""
    # Try to get any brain doc
    brain = brain_sync.get_brain()

    if brain.brain_docs:
        first_doc_name = list(brain.brain_docs.keys())[0]
        doc = brain_sync.get_brain_doc(first_doc_name)
        assert len(doc) > 0


def test_get_brain_doc_missing_returns_empty():
    """Test that missing brain doc returns empty string."""
    doc = brain_sync.get_brain_doc("nonexistent_doc_12345")
    assert doc == ""
