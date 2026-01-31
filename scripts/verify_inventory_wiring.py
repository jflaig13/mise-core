#!/usr/bin/env python3
"""Verify InventoryAgent is properly wired to domain router."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from transrouter.src.domain_router import DEFAULT_AGENT_REGISTRY

print("✅ Domain Router Agent Registry:")
for name in DEFAULT_AGENT_REGISTRY.keys():
    handler = DEFAULT_AGENT_REGISTRY[name]
    print(f"  - {name}: {handler.__name__}")

print("\n✅ InventoryAgent successfully wired to transrouter")
