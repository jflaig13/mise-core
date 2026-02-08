"""Shared test fixtures for Mise test suite."""

import json
import os
import sys
from unittest.mock import MagicMock

import pytest

# Ensure repo root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


# ============================================================================
# Sample Data Fixtures
# ============================================================================

SAMPLE_PAYROLL_APPROVAL_JSON = {
    "out_base": "TipReport_010626_011226",
    "header": "Week of January 6–12, 2026",
    "shift_cols": [
        "MAM", "MPM", "TAM", "TPM", "WAM", "WPM",
        "ThAM", "ThPM", "FAM", "FPM", "SaAM", "SaPM",
        "SuAM", "SuPM",
    ],
    "per_shift": {
        "Austin Kelley": {"MAM": 150.00, "MPM": 200.00},
        "Brooke Neal": {"MAM": 150.00, "TPM": 180.00},
        "Ryan Alexander": {"MAM": 30.00, "MPM": 40.00},
    },
    "cook_tips": {},
    "weekly_totals": {
        "Austin Kelley": 350.00,
        "Brooke Neal": 330.00,
        "Ryan Alexander": 70.00,
    },
    "detail_blocks": [
        ["Mon Jan 6 — AM (tip pool)", [
            "Pool: Austin Kelley $200 + Brooke Neal $200 = $400",
            "Tipout to Ryan: $60",
            "Austin Kelley: $200.00 - $30.00 = $150.00",
            "Brooke Neal: $200.00 - $30.00 = $150.00",
            "Ryan Alexander: $30.00 (utility)",
        ]],
        ["Mon Jan 6 — PM (tip pool)", [
            "Austin Kelley: $200.00",
            "Ryan Alexander: $40.00 (utility)",
        ]],
        ["Tue Jan 7 — PM (tip pool)", [
            "Brooke Neal: $180.00",
        ]],
    ],
}

SAMPLE_INVENTORY_JSON = {
    "category": "bar",
    "area": "back bar",
    "items": [
        {
            "product_name": "Milagro Reposado Tequila",
            "quantity": 0.7,
            "unit": "bottle",
            "notes": "70% remaining",
        },
        {
            "product_name": "Coors Light 12oz Can",
            "quantity": 7,
            "unit": "cans",
            "notes": "",
        },
        {
            "product_name": "High Rise Blueberry",
            "quantity": 6,
            "unit": "4-packs",
            "notes": "",
        },
    ],
    "counted_by": "Jonathan",
    "timestamp": "2026-01-31T14:30:00Z",
}

# A real payroll transcript (short, single shift) for Tier 2 tests
REAL_PAYROLL_TRANSCRIPT = """
This is the payroll recording for pay period January 6th to January 12th 2026.
Monday January 6th AM shift. Tip pool.
Austin Kelley before tipout $200 food sales $547.
Brooke Neal before tipout $195 food sales $480.
Ryan Alexander was utility.
Tipout from food sales is 2.5%.
"""

# A real inventory transcript (short) for Tier 2 tests
REAL_INVENTORY_TRANSCRIPT = """
Back bar inventory. We have 70% of a bottle of Milagro Reposado,
7 Coors Lights, 6 four-packs of High Rise Blueberry,
12 Michelob Ultras, half a bottle of Tito's, and 3 bottles of Charles de Fer Brut.
"""


# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_claude_payroll():
    """Mock Claude client that returns sample payroll approval JSON."""
    from transrouter.src.claude_client import ClaudeClient, ClaudeResponse

    mock_client = MagicMock(spec=ClaudeClient)
    mock_client.call.return_value = ClaudeResponse(
        success=True,
        content=json.dumps(SAMPLE_PAYROLL_APPROVAL_JSON),
        json_data=SAMPLE_PAYROLL_APPROVAL_JSON,
        model="claude-sonnet-4-20250514",
        usage={"input_tokens": 1000, "output_tokens": 500},
    )
    return mock_client


@pytest.fixture
def mock_claude_inventory():
    """Mock Claude client that returns sample inventory JSON."""
    from transrouter.src.claude_client import ClaudeClient, ClaudeResponse

    mock_client = MagicMock(spec=ClaudeClient)
    mock_client.call.return_value = ClaudeResponse(
        success=True,
        content=json.dumps(SAMPLE_INVENTORY_JSON),
        json_data=SAMPLE_INVENTORY_JSON,
        model="claude-sonnet-4-20250514",
        usage={"input_tokens": 500, "output_tokens": 200},
    )
    return mock_client


@pytest.fixture
def mock_asr():
    """Mock ASR provider that returns a fixed transcript."""
    from transrouter.src.schemas import TranscriptResult

    mock = MagicMock()
    mock.transcribe.return_value = TranscriptResult(
        transcript="Monday January 6th AM shift. Austin Kelley $200. Brooke Neal $195.",
        confidence=0.95,
    )
    return mock


def has_anthropic_key():
    """Check if ANTHROPIC_API_KEY is available for live tests."""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


# ============================================================================
# Product Catalog Loader (for Normalization Law tests)
# ============================================================================


def load_valid_product_names():
    """Load the full product catalog and return the set of ALL valid canonical product names.

    This is the single source of truth for the Normalization Law:
    every item parsed by the inventory agent MUST have a product_name
    that appears in this set. No exceptions.
    """
    from pathlib import Path

    repo_root = Path(__file__).parent.parent

    # Load BOTH catalog files — the prompt builder uses data/inventory_catalog.json
    # (which Claude sees), and the agent uses inventory_agent/inventory_catalog.json.
    # A valid product name from EITHER catalog is acceptable.
    catalog_paths = [
        repo_root / "data" / "inventory_catalog.json",
        repo_root / "inventory_agent" / "inventory_catalog.json",
    ]

    valid_names = set()
    categories = ["beer_cost", "wine_cost", "liquor_cost", "n_a_beverage_cost", "grocery_and_dry_goods"]

    for catalog_path in catalog_paths:
        if not catalog_path.exists():
            continue
        with open(catalog_path) as f:
            catalog = json.load(f)
        for cat in categories:
            if cat in catalog:
                for product in catalog[cat]:
                    # Handle both "item" and "name" field formats across catalog versions
                    name = product.get("item") or product.get("name")
                    if name:
                        valid_names.add(name)

    # Manual mapping targets are also valid (they point to catalog names,
    # but some may use slight variations — include them for completeness)
    for mapping_file in ["bar_item_mappings.json", "food_item_mappings.json"]:
        mapping_path = repo_root / "inventory_agent" / mapping_file
        if mapping_path.exists():
            with open(mapping_path) as f:
                mapping_data = json.load(f)
            for target_name in mapping_data.get("mappings", {}).values():
                valid_names.add(target_name)

    return valid_names
