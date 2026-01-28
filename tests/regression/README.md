# Mise Regression Test Suite

## Purpose

This regression test suite ensures Mise maintains quality and correctness across model changes, code updates, and new features. Inspired by CoCounsel's approach, these tests focus on **preventing "confident wrong" answers** that could damage trust, cause financial errors, or lead to staff disputes.

## Philosophy (from CoCounsel Learnings)

### The "QAnon Shaman" Problem
**Never assume what's not in the record.**

If Mise "knows" that:
- "Tucker usually works 6 hours"
- "Emily usually closes"
- "Tip pool is usually on"

But it's not in the shift transcript → **Mise must not assume it.**

**Grounding rule:** If it impacts money, it must be supported by explicit evidence.

### Test Categories

1. **Easy Cases** - Baseline functionality, should always pass
2. **Edge Cases** - Missing data, weird phrasing, Whisper errors
3. **Grounding Tests** - Ensure Mise doesn't hallucinate or assume
4. **Clarification Tests** - Mise should ask, not guess
5. **Source-of-Truth Conflicts** - Transcript vs Toast vs Schedule
6. **Refusal Tests** - HR content, profanity, sensitive incidents

## Test Structure

Each test case includes:

```
tests/regression/
├── payroll/
│   ├── easy/                    # Baseline happy path
│   ├── missing_data/            # Missing clock-out, incomplete info
│   ├── parsing_edge_cases/      # Whisper errors, weird phrasing
│   ├── grounding/               # Tests that Mise doesn't assume
│   ├── clarification/           # When Mise should ask questions
│   └── source_conflicts/        # Transcript vs other sources
├── inventory/
│   ├── easy/
│   ├── missing_data/
│   └── category_b_behavior/     # Normalization edge cases
└── shared/
    └── refusal_handling/        # HR content, sensitive data
```

## Test Case Format

Each test case is a directory containing:

```
test_name/
├── README.md                    # Description, expected behavior
├── input/
│   ├── transcript.txt           # Input transcript
│   ├── audio.wav                # (optional) actual audio file
│   └── context.json             # Additional context (Toast data, etc.)
├── expected/
│   ├── approval.json            # Expected approval JSON
│   ├── clarifications.json      # Expected questions to ask
│   └── errors.json              # Expected error messages (if any)
└── validation/
    └── assertions.py            # Custom validation logic
```

## Critical Test Cases (from CoCounsel Doc)

### Payroll Skill Priority Tests

Page 6 of CoCounsel notes identifies these as essential:

1. **Easy shift** - Baseline, should always work
2. **Missing clock-out** - Should ask or use policy
3. **Tip pool opt-in partial** - When some servers pool, some don't
4. **Support staff tipout AM/PM variants** - Different phrasing
5. **Double shift phrasing** - Same person works AM and PM
6. **Weird speech / Whisper errors** - ASR mistakes
7. **Manager correction mid-sentence** - "No wait, make that..."

### Grounding Tests (Critical!)

Tests that verify Mise doesn't assume what's not in the record:

- **Assume usual hours** - If transcript doesn't say hours, don't infer
- **Assume usual role** - If not stated, don't assume server vs support
- **Assume tip pool** - If not mentioned, don't apply pool logic
- **Assume sales** - Don't infer "typical" sales numbers

## Running Tests

### Run Full Suite
```bash
pytest tests/regression/ -v
```

### Run by Category
```bash
pytest tests/regression/payroll/easy/ -v
pytest tests/regression/payroll/grounding/ -v
```

### Run Specific Test
```bash
pytest tests/regression/payroll/missing_data/test_missing_clock_out.py -v
```

## Success Criteria

A test passes when:

1. **Correct extraction** - Approval JSON matches expected structure
2. **Correct math** - Totals, tipouts calculated correctly
3. **Appropriate clarifications** - Asks when it should, doesn't when it shouldn't
4. **Grounding discipline** - Only uses info from transcript/sources
5. **Deterministic output** - Same input → same output (every time)

## Adding New Tests

When you discover a bug or edge case:

1. **Recreate the failure** - Build minimal test case
2. **Add to regression suite** - Following structure above
3. **Fix the bug** - Update code
4. **Verify test passes** - Run the specific test
5. **Run full suite** - Ensure no regressions

## Model Changes Protocol

Before swapping models (GPT-4 → Claude, Sonnet → Opus, etc.):

1. **Run full regression suite** with OLD model → baseline
2. **Run full regression suite** with NEW model → compare
3. **Document differences** - What broke? What improved?
4. **Fix critical failures** - Especially grounding and math
5. **Update prompts if needed** - Models have different quirks
6. **Re-run suite** - Verify fixes
7. **Deploy only if suite passes** - No regressions on critical tests

## Maintenance

- **Weekly**: Run full suite as part of CI
- **Before deploy**: Run full suite
- **After model changes**: Run full suite + manual spot checks
- **When adding features**: Add regression tests for new behavior

## Testing Philosophy

From CoCounsel (page 7):

> "The moat is testing infrastructure."

The regression suite is not just about catching bugs - it's about:

- **Building confidence** to ship fast
- **Enabling model upgrades** safely
- **Preventing regressions** as code changes
- **Documenting expected behavior** for new team members
- **Protecting user trust** by preventing "confident wrong" errors
