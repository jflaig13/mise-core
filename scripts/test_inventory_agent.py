#!/usr/bin/env python3
"""Test the InventoryAgent with a real transcript."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from transrouter.src.agents.inventory_agent import InventoryAgent

def main():
    """Test InventoryAgent with real transcript."""

    # Read the real inventory transcript
    transcript_path = project_root / "inventory_agent" / "transcripts" / "113025_Inventory.txt"

    if not transcript_path.exists():
        print(f"❌ Transcript not found: {transcript_path}")
        return 1

    with transcript_path.open("r") as f:
        transcript = f.read()

    print("📋 Testing InventoryAgent with real transcript")
    print(f"   Transcript: {transcript_path.name} ({len(transcript)} chars)\n")

    # Create agent and parse
    agent = InventoryAgent()

    print("🤖 Parsing transcript (calling Claude API)...\n")

    result = agent.parse_transcript(
        transcript=transcript,
        category="bar",
        area="bar inventory"
    )

    # Check result
    if result["status"] == "success":
        print("✅ SUCCESS\n")

        inventory = result["inventory_json"]
        print(f"Category: {inventory.get('category')}")
        print(f"Area: {inventory.get('area', 'N/A')}")
        print(f"Items: {len(inventory.get('items', []))}")

        if inventory.get("counted_by"):
            print(f"Counted by: {inventory['counted_by']}")

        print("\nFirst 5 items:")
        for idx, item in enumerate(inventory.get("items", [])[:5]):
            product_name = item.get("product_name", "Unknown")
            quantity = item.get("quantity", "?")
            unit = item.get("unit", "?")
            notes = item.get("notes", "")

            print(f"  {idx+1}. {product_name}")
            print(f"     Quantity: {quantity} {unit}")
            if notes:
                print(f"     Notes: {notes}")

        # Show usage
        usage = result.get("usage", {})
        print(f"\nToken usage:")
        print(f"  Input:  {usage.get('input_tokens', 0)}")
        print(f"  Output: {usage.get('output_tokens', 0)}")

        return 0

    else:
        print("❌ FAILED\n")
        print(f"Error: {result.get('error')}")
        print(f"\nRaw response:\n{result.get('raw_response', 'N/A')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
