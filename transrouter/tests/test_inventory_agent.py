"""Tests for InventoryAgent."""

import pytest
from unittest.mock import MagicMock, patch

from transrouter.src.agents.inventory_agent import (
    InventoryAgent,
    handle_inventory_request,
)


@pytest.fixture
def mock_claude_client():
    """Mock Claude client with deterministic response."""
    mock_client = MagicMock()

    # Default response: simple bar inventory
    mock_client.call.return_value.success = True
    mock_client.call.return_value.content = '''
{
  "category": "bar",
  "area": "front bar",
  "items": [
    {
      "product_name": "Bar Mix, Margarita",
      "quantity": 12,
      "unit": "bottles",
      "notes": "750ml Stirrings brand"
    },
    {
      "product_name": "Coors Light 12oz Can",
      "quantity": 0.5,
      "unit": "cases",
      "notes": "Approximate"
    }
  ],
  "counted_by": "Jonathan",
  "timestamp": "2026-01-30T14:30:00Z"
}
'''
    mock_client.call.return_value.json_data = {
        "category": "bar",
        "area": "front bar",
        "items": [
            {
                "product_name": "Bar Mix, Margarita",
                "quantity": 12,
                "unit": "bottles",
                "notes": "750ml Stirrings brand",
            },
            {
                "product_name": "Coors Light 12oz Can",
                "quantity": 0.5,
                "unit": "cases",
                "notes": "Approximate",
            },
        ],
        "counted_by": "Jonathan",
        "timestamp": "2026-01-30T14:30:00Z",
    }
    mock_client.call.return_value.usage = {"input_tokens": 500, "output_tokens": 200}

    return mock_client


def test_inventory_agent_basic(mock_claude_client):
    """Test basic inventory parsing."""
    agent = InventoryAgent(claude_client=mock_claude_client)

    result = agent.parse_transcript(
        transcript="Front bar inventory. We have 12 bottles of margarita mix. And about half a case of Coors Light cans.",
        category="bar",
        area="front bar",
    )

    assert result["status"] == "success"
    assert "inventory_json" in result

    inventory = result["inventory_json"]
    assert inventory["category"] == "bar"
    assert len(inventory["items"]) == 2
    assert inventory["items"][0]["product_name"] == "Bar Mix, Margarita"
    assert inventory["items"][1]["product_name"] == "Coors Light 12oz Can"


def test_inventory_agent_validation_error(mock_claude_client):
    """Test validation catches malformed JSON."""
    # Mock returns invalid JSON (missing category)
    mock_claude_client.call.return_value.json_data = {"items": []}

    agent = InventoryAgent(claude_client=mock_claude_client)
    result = agent.parse_transcript("Test", "bar")

    assert result["status"] == "error"
    assert "missing required keys" in result["error"].lower()


def test_inventory_agent_category_mismatch(mock_claude_client):
    """Test validation catches category mismatch."""
    # Mock returns wrong category
    mock_claude_client.call.return_value.json_data = {
        "category": "food",
        "items": [],
    }

    agent = InventoryAgent(claude_client=mock_claude_client)
    result = agent.parse_transcript("Test", "bar")

    assert result["status"] == "error"
    assert "category mismatch" in result["error"].lower()


def test_inventory_agent_api_error(mock_claude_client):
    """Test handling of Claude API error."""
    mock_claude_client.call.return_value.success = False
    mock_claude_client.call.return_value.error = "API rate limit exceeded"

    agent = InventoryAgent(claude_client=mock_claude_client)
    result = agent.parse_transcript("Test", "bar")

    assert result["status"] == "error"
    assert "API rate limit exceeded" in result["error"]


def test_handle_inventory_request(mock_claude_client):
    """Test handle_inventory_request function."""
    with patch(
        "transrouter.src.agents.inventory_agent.get_agent",
        return_value=InventoryAgent(claude_client=mock_claude_client),
    ):
        result = handle_inventory_request({
            "intent_type": "count_inventory",
            "entities": {"category": "bar", "area": "front bar"},
            "meta": {"transcript": "Front bar. 12 bottles margarita mix."},
        })

        assert result["agent"] == "inventory"
        assert result["status"] == "success"
        assert "inventory_json" in result


def test_handle_inventory_request_no_transcript():
    """Test error handling when transcript missing."""
    result = handle_inventory_request({
        "intent_type": "count_inventory",
        "entities": {},
        "meta": {},
    })

    assert result["status"] == "error"
    assert "no transcript" in result["error"].lower()


def test_inventory_agent_null_quantity(mock_claude_client):
    """Test handling of null quantities (unclear counts)."""
    mock_claude_client.call.return_value.json_data = {
        "category": "bar",
        "items": [
            {
                "product_name": "Bar Mix, Margarita",
                "quantity": None,
                "unit": "bottles",
                "notes": "Count unclear",
            }
        ],
    }

    agent = InventoryAgent(claude_client=mock_claude_client)
    result = agent.parse_transcript("Test", "bar")

    assert result["status"] == "success"
    assert result["inventory_json"]["items"][0]["quantity"] is None


def test_inventory_agent_item_validation(mock_claude_client):
    """Test validation of item structure."""
    # Missing product_name
    mock_claude_client.call.return_value.json_data = {
        "category": "bar",
        "items": [
            {
                "quantity": 10,
                "unit": "bottles",
            }
        ],
    }

    agent = InventoryAgent(claude_client=mock_claude_client)
    result = agent.parse_transcript("Test", "bar")

    assert result["status"] == "error"
    assert "missing product_name" in result["error"].lower()


def test_inventory_agent_system_prompt_caching():
    """Test that system prompts are cached per category."""
    agent = InventoryAgent()

    # First call builds prompt
    prompt1 = agent.system_prompt("bar")
    assert "bar" in prompt1.lower()

    # Second call uses cache
    prompt2 = agent.system_prompt("bar")
    assert prompt1 == prompt2

    # Different category builds new prompt
    prompt3 = agent.system_prompt("food")
    assert "food" in prompt3.lower()
    assert prompt3 != prompt1
