"""Tier 2: Payroll pipeline tests — REAL Claude API calls.

These tests send actual transcripts to Claude and verify the output
structure and invariants. They cost ~$0.01 per test and take ~5 seconds each.

Run with: pytest -m live
Skip with: pytest -m "not live"
"""

import os
import pytest

from tests.conftest import REAL_PAYROLL_TRANSCRIPT

# Skip entire module if no API key
pytestmark = pytest.mark.live

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_KEY:
    pytest.skip("ANTHROPIC_API_KEY not set — skipping live tests", allow_module_level=True)


# ============================================================================
# PayrollAgent — Real Claude Parsing
# ============================================================================


class TestPayrollRealParsing:
    """Send real transcripts to Claude, verify output structure."""

    def _get_agent(self):
        from transrouter.src.agents.payroll_agent import PayrollAgent
        return PayrollAgent()

    def test_parse_returns_success(self):
        """Claude should successfully parse a simple payroll transcript."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_PAYROLL_TRANSCRIPT)

        assert result["status"] == "success", f"Parsing failed: {result.get('error')}"
        assert result["agent"] == "payroll"

    def test_approval_json_has_required_keys(self):
        """Output must contain all required approval JSON keys."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_PAYROLL_TRANSCRIPT)

        assert result["status"] == "success", f"Parsing failed: {result.get('error')}"

        approval = result["approval_json"]
        required_keys = [
            "out_base", "header", "shift_cols", "per_shift",
            "cook_tips", "weekly_totals", "detail_blocks",
        ]
        for key in required_keys:
            assert key in approval, f"Missing key: {key}"

    def test_shift_cols_has_14_entries(self):
        """shift_cols must always be the canonical 14 shift codes."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_PAYROLL_TRANSCRIPT)

        assert result["status"] == "success"
        assert len(result["approval_json"]["shift_cols"]) == 14

    def test_employees_in_per_shift_match_weekly_totals(self):
        """Every employee in per_shift must appear in weekly_totals."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_PAYROLL_TRANSCRIPT)

        assert result["status"] == "success"
        approval = result["approval_json"]

        per_shift_employees = set(approval["per_shift"].keys())
        weekly_total_employees = set(approval["weekly_totals"].keys())

        # per_shift employees should be subset of weekly_totals
        missing = per_shift_employees - weekly_total_employees
        assert not missing, f"Employees in per_shift but not weekly_totals: {missing}"

    def test_per_shift_sums_match_weekly_totals(self):
        """Sum of per_shift amounts must match weekly_totals within $0.02."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_PAYROLL_TRANSCRIPT)

        assert result["status"] == "success"
        approval = result["approval_json"]

        for employee, shifts in approval["per_shift"].items():
            calculated = sum(shifts.values())
            stated = approval["weekly_totals"].get(employee, 0)
            diff = abs(calculated - stated)
            assert diff <= 0.02, (
                f"{employee}: per_shift sum ${calculated:.2f} != "
                f"weekly_total ${stated:.2f} (diff: ${diff:.2f})"
            )

    def test_transcript_mentions_employees_appear_in_output(self):
        """Employees mentioned in transcript should appear in output."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_PAYROLL_TRANSCRIPT)

        assert result["status"] == "success"
        approval = result["approval_json"]

        all_employees = set(approval["per_shift"].keys()) | set(approval["cook_tips"].keys())
        # The transcript mentions Austin, Brooke, and Ryan
        employee_names = [name.lower() for name in all_employees]
        employee_str = " ".join(employee_names)

        assert "austin" in employee_str, "Austin not found in output"
        assert "brooke" in employee_str, "Brooke not found in output"
        assert "ryan" in employee_str, "Ryan not found in output"

    def test_detail_blocks_are_list_of_lists(self):
        """detail_blocks must be a list of [label, lines] pairs."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_PAYROLL_TRANSCRIPT)

        assert result["status"] == "success"
        detail_blocks = result["approval_json"]["detail_blocks"]

        assert isinstance(detail_blocks, list)
        for block in detail_blocks:
            assert isinstance(block, list), f"Block is not a list: {type(block)}"
            assert len(block) >= 2, f"Block too short: {block}"
            assert isinstance(block[0], str), f"Block label not string: {block[0]}"
            assert isinstance(block[1], list), f"Block lines not list: {block[1]}"


# ============================================================================
# PayrollAgent.process_audio — Full pipeline with real ASR + Claude
# (skipped by default since it requires audio bytes)
# ============================================================================

# process_audio() requires actual audio bytes, which we don't have in CI.
# The mocked version in test_tier1_agent_pipelines.py covers the plumbing.
# The real Claude parsing above covers the model behavior.
# Together they give full coverage without needing audio files.
