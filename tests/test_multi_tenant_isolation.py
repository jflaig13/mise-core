"""Tests for multi-tenant data isolation.

These tests verify that restaurant data is properly isolated:
- Papa Surf cannot see SoWal House data
- SoWal House cannot see Papa Surf data
"""

import pytest
from pathlib import Path
import json
import os

# Set up test environment before imports
os.environ["ENVIRONMENT"] = "development"


@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    """Create a temporary storage backend."""
    from mise_app.storage_backend import LocalStorage
    import mise_app.storage_backend as sb

    # Create restaurant directories
    (tmp_path / "papasurf" / "2026-01-19").mkdir(parents=True)
    (tmp_path / "sowalhouse" / "2026-01-19").mkdir(parents=True)

    # Create and set the test backend
    test_backend = LocalStorage(tmp_path)
    monkeypatch.setattr(sb, "_storage_backend", test_backend)

    return test_backend


class TestApprovalStorageIsolation:
    """Test that approval storage is properly isolated by restaurant."""

    def test_add_shifty_isolation(self, temp_storage):
        """Verify shifties are stored per-restaurant."""
        from mise_app.local_storage import LocalApprovalStorage

        storage = LocalApprovalStorage()

        # Add shifty to papasurf (note: lowercase keys as expected by add_shifty)
        papasurf_rows = [
            {"employee": "Austin", "role": "Server", "amount": 100.00}
        ]
        storage.add_shifty(
            period_id="2026-01-19",
            rows=papasurf_rows,
            filename="MAM.wav",
            transcript="Papa Surf Monday AM",
            restaurant_id="papasurf"
        )

        # Add shifty to sowalhouse
        sowalhouse_rows = [
            {"employee": "John", "role": "Server", "amount": 150.00}
        ]
        storage.add_shifty(
            period_id="2026-01-19",
            rows=sowalhouse_rows,
            filename="MAM.wav",
            transcript="SoWal House Monday AM",
            restaurant_id="sowalhouse"
        )

        # Verify isolation
        papasurf_data = storage.get_all("2026-01-19", restaurant_id="papasurf")
        sowalhouse_data = storage.get_all("2026-01-19", restaurant_id="sowalhouse")

        assert len(papasurf_data) == 1
        assert len(sowalhouse_data) == 1

        assert papasurf_data[0]["Employee"] == "Austin"
        assert sowalhouse_data[0]["Employee"] == "John"

        # Cross-check: papasurf should not see John
        papasurf_employees = {r["Employee"] for r in papasurf_data}
        assert "John" not in papasurf_employees

        # Cross-check: sowalhouse should not see Austin
        sowalhouse_employees = {r["Employee"] for r in sowalhouse_data}
        assert "Austin" not in sowalhouse_employees


class TestTotalsStorageIsolation:
    """Test that totals storage is properly isolated by restaurant."""

    def test_totals_isolation(self, temp_storage):
        """Verify totals are stored per-restaurant."""
        from mise_app.local_storage import LocalTotalsStorage

        storage = LocalTotalsStorage()

        # Add totals to papasurf
        storage.add_shift_amount(
            period_id="2026-01-19",
            employee="Austin",
            shift_code="MAM",
            amount=100.00,
            restaurant_id="papasurf"
        )

        # Add totals to sowalhouse
        storage.add_shift_amount(
            period_id="2026-01-19",
            employee="John",
            shift_code="MAM",
            amount=150.00,
            restaurant_id="sowalhouse"
        )

        # Verify isolation using get_all_totals
        papasurf_totals = storage.get_all_totals("2026-01-19", restaurant_id="papasurf")
        sowalhouse_totals = storage.get_all_totals("2026-01-19", restaurant_id="sowalhouse")

        # Check that each restaurant only sees their own data
        papasurf_names = {t["name"] for t in papasurf_totals}
        sowalhouse_names = {t["name"] for t in sowalhouse_totals}

        assert "Austin" in papasurf_names
        assert "John" not in papasurf_names

        assert "John" in sowalhouse_names
        assert "Austin" not in sowalhouse_names


class TestShiftyStateIsolation:
    """Test that shifty state is properly isolated by restaurant."""

    def test_shifty_state_isolation(self, temp_storage):
        """Verify shifty states are stored per-restaurant."""
        from mise_app.config import ShiftyStateManager

        state_manager = ShiftyStateManager()

        # Set state for papasurf
        state_manager.set_status("2026-01-19", "MAM", "approved", restaurant_id="papasurf")

        # Set state for sowalhouse
        state_manager.set_status("2026-01-19", "MAM", "pending", restaurant_id="sowalhouse")

        # Verify isolation
        papasurf_status = state_manager.get_status("2026-01-19", "MAM", restaurant_id="papasurf")
        sowalhouse_status = state_manager.get_status("2026-01-19", "MAM", restaurant_id="sowalhouse")

        assert papasurf_status == "approved"
        assert sowalhouse_status == "pending"

        # They should be different
        assert papasurf_status != sowalhouse_status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
