"""Tier 1: Inventory logic tests — no API keys needed.

Tests validation, conversion math, catalog matching, and pack multipliers.
"""

import copy
import pytest

from tests.conftest import SAMPLE_INVENTORY_JSON


# ============================================================================
# Inventory JSON Validation
# ============================================================================


class TestInventoryValidation:
    """Test InventoryAgent._validate_inventory_json()."""

    def _get_agent(self):
        from transrouter.src.agents.inventory_agent import InventoryAgent
        from unittest.mock import MagicMock
        return InventoryAgent(claude_client=MagicMock())

    def test_valid_json_passes(self):
        agent = self._get_agent()
        result = agent._validate_inventory_json(SAMPLE_INVENTORY_JSON, "bar")
        assert result is None  # None = no error

    def test_missing_category_fails(self):
        agent = self._get_agent()
        result = agent._validate_inventory_json({"items": []}, "bar")
        assert result is not None
        assert "Missing required keys" in result

    def test_missing_items_fails(self):
        agent = self._get_agent()
        result = agent._validate_inventory_json({"category": "bar"}, "bar")
        assert result is not None
        assert "Missing required keys" in result

    def test_category_mismatch_fails(self):
        agent = self._get_agent()
        data = copy.deepcopy(SAMPLE_INVENTORY_JSON)
        result = agent._validate_inventory_json(data, "kitchen")
        assert "Category mismatch" in result

    def test_item_missing_product_name_fails(self):
        agent = self._get_agent()
        data = {"category": "bar", "items": [{"quantity": 10, "unit": "bottles"}]}
        result = agent._validate_inventory_json(data, "bar")
        assert "missing product_name" in result.lower()

    def test_null_quantity_accepted(self):
        agent = self._get_agent()
        data = {
            "category": "bar",
            "items": [{"product_name": "Test", "quantity": None, "unit": "bottles"}],
        }
        result = agent._validate_inventory_json(data, "bar")
        assert result is None

    def test_invalid_quantity_type_fails(self):
        agent = self._get_agent()
        data = {
            "category": "bar",
            "items": [{"product_name": "Test", "quantity": "ten", "unit": "bottles"}],
        }
        result = agent._validate_inventory_json(data, "bar")
        assert "quantity must be a number" in result.lower()


# ============================================================================
# Pack Multiplier Extraction
# ============================================================================


class TestPackMultiplier:
    """Test _extract_pack_multiplier()."""

    def _extract(self, unit):
        from transrouter.src.agents.inventory_agent import _extract_pack_multiplier
        return _extract_pack_multiplier(unit)

    def test_four_pack(self):
        result = self._extract("4-pack")
        assert result == (4, "pack")

    def test_six_packs(self):
        result = self._extract("6-packs")
        assert result == (6, "pack")

    def test_twelve_pack(self):
        result = self._extract("12 pack")
        assert result == (12, "pack")

    def test_case_returns_none(self):
        # Cases have no assumed multiplier — case sizes vary by product
        result = self._extract("case")
        assert result is None

    def test_bottles_returns_none(self):
        result = self._extract("bottles")
        assert result is None

    def test_empty_string(self):
        result = self._extract("")
        assert result is None


# ============================================================================
# Conversion Display
# ============================================================================


class TestConversionDisplay:
    """Test _calculate_conversion_display()."""

    def _calc(self, quantity, unit, product_name, catalog=None):
        from transrouter.src.agents.inventory_agent import _calculate_conversion_display
        return _calculate_conversion_display(quantity, unit, product_name, catalog or {})

    def test_four_pack_conversion(self):
        result = self._calc(6, "4-packs", "High Rise Blueberry")
        assert result == "6 × 4 = 24 units"

    def test_cases_no_conversion(self):
        # Cases have no assumed multiplier — varies by product
        result = self._calc(2, "cases", "Coors Light")
        assert result is None

    def test_no_conversion_for_bottles(self):
        result = self._calc(3, "bottles", "Tito's")
        assert result is None

    def test_zero_quantity(self):
        result = self._calc(0, "4-packs", "Test")
        assert result is None

    def test_none_quantity(self):
        result = self._calc(None, "4-packs", "Test")
        assert result is None


# ============================================================================
# Enrichment (Conversion Fields Added to Items)
# ============================================================================


class TestEnrichment:
    """Test InventoryAgent._enrich_with_conversions()."""

    def _get_agent(self):
        from transrouter.src.agents.inventory_agent import InventoryAgent
        from unittest.mock import MagicMock
        return InventoryAgent(claude_client=MagicMock())

    def test_adds_converted_quantity_for_packs(self):
        agent = self._get_agent()
        data = copy.deepcopy(SAMPLE_INVENTORY_JSON)
        enriched = agent._enrich_with_conversions(data)

        # Find the 4-packs item (High Rise Blueberry, qty 6)
        pack_item = None
        for item in enriched["items"]:
            if "4-pack" in item.get("unit", ""):
                pack_item = item
                break

        assert pack_item is not None
        assert pack_item["converted_quantity"] == 24  # 6 × 4
        assert "conversion_display" in pack_item

    def test_no_conversion_for_plain_units(self):
        agent = self._get_agent()
        data = {
            "category": "bar",
            "items": [
                {"product_name": "Test", "quantity": 3, "unit": "bottles"},
            ],
        }
        enriched = agent._enrich_with_conversions(data)
        item = enriched["items"][0]
        assert item["converted_quantity"] == 3  # No multiplier
        assert "conversion_display" not in item


# ============================================================================
# NORMALIZATION LAW — Every item MUST match the product catalog.
# No unknown product names. No exceptions. No mercy.
# ============================================================================


class TestNormalizationLaw:
    """THE LAW: Every product_name in inventory output MUST exist in the catalog.

    If an item cannot be normalized to a known product, it has no business
    being in the output. These tests enforce that at the structural level.
    """

    def test_catalog_loads_successfully(self):
        from tests.conftest import load_valid_product_names
        valid_names = load_valid_product_names()
        assert len(valid_names) > 100, (
            f"Catalog only has {len(valid_names)} products — something is wrong with the loader"
        )

    def test_known_products_are_in_catalog(self):
        from tests.conftest import load_valid_product_names
        valid_names = load_valid_product_names()
        # These are real Papa Surf products — they MUST be in the catalog
        assert "Coors Light 12oz Can" in valid_names
        assert "Corona 12oz Can" in valid_names

    def test_fake_product_is_not_in_catalog(self):
        from tests.conftest import load_valid_product_names
        valid_names = load_valid_product_names()
        assert "Magic Unicorn IPA 16oz Tallboy" not in valid_names
        assert "Dr. Pepper Cherry Vanilla" not in valid_names

    def test_sample_inventory_items_in_catalog(self):
        """The SAMPLE_INVENTORY_JSON fixture must use real catalog names."""
        from tests.conftest import load_valid_product_names
        valid_names = load_valid_product_names()
        for item in SAMPLE_INVENTORY_JSON["items"]:
            name = item["product_name"]
            assert name in valid_names, (
                f"NORMALIZATION LAW VIOLATION: '{name}' in SAMPLE_INVENTORY_JSON "
                f"is not in the product catalog. Fix the fixture or the catalog."
            )

    def test_rejects_inventory_with_unknown_product(self):
        """An inventory with an unknown product_name MUST be caught."""
        from tests.conftest import load_valid_product_names
        valid_names = load_valid_product_names()
        bad_inventory = {
            "category": "bar",
            "items": [
                {"product_name": "Coors Light 12oz Can", "quantity": 7, "unit": "cans"},
                {"product_name": "Totally Fake Beer Brand XYZ", "quantity": 3, "unit": "bottles"},
            ],
        }
        violations = [
            item["product_name"] for item in bad_inventory["items"]
            if item["product_name"] not in valid_names
        ]
        assert len(violations) > 0, "Should have caught the fake product"
        assert "Totally Fake Beer Brand XYZ" in violations
