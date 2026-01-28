# Regression Test Suite - Implementation Guide

## What I've Built

Based on the CoCounsel interview notes (especially the "QAnon Shaman" grounding problem), I've created a comprehensive regression test suite framework for Mise.

### Files Created

```
tests/regression/
├── README.md                                    # Overview, philosophy, usage
├── IMPLEMENTATION_GUIDE.md                      # This file
├── payroll/
│   ├── easy/
│   │   └── test_easy_shift.py                   # Baseline happy path
│   ├── missing_data/
│   │   └── test_missing_clock_out.py            # Missing hours/data
│   ├── grounding/
│   │   └── test_no_assumptions.py               # "QAnon Shaman" tests
│   └── parsing_edge_cases/
│       └── test_whisper_errors.py               # ASR errors, robustness
```

## Test Categories Implemented

### 1. Easy / Baseline Tests (`payroll/easy/`)

**Purpose:** Verify core functionality works
**File:** `test_easy_shift.py`

Tests:
- ✓ Clean transcript parsing
- ✓ Employee name normalization
- ✓ Amount extraction
- ✓ Role assignment (server vs support)
- ✓ No unnecessary clarifications
- ✓ Deterministic output (same input → same output)

**Priority:** CRITICAL - If these fail, core system is broken

### 2. Missing Data Tests (`payroll/missing_data/`)

**Purpose:** Handle incomplete information correctly
**File:** `test_missing_clock_out.py`

Tests:
- ✓ Missing hours triggers clarification
- ✓ Partial data identifies what's missing
- ✓ Policy application (if restaurant has explicit policy)
- ✓ Export blocking when critical data missing

**Key Insight from CoCounsel:**
> "LLMs will confidently answer even when info is missing. Jake treats this as a core design constraint."

### 3. Grounding Tests (`payroll/grounding/`)

**Purpose:** Prevent "confident wrong" answers
**File:** `test_no_assumptions.py`

**THE CRITICAL TESTS - Core to Mise's trustworthiness**

Tests:
- ✓ Don't assume typical hours from patterns
- ✓ Don't assume tip pool status from history
- ✓ Don't infer roles from typical assignments
- ✓ Don't fill in sales from averages
- ✓ Don't add employees based on pairing patterns
- ✓ Source attribution for all data points
- ✓ Flag unusual patterns without auto-correcting

**The "QAnon Shaman" Problem (from CoCounsel doc, page 5):**

> "QAnon Shaman: model knows it, but it's not in the document. So it must refuse to invent it."
>
> For Mise: If Mise "knows" Tucker usually works 6 hours, but it's not in the shift record → **must not assume it.**
>
> **Grounding rule:** If it impacts money, it must be supported by explicit evidence.

### 4. Parsing Edge Cases (`payroll/parsing_edge_cases/`)

**Purpose:** Handle real-world messiness
**File:** `test_whisper_errors.py`

Tests (based on actual production errors from existing tests):
- ✓ Name mishearings ("Austin" → "lost him", "Allston")
- ✓ Punctuation errors ("mic" = "Mike")
- ✓ Full phrase amounts ("111 dollars and 12 cents")
- ✓ Trailing dots ("$120.")
- ✓ Filler words ("um", "uh", "okay")
- ✓ Background noise / partial words
- ✓ Number spacing variants
- ✓ Name pronunciation variants
- ✓ Manager self-correction ("no wait, make that...")
- ✓ Ambiguous errors → request clarification

**Key Insight from CoCounsel:**
> "Prompt engineers need high tolerance for pain. Restaurant workflows are speech-driven, interrupted, inconsistent naming, and error-prone."

## Implementation Status

### ✅ Completed
- Test suite structure designed
- Test philosophy documented (based on CoCounsel)
- 4 critical test files created with comprehensive test cases
- Test skeletons ready for integration

### 🔨 Next Steps

1. **Integrate with actual parsing functions**
   - Import `payroll_agent.parse_transcript()`
   - Import approval JSON generation
   - Import clarification logic

2. **Remove `pytest.skip()` and implement assertions**
   - Connect test inputs to actual code
   - Verify outputs match expectations

3. **Add test fixtures**
   - Mock Claude API responses
   - Mock restaurant configurations
   - Mock historical data (for grounding tests)

4. **Build test runner**
   - CI integration
   - Pre-deploy check
   - Regression report generation

5. **Expand test coverage**
   - Tip pool opt-in partial (some servers pool, some don't)
   - Support staff tipout AM/PM variants
   - Double shift phrasing (same person AM + PM)
   - Source-of-truth conflicts (transcript vs Toast vs schedule)

6. **Add inventory tests**
   - Similar structure to payroll
   - Category B behavior tests (normalization)

## How to Use (Once Integrated)

### Run all regression tests
```bash
cd ~/mise-core
pytest tests/regression/ -v
```

### Run specific category
```bash
pytest tests/regression/payroll/grounding/ -v      # Just grounding tests
pytest tests/regression/payroll/easy/ -v            # Just baseline tests
```

### Run single test file
```bash
pytest tests/regression/payroll/grounding/test_no_assumptions.py -v
```

### Run specific test function
```bash
pytest tests/regression/payroll/grounding/test_no_assumptions.py::test_no_assume_typical_hours -v
```

## Before Model Changes

From CoCounsel doc (page 6):

> "They rarely swap models for a task because prompts are tailored to model quirks. Switching means re-testing everything."

**Protocol before changing models (GPT-4 → Claude, Sonnet → Opus, etc.):**

1. ✓ Run full regression suite with OLD model → baseline
2. ✓ Run full regression suite with NEW model → compare
3. ✓ Document differences (what broke? what improved?)
4. ✓ Fix critical failures (especially grounding and math)
5. ✓ Update prompts if needed
6. ✓ Re-run suite → verify fixes
7. ✓ Deploy ONLY if suite passes

## Test Maintenance

- **Weekly:** Run full suite as part of CI
- **Before deploy:** Run full suite
- **After model changes:** Run full suite + manual spot checks
- **When bugs found:** Add regression test before fixing

## Critical Success Criteria

A test passes when:

1. ✅ **Correct extraction** - Approval JSON matches expected structure
2. ✅ **Correct math** - Totals, tipouts calculated correctly
3. ✅ **Appropriate clarifications** - Asks when it should, doesn't when it shouldn't
4. ✅ **Grounding discipline** - Only uses info from transcript/sources
5. ✅ **Deterministic output** - Same input → same output (every time)

## The Moat (from CoCounsel doc, page 7)

> "The moat is testing infrastructure."

The regression suite is not just about catching bugs - it's about:

- **Building confidence** to ship fast
- **Enabling model upgrades** safely
- **Preventing regressions** as code changes
- **Documenting expected behavior** for new team members
- **Protecting user trust** by preventing "confident wrong" errors

## Next Immediate Steps for You

1. **Review test files** - Make sure they cover the right scenarios
2. **Prioritize integration** - Which tests should connect first?
3. **Add actual test data** - Real transcripts from production
4. **Set up CI** - Run tests automatically on every commit

## Questions to Answer

- [ ] Which parsing function should tests import?
- [ ] How should clarification logic be structured?
- [ ] What format for source attribution?
- [ ] Should grounding tests use mock historical data or real?
- [ ] How to handle model-specific quirks in tests?

---

**Total Test Coverage Once Implemented:**

- 4 test files created
- ~35 individual test functions sketched out
- Covers 4 critical categories (Easy, Missing Data, Grounding, Parsing Edge Cases)
- Based directly on CoCounsel learnings + actual production errors from your codebase

This is the foundation for "CoCounsel-level maturity" for Mise.
