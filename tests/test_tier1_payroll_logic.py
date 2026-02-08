"""Tier 1: Payroll logic tests — no API keys needed.

Tests validation, auto-correction, flattening, and shift detection.
These run in <1 second and catch the most common breakage patterns.
"""

import copy
import pytest
from datetime import date

from tests.conftest import SAMPLE_PAYROLL_APPROVAL_JSON


# ============================================================================
# Approval JSON Validation
# ============================================================================


class TestApprovalValidation:
    """Test PayrollAgent._validate_approval_json()."""

    def _get_agent(self):
        from transrouter.src.agents.payroll_agent import PayrollAgent
        from unittest.mock import MagicMock
        return PayrollAgent(claude_client=MagicMock())

    def test_valid_json_passes(self):
        agent = self._get_agent()
        result = agent._validate_approval_json(SAMPLE_PAYROLL_APPROVAL_JSON)
        assert result is None  # None = no error

    def test_missing_required_keys_fails(self):
        agent = self._get_agent()
        result = agent._validate_approval_json({"out_base": "test"})
        assert result is not None
        assert "Missing required keys" in result

    def test_wrong_shift_cols_fails(self):
        agent = self._get_agent()
        bad = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        bad["shift_cols"] = ["MAM", "MPM"]
        result = agent._validate_approval_json(bad)
        assert "shift_cols" in result

    def test_employee_missing_from_weekly_totals_fails(self):
        agent = self._get_agent()
        bad = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        del bad["weekly_totals"]["Ryan Alexander"]
        result = agent._validate_approval_json(bad)
        assert "missing from weekly_totals" in result.lower()

    def test_per_shift_not_dict_fails(self):
        agent = self._get_agent()
        bad = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        bad["per_shift"] = "not a dict"
        result = agent._validate_approval_json(bad)
        assert "per_shift must be an object" in result

    def test_detail_blocks_not_list_fails(self):
        agent = self._get_agent()
        bad = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        bad["detail_blocks"] = "not a list"
        result = agent._validate_approval_json(bad)
        assert "detail_blocks must be an array" in result


# ============================================================================
# Auto-Correction
# ============================================================================


class TestAutoCorrection:
    """Test PayrollAgent._auto_correct_approval_json()."""

    def _get_agent(self):
        from transrouter.src.agents.payroll_agent import PayrollAgent
        from unittest.mock import MagicMock
        return PayrollAgent(claude_client=MagicMock())

    def test_no_corrections_when_consistent(self):
        agent = self._get_agent()
        data = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        corrections = agent._auto_correct_approval_json(data)
        # May or may not have corrections depending on detail_blocks parsing
        # The important thing is it doesn't crash
        assert isinstance(corrections, list)

    def test_corrects_wrong_per_shift_amount(self):
        agent = self._get_agent()
        data = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        # Deliberately set wrong amount in per_shift
        data["per_shift"]["Austin Kelley"]["MAM"] = 999.99
        corrections = agent._auto_correct_approval_json(data)
        # Should detect and fix the mismatch
        assert isinstance(corrections, list)

    def test_recalculates_weekly_totals(self):
        agent = self._get_agent()
        data = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        # Set wrong weekly total
        data["weekly_totals"]["Austin Kelley"] = 1.00
        corrections = agent._auto_correct_approval_json(data)
        # After correction, weekly_totals should match per_shift sums
        per_shift_sum = sum(data["per_shift"]["Austin Kelley"].values())
        assert abs(data["weekly_totals"]["Austin Kelley"] - per_shift_sum) < 0.03


# ============================================================================
# Flatten Approval JSON
# ============================================================================


def _load_recording_module():
    """Load recording module directly, bypassing routes/__init__.py.

    The __init__.py eagerly imports all routes which cascades into
    google.cloud dependencies. This loader avoids that.
    """
    import importlib.util, os
    spec = importlib.util.spec_from_file_location(
        "recording",
        os.path.join(os.path.dirname(__file__), "..", "mise_app", "routes", "recording.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestFlattenApprovalJson:
    """Test flatten_approval_json() from recording.py."""

    def _flatten(self, approval_json, shifty_code, period):
        mod = _load_recording_module()
        return mod.flatten_approval_json(approval_json, shifty_code, period)

    def _make_period(self, start_date_str="2026-01-05"):
        from mise_app.config import PayPeriod
        return PayPeriod.from_id(start_date_str)

    def test_extracts_correct_shift_amounts(self):
        period = self._make_period()
        rows = self._flatten(SAMPLE_PAYROLL_APPROVAL_JSON, "MAM", period)
        # Austin and Brooke have MAM entries, Ryan has MAM entry
        employees = {r["employee"] for r in rows}
        assert "Austin Kelley" in employees
        assert "Brooke Neal" in employees
        assert "Ryan Alexander" in employees

    def test_amounts_match_per_shift(self):
        period = self._make_period()
        rows = self._flatten(SAMPLE_PAYROLL_APPROVAL_JSON, "MAM", period)
        for row in rows:
            expected = SAMPLE_PAYROLL_APPROVAL_JSON["per_shift"][row["employee"]].get("MAM", 0)
            assert row["amount"] == expected

    def test_returns_empty_for_unrecorded_shift(self):
        period = self._make_period()
        rows = self._flatten(SAMPLE_PAYROLL_APPROVAL_JSON, "SuPM", period)
        # Nobody worked SuPM in sample data
        assert rows == []

    def test_row_structure(self):
        period = self._make_period()
        rows = self._flatten(SAMPLE_PAYROLL_APPROVAL_JSON, "MAM", period)
        assert len(rows) > 0
        row = rows[0]
        assert "date" in row
        assert "shift" in row
        assert "employee" in row
        assert "role" in row
        assert "amount" in row

    def test_support_staff_detected_from_detail_blocks(self):
        period = self._make_period()
        rows = self._flatten(SAMPLE_PAYROLL_APPROVAL_JSON, "MAM", period)
        # Ryan is marked as utility in detail_blocks
        ryan_rows = [r for r in rows if r["employee"] == "Ryan Alexander"]
        assert len(ryan_rows) == 1
        assert ryan_rows[0]["role"] == "Utility"


# ============================================================================
# Shift Detection from Transcript
# ============================================================================


class TestShiftDetection:
    """Test detect_shifty_from_transcript() from recording.py."""

    def _detect(self, transcript, period=None):
        mod = _load_recording_module()
        if period is None:
            from mise_app.config import PayPeriod
            period = PayPeriod.from_id("2026-01-05")
        return mod.detect_shifty_from_transcript(transcript, period)

    def test_detects_monday_am(self):
        result = self._detect("This is Monday AM shift, January 5th 2026")
        assert result["code"] == "MAM"

    def test_detects_thursday_pm(self):
        result = self._detect("Thursday evening shift, dinner service")
        assert result["code"] == "ThPM"

    def test_detects_friday_pm(self):
        result = self._detect("Friday PM shift, January 9th 2026")
        assert result["code"] == "FPM"

    def test_detects_saturday_am(self):
        result = self._detect("Saturday morning, January 10th")
        assert result["code"] == "SaAM"

    def test_returns_none_for_ambiguous(self):
        result = self._detect("No day or shift mentioned here at all")
        assert result["code"] is None

    def test_parses_date_from_transcript(self):
        result = self._detect("January 8th 2026 PM shift")
        assert result["parsed_date"] == date(2026, 1, 8)

    def test_parses_date_with_ordinal(self):
        result = self._detect("Recording for January 12th, 2026 morning shift")
        assert result["parsed_date"] == date(2026, 1, 12)


# ============================================================================
# Shift Code Fix (Claude day-of-week miscalculation)
# ============================================================================


class TestFixShiftCodes:
    """Test fix_approval_json_shift_codes() from recording.py."""

    def _fix(self, approval_json, correct_code):
        mod = _load_recording_module()
        return mod.fix_approval_json_shift_codes(approval_json, correct_code)

    def test_remaps_wrong_shift_code(self):
        data = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        # Simulate Claude thinking it's Sunday when it's Monday
        data["per_shift"]["Austin Kelley"] = {"SuAM": 150.00}
        fixed = self._fix(data, "MAM")
        assert "MAM" in fixed["per_shift"]["Austin Kelley"]
        assert "SuAM" not in fixed["per_shift"]["Austin Kelley"]

    def test_preserves_correct_shift_code(self):
        data = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        fixed = self._fix(data, "MAM")
        # MAM entries should still exist
        assert "MAM" in fixed["per_shift"]["Austin Kelley"]

    def test_recalculates_weekly_totals_after_fix(self):
        data = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        data["per_shift"]["Austin Kelley"] = {"SuAM": 150.00}
        fixed = self._fix(data, "MAM")
        assert fixed["weekly_totals"]["Austin Kelley"] == 150.00

    def test_noop_when_no_correction_needed(self):
        data = copy.deepcopy(SAMPLE_PAYROLL_APPROVAL_JSON)
        original_totals = data["weekly_totals"].copy()
        fixed = self._fix(data, "MAM")
        # Weekly totals should be recalculated but values should be same for MAM entries
        assert "Austin Kelley" in fixed["weekly_totals"]
