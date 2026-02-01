# CoCounsel Plan Updates - January 2026

**Date**: January 27, 2026
**Status**: Phase 1 Complete (with critical lessons learned)
**Commits**: 6 commits on main branch (73c9d89, d3408a8, 36f5e21, 4d77cc9, 6327c67, 6aabb84, 12e493d)

---

## 🚨 CRITICAL UPDATE: SEARCH_FIRST Protocol

### New Step 0 Added to Safety Protocols

**BEFORE ANY CODE CHANGES - SEARCH THE CODEBASE FIRST**

```markdown
🚨 SAFETY PROTOCOLS (Apply to All Phases)

Step 0: MANDATORY CODEBASE SEARCH (NEW - Added Jan 27, 2026)

**READ THIS FILE FIRST: `SEARCH_FIRST.md`**

This protocol was created after a critical incident in Phase 1.4 where grounding rules
were added that CONTRADICTED existing canonical policies because the codebase wasn't
searched first.

**The Cardinal Rule:**
NEVER write code, prompts, or documentation without first searching the codebase for
existing implementations, policies, and specifications.

**Required Searches Before ANY Change:**

1. **Search for existing implementations:**
   ```bash
   grep -r "feature_name" --include="*.py" --include="*.md"
   ```

2. **Check workflow specs:**
   ```bash
   ls workflow_specs/
   cat workflow_specs/[RELEVANT_SPEC]/[SPEC_FILE]
   ```

3. **Check brain files:**
   ```bash
   ls docs/brain/
   grep -r "topic" docs/brain/
   ```

4. **Check existing prompts:**
   ```bash
   grep -r "topic" transrouter/src/prompts/
   ```

5. **Check agent implementations:**
   ```bash
   ls transrouter/src/agents/
   ```

**The "I've Read Everything" Checklist:**

Before submitting ANY code change that touches business logic, prompts, or policies:

- [ ] I have read the complete workflow spec for this domain
- [ ] I have searched and read all relevant brain files
- [ ] I have read the ENTIRE existing prompt file (not skimmed)
- [ ] I have searched for existing implementations of this feature
- [ ] I have verified my changes do NOT contradict existing policies
- [ ] I can cite specific files/line numbers that support my changes

**If you cannot check ALL boxes, DO NOT PROCEED.**

**Consequences of Violating This:**
1. Wastes the user's time (explaining things that are documented)
2. Breaks trust (shows you're not thorough)
3. Risks production bugs (contradicting existing logic)
4. Requires rollback (wasted effort)

---

Step 1: Backup Current State
...
```

---

## ✅ Phase 1: COMPLETED (Jan 27, 2026)

**Status**: ✅ Complete (with fixes)
**Timeline**: 1 day (accelerated from planned 5 days)
**Risk Level**: MEDIUM → HIGH (due to critical incident, then resolved)

### What Was Implemented

#### Phase 1.1: Clarification Schemas ✅
**Commit**: `73c9d89`
**Files Modified**:
- `transrouter/src/schemas.py` - Added 5 Pydantic models
- `tests/unit/test_schemas.py` - NEW - 12 unit tests
- `tests/unit/__init__.py` - NEW

**Models Added**:
- `QuestionType` (enum)
- `ClarificationQuestion` (Pydantic model)
- `ClarificationResponse` (Pydantic model)
- `ConversationState` (Pydantic model)
- `ParseResult` (Pydantic model - extended existing)

#### Phase 1.2: Multi-Turn Logic ✅
**Commit**: `d3408a8`
**Files Modified**:
- `transrouter/src/conversation_manager.py` - NEW - State persistence to disk
- `transrouter/src/agents/payroll_agent.py` - Added multi-turn methods

**Methods Added**:
- `parse_with_clarification()` - Main multi-turn entry point
- `detect_missing_data()` - Detects missing/ambiguous data
- `_incorporate_clarifications()` - Enriches transcript with answers

**Key Features**:
- Conversation state persisted to `~/mise-core/mise_app/data/conversations/`
- Max 5 iterations per conversation
- JSON file format: `{conversation_id}.json`

#### Phase 1.3: Clarification UI ✅
**Commit**: `36f5e21`
**Files Modified**:
- `mise_app/templates/clarification.html` - NEW - Question form UI
- `mise_app/routes/recording.py` - Added clarification routes

**Routes Added**:
- `GET /payroll/period/{period_id}/clarify/{conversation_id}` - Show questions
- `POST /payroll/period/{period_id}/clarify/{conversation_id}/submit` - Submit answers

**UX Changes**:
- If parsing needs clarification → redirect to clarification page
- Manager answers questions in form
- Submit → resume parsing with answers
- May require multiple rounds (up to 5)

#### Phase 1.4: Grounding Rules ✅ (with critical fix)
**Initial Commit**: `4d77cc9` (CONTAINED ERROR)
**Fix Commits**: `6327c67`, `6aabb84`
**Files Modified**:
- `transrouter/src/prompts/payroll_prompt.py` - Added grounding rules

**CRITICAL INCIDENT - What Went Wrong**:

**The Mistake**: Added grounding rule "DO NOT assume typical hours" which CONTRADICTED existing canonical policy "If hours not mentioned, use standard shift duration"

**Root Cause**: Did not read brain files (`docs/brain/011326__lpm-shift-hours.md`) or full prompt before making changes. Violated the search-first principle.

**User Feedback** (verbatim):
> "I'm confused, I thought we had a rule that, if a server's hours weren't mentioned, it was assumed they worked the full shift?"
>
> "Use our operating hours, which are IN MY CODEBASE to figure this out. You should NOT be asking me questions like this."
>
> "Check my damn workflow specs/brain files before asking me questions like this!"
>
> **"This can never happen again."**

**The Fix**:
Rewrote grounding rules to clearly distinguish:
- **✅ CANONICAL POLICY (from workflow specs/brain) → ALWAYS USE**
  - Standard shift durations (AM = 6.5hr, PM = varies)
  - Tipout percentages (utility = 5%, busser = 3%, expo = 1%)
  - Tip pooling default rule
  - Operating hours
  - Employee roster
- **❌ HISTORICAL PATTERNS (from past transcripts) → NEVER ASSUME**
  - "Austin usually works 6 hours"
  - "Fridays usually have tip pool"
  - "Ryan is usually utility"

#### Phase 1.5: SEARCH_FIRST Protocol ✅
**Commit**: `12e493d`
**Files Created**:
- `SEARCH_FIRST.md` - NEW - Mandatory search protocol
- `CLAUDE.md` - Updated to reference SEARCH_FIRST prominently

**Purpose**: Prevent future incidents where code changes contradict existing policies

**Key Sections**:
- The Cardinal Rule
- What Just Happened (documents the Phase 1.4 incident)
- Before ANY Change, You MUST Search
- Specific Searches Required by Domain
- The "I've Read Everything" Checklist
- User's Explicit Instruction (verbatim quotes)

---

## 📊 Phase 1 Post-Mortem

### Timeline
- **Planned**: 5 days (Week 1)
- **Actual**: 1 day (January 27, 2026)
- **Acceleration Factor**: 5x faster than planned

### Success Metrics
- ✅ Multi-turn clarification system implemented
- ✅ Conversation state persistence working
- ✅ UI routes functional
- ✅ Grounding rules established (after fix)
- ✅ 12 unit tests passing
- ✅ 6 commits on main branch

### Critical Lessons Learned

#### 1. **The "Confident Wrong" Problem Applies to Claude Too**
The same problem we're trying to prevent in Mise (LLM inventing data) happened during development. I assumed grounding rules based on general knowledge instead of reading the actual documented policies.

#### 2. **SEARCH_FIRST is Non-Negotiable**
Created mandatory protocol file after incident. This must be referenced in EVERY phase going forward.

#### 3. **Canonical Policy vs Historical Patterns**
Critical distinction that wasn't clear until the incident:
- Canonical policies (from workflow specs) = SOURCE OF TRUTH
- Historical patterns (from past data) = NEVER USE FOR ASSUMPTIONS

#### 4. **User Feedback is Gold**
The incident happened because of a real use case (NotebookLM playback). User caught the error immediately. This validates the importance of the clarification system we're building.

### What Worked Well
- ✅ Pydantic models caught type errors early
- ✅ Conversation persistence to disk (simple JSON) works great
- ✅ Multi-turn flow conceptually sound
- ✅ User caught the error before it went to production

### What Needs Improvement
- ❌ Need better checklist/gate before changing prompts
- ❌ Need automated tests for grounding rules
- ❌ Need to integrate SEARCH_FIRST into every phase

### Impact on Future Phases

**All subsequent phases now require Step 0:**

```markdown
📝 Phase X.Y: [Task Name]

Step 0: MANDATORY CODEBASE SEARCH (5-10 minutes)

Before writing ANY code:
1. Read SEARCH_FIRST.md completely
2. Search workflow specs for this domain
3. Search docs/brain/ for relevant policies
4. Search existing prompts
5. Search existing agent code
6. Complete the "I've Read Everything" checklist
7. Only then proceed to implementation

If you skip this step, you WILL introduce bugs.
```

---

## 📋 Updated Phase Status

### ✅ Phase 1: Clarification System (COMPLETE)
- Status: ✅ Complete (Jan 27, 2026)
- Commits: 6 (including fixes)
- Duration: 1 day (planned: 5 days)
- Risk: Medium → High → Resolved
- Lesson: SEARCH_FIRST protocol created

### 📋 Phase 2: Skills Architecture (PENDING)
- Status: ⏳ Not Started
- Prerequisites: Phase 1 ✅
- Estimated Duration: 5 days
- **NEW REQUIREMENT**: Must complete Step 0 (SEARCH_FIRST) before each sub-phase

### 📋 Phase 3: Grounding Enforcement (PENDING)
- Status: ⏳ Not Started
- Prerequisites: Phase 1 ✅
- Estimated Duration: 5 days
- **NEW REQUIREMENT**: Must validate against Phase 1.4 incident

### 📋 Phase 4: Regression Tests (PENDING)
- Status: ⏳ Not Started
- Prerequisites: Phases 1-3 ✅
- Estimated Duration: 5 days
- **NEW REQUIREMENT**: Add test for Phase 1.4 incident scenario

### 📋 Phase 5: Model Routing (PENDING)
- Status: ⏳ Not Started
- Prerequisites: Phases 1-4 ✅
- Estimated Duration: 3 days

### 📋 Phase 6: Conflict Resolution (PENDING)
- Status: ⏳ Not Started
- Prerequisites: Phases 1-5 ✅
- Estimated Duration: 3 days

### 📋 Phase 7: Instrumentation (PENDING)
- Status: ⏳ Not Started
- Prerequisites: Phases 1-6 ✅
- Estimated Duration: 2 days

### 📋 Phase 8: Enterprise Hardening (PENDING)
- Status: ⏳ Not Started
- Prerequisites: Phases 1-7 ✅
- Estimated Duration: 5 days

---

## 🔄 Updated Timeline

### Original Plan
- **Total Duration**: 4 weeks (20 working days)
- **Phase 1**: Week 1 (5 days)
- **Phases 2-8**: Weeks 2-4 (15 days)

### Revised Estimate (After Phase 1)
- **Total Duration**: ~3.5 weeks (17-18 working days)
- **Phase 1**: ✅ 1 day (actual)
- **Time Saved**: 4 days
- **Buffer Added**: 2 days for SEARCH_FIRST compliance in each phase
- **Remaining**: ~16-17 days for Phases 2-8

### Risk Assessment Update
- **Original Risk**: MEDIUM
- **Updated Risk**: MEDIUM-LOW
  - **Reduced**: Fast Phase 1 completion, good test coverage
  - **Increased**: Need SEARCH_FIRST compliance adds process overhead
  - **Net**: Slightly lower risk due to learned lessons

---

## 📝 Key Files Created/Modified Summary

### New Files (Phase 1)
1. `transrouter/src/conversation_manager.py` (201 lines)
2. `mise_app/templates/clarification.html` (HTML template)
3. `tests/unit/test_schemas.py` (12 tests)
4. `tests/unit/__init__.py` (empty)
5. `SEARCH_FIRST.md` (187 lines)
6. `fundraising/CoCounsel_Improvements_Guide.md` (8,000 words - for NotebookLM)

### Modified Files (Phase 1)
1. `transrouter/src/schemas.py` (+150 lines)
2. `transrouter/src/agents/payroll_agent.py` (+200 lines)
3. `transrouter/src/prompts/payroll_prompt.py` (+100 lines, then fixed)
4. `mise_app/routes/recording.py` (+80 lines)
5. `CLAUDE.md` (added SEARCH_FIRST reference)

### Commits Timeline
```
73c9d89 - feat(clarification): Add schemas for multi-turn conversation
d3408a8 - feat(clarification): Add multi-turn conversation logic to PayrollAgent
36f5e21 - feat(clarification): Add UI routes and templates
4d77cc9 - feat(grounding): Add grounding rules to payroll prompt [CONTAINS ERROR]
6327c67 - fix(grounding): Fix grounding rules to match canonical policy
6aabb84 - fix(payroll): Fix misleading TODOs in detect_missing_data
12e493d - docs(protocol): Add SEARCH_FIRST mandatory protocol
```

---

## 🎯 Next Steps

### Immediate (Before Phase 2)
1. ✅ Document Phase 1 completion (this file)
2. ⏳ Generate PDF of CoCounsel Improvements Guide (delegated to ccw5)
3. ⏳ Validate Phase 1 in production (test with real audio files)
4. ⏳ Update master plan with SEARCH_FIRST in all phases

### Phase 2 Preparation
1. **Step 0**: Read SEARCH_FIRST.md
2. Search for existing "skills" or "registry" patterns in codebase
3. Search docs/brain/ for architectural guidance
4. Search workflow specs for skills-related requirements
5. Read existing agent implementations completely
6. Complete checklist
7. Then proceed with Phase 2.1

---

## 📚 References

**Key Documentation**:
- `SEARCH_FIRST.md` - Mandatory search protocol
- `CLAUDE.md` - Initialization file (references SEARCH_FIRST)
- `fundraising/CoCounsel_Improvements_Guide.md` - Plain English guide
- `~/.claude/plans/declarative-strolling-canyon.md` - Master plan (8,866 lines)

**Key Code**:
- `transrouter/src/schemas.py` - Clarification models
- `transrouter/src/conversation_manager.py` - State persistence
- `transrouter/src/agents/payroll_agent.py` - Multi-turn logic
- `mise_app/routes/recording.py` - Clarification routes

**Tests**:
- `tests/unit/test_schemas.py` - 12 unit tests

---

## 🔍 Incident Report: Phase 1.4 Grounding Rules

**Date**: January 27, 2026
**Severity**: High (contradiction of canonical policy)
**Status**: Resolved
**Root Cause**: Failure to search codebase before making changes

### What Happened
1. I added grounding rules to payroll prompt
2. Rule stated: "DO NOT assume typical hours"
3. User listened to NotebookLM playback and questioned this
4. Revealed: Existing canonical policy says "If hours not mentioned, use standard shift duration"
5. My new rule CONTRADICTED existing documented policy

### Why It Happened
- Did not read `docs/brain/011326__lpm-shift-hours.md`
- Did not read full existing payroll prompt
- Relied on general knowledge instead of codebase as source of truth
- Exactly the same "confident wrong" problem we're trying to prevent in Mise

### How It Was Fixed
1. **Immediate**: User pointed out the contradiction
2. **Short-term**: Rewrote grounding rules to distinguish canonical vs historical
3. **Long-term**: Created SEARCH_FIRST.md mandatory protocol

### Prevention Measures
1. ✅ `SEARCH_FIRST.md` created and committed
2. ✅ `CLAUDE.md` updated to reference it prominently
3. ⏳ All future phases require Step 0 (search first)
4. ⏳ Add regression test for this scenario

### User's Words (Verbatim)
> "Check my damn workflow specs/brain files before asking me questions like this!"
>
> **"This can never happen again."**

---

**End of Phase 1 Update Document**

This document should be referenced alongside the master plan at:
`~/.claude/plans/declarative-strolling-canyon.md`
