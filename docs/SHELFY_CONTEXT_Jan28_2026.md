# Shelfy Context - Inventory System Architecture

**Date**: January 28, 2026
**Source**: workflow_specs/SHELFY/SHELFY_Workflow_Master_DRAFT.md

---

## Critical Discovery: TWO Inventory Systems

### 1. Legacy: inventory_agent/ (Rule-Based Parser)

**Status**: WORKING (1,252 lines)
**Architecture**: Standalone CLI tool
**Tech**: Fuzzy matching + catalog, NO Claude
**Files**:
- parser.py (356 lines) - Main parser
- parse_bar_inventory.py (271 lines)
- parse_food_inventory.py (281 lines)
- catalog_loader.py (100 lines)
- inventory_catalog.json (65KB product catalog)

**Capabilities**:
- Parses transcript → structured counts
- Fuzzy name matching (handles Whisper errors)
- Quantity extraction (percentages, fractions, packs)
- Location detection (Walk-in, Back Bar, etc.)

**Integration**: NOT connected to transrouter (domain_router.py has 4-line stub)

---

### 2. Shelfy: Product UI (Storage Only)

**Status**: LITE VERSION (no parsing yet)
**Architecture**: Web UI + storage
**Tech**: Flask routes + file storage
**Files**:
- mise_app/shelfy_storage.py - Storage, date normalization, areas
- mise_app/routes/inventory.py - API + HTML routes

**Endpoints**:
- POST /inventory/record_shelfy - Record voice
- POST /inventory/approve_shelfy - Approve transcript
- GET /inventory/totals/{period_id} - View totals
- GET /inventory/shelfy/{shelfy_id} - View shelfy
- GET /inventory/areas - List areas
- GET /inventory/periods - List periods

**Current Flow**:
1. User records inventory by area (Walk-in, Back Bar, etc.)
2. Whisper transcribes audio
3. **Transcript stored RAW (line 77: "No product parsing")**
4. User approves
5. (Future: Email spreadsheet)

**TODO (line 87)**: "Inventory AI agent for parsing items/quantities"

---

## What This Means for Phase 2.4

### The Gap

**Shelfy UI**: ✅ EXISTS (can record + store)
**Parsing**: ❌ MISSING (transcripts not parsed into structured data)

**Options**:

1. **Connect legacy parser to Shelfy**
   - Wrap inventory_agent/parser.py in API
   - Call from Shelfy routes
   - Pros: Working code exists
   - Cons: Legacy architecture (no Claude, no transrouter)

2. **Build new InventoryAgent (Claude-powered)**
   - Create transrouter-native agent
   - Use Claude + catalog (like PayrollAgent)
   - Wire to domain_router
   - Call from Shelfy routes
   - Pros: Consistent with PayrollAgent pattern
   - Cons: More work, but cleaner architecture

3. **Hybrid approach**
   - Migrate legacy parser logic into new InventoryAgent
   - Use best of both (fuzzy matching + Claude reasoning)
   - Integrate with transrouter

---

## Phase 2.4 Corrected Assessment

**Original validation said**: "Phase 2.4 valuable - wrap legacy code (~2 days)"

**With Shelfy context**: Phase 2.4 is CRITICAL for PRODUCT LAUNCH

**Why**:
- Shelfy is "first product Mise will bring to market" (line 11)
- Currently in "Lite" mode (no parsing)
- Cannot deliver spreadsheets without parsing
- TODO explicitly mentions "Inventory AI agent"

**Priority**: P1 (not P2) - BLOCKS PRODUCT LAUNCH

**Recommended Approach**: Option 2 (Build new InventoryAgent)
- Aligns with transrouter architecture
- Enables multi-turn clarification (like payroll)
- Can leverage existing catalog for validation
- Consistent with CoCounsel improvements philosophy

**Effort**: ~3-4 days (not 2)
1. Day 1: Create InventoryAgent class (following PayrollAgent pattern)
2. Day 2: Integrate with Shelfy routes
3. Day 3: Test with historical transcripts
4. Day 4: Polish + edge cases

---

## Updated Priority

**Phase 2.4: Inventory Integration**
- **Old priority**: P2 (nice to have)
- **NEW priority**: P1 (blocks product launch)
- **Reason**: Shelfy cannot deliver value without parsing

**Sequence Impact**:
- Should be done AFTER regression tests (Week 2)
- But BEFORE instrumentation (critical path for product)

---

## Shelfy Context Summary

| Aspect | Status | Evidence |
|--------|--------|----------|
| UI | ✅ EXISTS | routes/inventory.py |
| Storage | ✅ EXISTS | shelfy_storage.py |
| Transcription | ✅ EXISTS | Whisper integration |
| **Parsing** | ❌ MISSING | "No product parsing (raw transcript only)" |
| Product Status | "Lite" | First product to market |
| Deliverable | ❌ BLOCKED | Cannot generate spreadsheets without parsing |

---

**Impact on Master Plan**: Phase 2.4 is NOT optional refactoring - it's CRITICAL PATH for product launch.

**For tomorrow**: Decide if Phase 2.4 moves up in priority based on product roadmap.
