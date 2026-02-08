# CoCounsel Unfinished Work — What We Left Behind

**Date:** February 6, 2026
**Category:** Strategy & Playbooks
**Purpose:** Reference document so we don't lose sight of valuable CoCounsel-inspired ideas that never shipped.

---

<div class="callout important" markdown="1">
<div class="callout-title">Why This Document Exists</div>
In late January 2026, we wrote a 292KB, 8-phase master plan to transform Mise into a "CoCounsel-level" professional AI system. Phase 1 shipped. Phases 2-7 didn't. This document captures what's worth coming back to — without the 9,000 lines of planning overhead.
</div>

<div class="pull-quote">
"LLMs don't know when they don't know. If it impacts money, it must be supported by explicit evidence."
<div class="attribution">— Core CoCounsel Philosophy</div>
</div>

---

## What Shipped

### Phase 1: Multi-Turn Clarification System (~90% Complete)

The foundational idea — Mise should ask instead of guess — is live and working.

**Fully implemented:**

- Clarification schemas: `ClarificationQuestion`, `ConversationState`, `ParseResult` with `needs_clarification` status
- `ConversationManager` with disk-based persistence in `mise_app/data/conversations/`
- `parse_with_clarification()` method in PayrollAgent (lines 170-311)
- UI template (`clarification.html`) with numeric, boolean, dropdown, and text inputs
- API routes wired up in `recording.py` for GET/POST clarification flows
- `QuestionType` enum: missing_data, ambiguous, conflict, unusual_pattern, confirmation

**Still unfinished in Phase 1:**

- `detect_missing_data()` is skeletal — only checks for amounts under $1.00. The plan called for detecting: employees mentioned without amounts, physically impossible data (tips exceeding food sales), and ambiguous name resolution
- Grounding rules ("QAnon Shaman" rules) exist in regression test comments but were never added to the actual `payroll_prompt.py`

<div class="callout tip" markdown="1">
<div class="callout-title">Quick Win</div>
Finishing these two items would complete Phase 1 with relatively small effort. The infrastructure is already built — it's just the detection logic and prompt updates that are missing.
</div>

---

## What Didn't Ship

### Phase 2: Skills Architecture (0% Complete)

**What was planned:** A formal plugin system — `BaseSkill` abstract class, `SkillRegistry` for auto-discovery, `SkillExecutor` for orchestration. PayrollAgent would become PayrollSkill, InventoryAgent would become InventorySkill, and new domains would slot in cleanly.

**What exists:** Nothing. No `transrouter/src/skills/` directory. No BaseSkill. No registry.

**AGI Assessment:** Probably not needed until 3+ domain agents exist. We have 2 agents (payroll, inventory) and they work fine as standalone classes. The Claude Code skills we set up (`/payroll-specialist`, `/inventory-specialist`, etc.) handle the developer-facing version of this pattern. Phase 2 becomes worth building when we need shared lifecycle hooks for instrumentation (Phase 7) or model routing (Phase 5).

---

### Phase 3: Regression Test Suite (10% — Scaffolding Only)

**What was planned:** 30+ test functions across 4 categories, fixtures, mocks, CI integration. The "moat" — a comprehensive test suite that proves correctness and catches regressions.

**What exists:** Test files in `tests/regression/payroll/` with the right structure:

- `easy/test_easy_shift.py`
- `missing_data/test_missing_clock_out.py`
- `grounding/test_no_assumptions.py`
- `parsing_edge_cases/test_whisper_errors.py`

**The problem:** Every single test is `pytest.skip()`. Zero actual test implementations. The scaffolding is there but there's no substance.

---

### Phase 4: Grounding Enforcement (20% Complete)

**What was planned:** Add explicit grounding rules to `payroll_prompt.py` — 6 prohibited behaviors (never invent data, never assume standard hours, etc.) and 6 required behaviors (always cite source, always flag uncertainty, etc.). Include good-vs-bad examples. A/B testing script for prompt changes.

**What exists:**

- The "QAnon Shaman" philosophy is documented in `tests/regression/payroll/grounding/test_no_assumptions.py` (as comments, not as executable tests)
- The clarification system partially enforces grounding by returning `needs_clarification` instead of guessing
- But the actual prompt in `payroll_prompt.py` has no "CRITICAL GROUNDING RULES" section

**Why it matters:** This is the difference between "usually right" and "provably never confidently wrong." When money moves based on LLM output, grounding isn't optional.

---

### Phase 5: Model Routing (0% Complete)

**What was planned:** Use the right model for each phase of processing:

| Phase | Model | Why |
|-------|-------|-----|
| Transcript parsing | claude-sonnet-4 | Best quality for complex extraction |
| Missing data detection | claude-haiku-4 | Fast and cheap for simple checks |
| Total computation | Python (no LLM) | Deterministic math, zero cost |

**What exists:** Everything uses `claude-sonnet-4` for every call. The `claude_client.py` has a single default model with no routing logic.

**Cost impact:** Every missing-data check and simple validation burns sonnet tokens when haiku would do. Direct savings opportunity.

---

### Phase 6: Source-of-Truth Conflict Resolution (0% Complete)

**What was planned:** Cross-check the transcript against external data sources:

- Transcript vs. Toast POS (actual sales/tips recorded)
- Transcript vs. Schedule (who was supposed to work)
- Transcript vs. Historical data (what's normal for this shift)

Priority rules: Transcript > Toast > Schedule > Historical. Flag conflicts for manager review with evidence from each source.

**What exists:** The schema has a `CONFLICT` question type in `QuestionType` enum, but nothing detects or resolves conflicts. No Toast integration, no schedule comparison.

<div class="callout warning" markdown="1">
<div class="callout-title">This Was the Core CoCounsel Idea</div>
The entire CoCounsel philosophy boils down to: "If it impacts money, it must be supported by explicit evidence." Conflict resolution is where that philosophy meets reality — catching discrepancies before they become payroll errors.
</div>

---

### Phase 7: Instrumentation & Feedback Capture (0% Complete)

**What was planned:** Full execution logging — every API call traced with tokens used, model, duration, cost. Feedback capture after approvals. Metrics dashboard. Alerting on error rate spikes.

**What exists:** `ParseResult` has `tokens_used` and `execution_time_ms` fields, and `PayrollAgent` populates them from `response.usage`. But nothing aggregates, logs, or surfaces this data.

**Current state:** Flying blind on API costs per execution. No way to know which calls are expensive, which fail, or how much each payroll run costs.

---

## The 6 Items Worth Coming Back To

Ranked by effort-to-impact ratio:

<div class="stats-row">
<div class="stat-box">
<div class="number">1</div>
<div class="label">Grounding Rules</div>
</div>
<div class="stat-box">
<div class="number">2</div>
<div class="label">Missing Data</div>
</div>
<div class="stat-box">
<div class="number">3</div>
<div class="label">Regression Tests</div>
</div>
</div>

<div class="stats-row">
<div class="stat-box">
<div class="number">4</div>
<div class="label">Model Routing</div>
</div>
<div class="stat-box">
<div class="number">5</div>
<div class="label">Instrumentation</div>
</div>
<div class="stat-box">
<div class="number">6</div>
<div class="label">Conflict Resolution</div>
</div>
</div>

### 1. Finish Grounding Enforcement
Add "never guess when money is involved" rules directly to `payroll_prompt.py`. Small effort, high impact. The rules are already written in the plan — they just need to be added to the prompt.

### 2. Finish Missing Data Detection
Expand `detect_missing_data()` beyond the current "amounts < $1.00" check. Priority detections: employee mentioned in transcript but no amount parsed, physically impossible numbers, ambiguous employee names. Builds directly on existing code.

### 3. Regression Tests With Real Data
The scaffolding in `tests/regression/payroll/` is ready. Replace `pytest.skip()` markers with actual test implementations using real transcript data from `transcripts/`. This is the moat — proving correctness across edge cases.

### 4. Model Routing
Route cheap tasks (missing data detection, simple validation) to haiku instead of sonnet. Keep sonnet for transcript parsing. Use pure Python for deterministic math (totals, tipout calculations). Direct cost savings with no quality loss.

### 5. Instrumentation
At minimum: log token usage and execution time per API call. Write to JSONL files. Build a simple script to aggregate daily/weekly costs. Stop flying blind on API spend.

### 6. Conflict Resolution
Cross-check transcripts against Toast POS data and schedules. This is the long game — the feature that makes Mise genuinely harder to replicate. Requires Toast API integration (separate effort).

---

## Relationship to Claude Code Skills

The Claude Code skills (`/payroll-specialist`, `/inventory-specialist`, `/oracle`, etc.) are the **developer-facing** version of Phase 2's skills architecture. They help Jon work on Mise.

Phase 2 was the **product-facing** version — how Mise itself would process requests at runtime with a formal plugin system.

Same pattern (pluggable specialist modules with a common interface), different layers:

| Dimension | Claude Code Skills | Phase 2 Skills |
|-----------|-------------------|----------------|
| Audience | Developer (Jon) | Restaurant managers |
| Runtime | Development time | Production |
| Location | `.claude/agents/*.md` | `transrouter/src/skills/` |
| Interface | Prompt templates | `BaseSkill` Python class |

Phase 2 becomes worth building when either: (a) we have 3+ domain agents and need consistent patterns, or (b) we need the skills infrastructure as a foundation for instrumentation hooks or model routing.

---

## Source Plans

These plan files can be cleaned up now that this IMD captures their value:

- `~/.claude/plans/cocounsel-master-plan-original.md` — 292KB, 8-phase mega-plan. Phase 1 shipped, rest didn't.
- `~/.claude/plans/declarative-strolling-canyon.md` — Plan to edit the mega-plan (add SEARCH_FIRST to phases, expand stubs). All 4 tasks are moot since phases 2-7 never ran.

---

## Key Files Reference

For when we come back to implement any of this:

| Component | File | Status |
|-----------|------|--------|
| Clarification schemas | `transrouter/src/schemas.py` | Complete |
| Conversation manager | `transrouter/src/conversation_manager.py` | Complete |
| PayrollAgent (with clarification) | `transrouter/src/agents/payroll_agent.py` | ~90% |
| Clarification UI | `mise_app/templates/clarification.html` | Complete |
| Clarification routes | `mise_app/routes/recording.py` (lines 815-909) | Complete |
| Payroll prompt (needs grounding rules) | `transrouter/src/prompts/payroll_prompt.py` | Needs update |
| Regression test scaffolding | `tests/regression/payroll/` | Scaffolding only |
| Claude client (needs model routing) | `transrouter/src/claude_client.py` | Needs update |

---

*Mise: Everything in its place.*
