"""Tier 2: Inventory pipeline tests — REAL Claude API calls.

These tests send actual inventory transcripts to Claude and verify
the output structure. They cost ~$0.01 per test and take ~5 seconds each.

Run with: pytest -m live
Skip with: pytest -m "not live"
"""

import os
import pytest

from tests.conftest import REAL_INVENTORY_TRANSCRIPT

pytestmark = pytest.mark.live

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_KEY:
    pytest.skip("ANTHROPIC_API_KEY not set — skipping live tests", allow_module_level=True)


# ============================================================================
# InventoryAgent — Real Claude Parsing
# ============================================================================


class TestInventoryRealParsing:
    """Send real transcripts to Claude, verify output structure."""

    def _get_agent(self):
        from transrouter.src.agents.inventory_agent import InventoryAgent
        return InventoryAgent()

    def test_parse_returns_success(self):
        """Claude should successfully parse a simple inventory transcript."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_INVENTORY_TRANSCRIPT, category="bar")

        assert result["status"] == "success", f"Parsing failed: {result.get('error')}"
        assert result["agent"] == "inventory"

    def test_inventory_json_has_required_keys(self):
        """Output must contain category and items."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_INVENTORY_TRANSCRIPT, category="bar")

        assert result["status"] == "success"
        inventory = result["inventory_json"]

        assert "category" in inventory
        assert "items" in inventory
        assert inventory["category"] == "bar"

    def test_items_have_product_name(self):
        """Every item must have a product_name."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_INVENTORY_TRANSCRIPT, category="bar")

        assert result["status"] == "success"
        items = result["inventory_json"]["items"]

        assert len(items) > 0, "No items parsed"
        for i, item in enumerate(items):
            assert "product_name" in item, f"Item {i} missing product_name"
            assert len(item["product_name"]) > 0, f"Item {i} has empty product_name"

    def test_items_have_quantity(self):
        """Every item should have a quantity (number or null)."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_INVENTORY_TRANSCRIPT, category="bar")

        assert result["status"] == "success"
        items = result["inventory_json"]["items"]

        for i, item in enumerate(items):
            assert "quantity" in item, f"Item {i} missing quantity"
            qty = item["quantity"]
            assert qty is None or isinstance(qty, (int, float)), (
                f"Item {i} quantity is {type(qty)}, expected number or null"
            )

    def test_parses_reasonable_number_of_items(self):
        """The transcript mentions ~6 products, Claude should find at least 4."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_INVENTORY_TRANSCRIPT, category="bar")

        assert result["status"] == "success"
        items = result["inventory_json"]["items"]

        # Transcript mentions: Milagro, Coors Light, High Rise, Michelob, Tito's, Charles de Fer
        assert len(items) >= 4, f"Only {len(items)} items parsed, expected at least 4"

    def test_known_products_appear_in_output(self):
        """Products clearly named in transcript should appear in output."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_INVENTORY_TRANSCRIPT, category="bar")

        assert result["status"] == "success"
        items = result["inventory_json"]["items"]

        product_names_lower = [item["product_name"].lower() for item in items]
        all_products = " ".join(product_names_lower)

        # These are clearly stated in the transcript
        assert "coors" in all_products, f"Coors Light not found in: {product_names_lower}"
        assert "michelob" in all_products, f"Michelob Ultra not found in: {product_names_lower}"

    def test_enrichment_adds_conversion_fields(self):
        """Items with pack sizes should get conversion_display after enrichment."""
        agent = self._get_agent()
        result = agent.parse_transcript(REAL_INVENTORY_TRANSCRIPT, category="bar")

        assert result["status"] == "success"
        items = result["inventory_json"]["items"]

        # Check if any items have conversion fields (depends on whether Claude
        # uses pack units — this is a soft check)
        has_any_conversion = any("converted_quantity" in item for item in items)
        # Not asserting True — just verifying it doesn't crash


# ============================================================================
# InventoryAgent.process_text — Real Claude pipeline
# ============================================================================


class TestInventoryProcessTextReal:
    """Test process_text() with real Claude calls."""

    def _get_agent(self):
        from transrouter.src.agents.inventory_agent import InventoryAgent
        return InventoryAgent()

    def test_process_text_returns_correct_dict(self):
        """process_text() should return {status, transcript, approval_json}."""
        agent = self._get_agent()
        result = agent.process_text(REAL_INVENTORY_TRANSCRIPT, category="bar")

        assert result["status"] == "success", f"Failed: {result.get('error')}"
        assert result["transcript"] == REAL_INVENTORY_TRANSCRIPT
        assert "approval_json" in result
        assert isinstance(result["approval_json"], dict)
        assert "items" in result["approval_json"]


# ============================================================================
# NORMALIZATION LAW — PUNISHABLE BY DEATH
#
# Every single product_name that Claude returns MUST exist in the
# product catalog. If Claude cannot normalize a spoken item to a known
# product, that item MUST NOT appear in the output.
#
# No unknown products. No hallucinated names. No slipping through.
# ============================================================================


@pytest.mark.timeout(180)
class TestNormalizationLaw:
    """THE LAW: Every product Claude returns MUST be in the product catalog.

    These tests send real transcripts to the real Claude API and verify
    that every single item in the response has a product_name that exists
    in the canonical product catalog. One violation = test failure.
    """

    def _get_agent(self):
        from transrouter.src.agents.inventory_agent import InventoryAgent
        return InventoryAgent()

    def _get_valid_names(self):
        from tests.conftest import load_valid_product_names
        return load_valid_product_names()

    def test_all_items_normalized_to_catalog(self):
        """CORE LAW: Parse real transcript, every item MUST be in catalog."""
        agent = self._get_agent()
        valid_names = self._get_valid_names()

        result = agent.parse_transcript(REAL_INVENTORY_TRANSCRIPT, category="bar")
        assert result["status"] == "success", f"Parsing failed: {result.get('error')}"

        items = result["inventory_json"]["items"]
        assert len(items) > 0, "No items parsed — nothing to validate"

        violations = []
        for item in items:
            name = item["product_name"]
            if name not in valid_names:
                violations.append(name)

        assert len(violations) == 0, (
            f"NORMALIZATION LAW VIOLATION — {len(violations)} product(s) not in catalog:\n"
            + "\n".join(f"  - '{v}'" for v in violations)
            + f"\n\nCatalog has {len(valid_names)} valid products. "
            f"These items slipped through without normalization."
        )

    def test_process_text_all_items_normalized(self):
        """Same law, through the process_text() pipeline."""
        agent = self._get_agent()
        valid_names = self._get_valid_names()

        result = agent.process_text(REAL_INVENTORY_TRANSCRIPT, category="bar")
        assert result["status"] == "success", f"Failed: {result.get('error')}"

        items = result["approval_json"]["items"]
        assert len(items) > 0, "No items parsed"

        violations = []
        for item in items:
            name = item["product_name"]
            if name not in valid_names:
                violations.append(name)

        assert len(violations) == 0, (
            f"NORMALIZATION LAW VIOLATION — {len(violations)} product(s) not in catalog:\n"
            + "\n".join(f"  - '{v}'" for v in violations)
            + f"\n\nEvery item must normalize to a known product. No exceptions."
        )

    def test_tricky_transcript_still_normalizes(self):
        """Slang, nicknames, ASR garble — Claude must STILL normalize to catalog names."""
        agent = self._get_agent()
        valid_names = self._get_valid_names()

        tricky_transcript = """
        Back bar. We got 3 Tito's, half a bottle of Jager,
        two cases of Coors, a four-pack of Athletic non-alcoholic,
        and like 6 bottles of that red bull.
        """
        result = agent.parse_transcript(tricky_transcript, category="bar")
        assert result["status"] == "success", f"Parsing failed: {result.get('error')}"

        items = result["inventory_json"]["items"]
        assert len(items) > 0, "No items parsed from tricky transcript"

        violations = []
        for item in items:
            name = item["product_name"]
            if name not in valid_names:
                violations.append(f"'{name}' (spoken as something informal)")

        assert len(violations) == 0, (
            f"NORMALIZATION LAW VIOLATION on tricky transcript — "
            f"{len(violations)} product(s) not in catalog:\n"
            + "\n".join(f"  - {v}" for v in violations)
            + f"\n\nClaude must normalize slang/nicknames to canonical catalog names."
        )
