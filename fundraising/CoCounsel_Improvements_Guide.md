# CoCounsel-Inspired Improvements to Mise

**A Complete Guide to Making Mise Smarter and More Reliable**

---

## Introduction: What is CoCounsel?

CoCounsel is an AI legal assistant built by Casetext (now part of Thomson Reuters). It's used by thousands of lawyers to analyze legal documents, find case law, and answer complex legal questions.

**Why does it matter for Mise?**

CoCounsel faced the same challenge Mise faces: **AI systems that handle important information (legal cases or restaurant payroll) must NEVER be "confidently wrong."**

When a lawyer asks CoCounsel about a case, it can't guess. When a manager records payroll in Mise, we can't guess either. Money is at stake.

The CoCounsel team spent years solving this problem. We're learning from their solutions.

---

## The Core Problem: "Confident Wrong"

### What "Confident Wrong" Means

Imagine you ask Mise: *"How many hours did Austin work on Monday?"*

If the audio recording didn't mention hours, Mise has three options:

1. **Guess** (using past patterns: "Austin usually works 6 hours, so probably 6") ❌ BAD
2. **Return an error** ("Cannot process - missing hours") ❌ BAD
3. **Ask you** ("I didn't hear hours mentioned. How many hours did Austin work?") ✅ GOOD

**Current Mise does #1 or #2. We're building #3.**

The CoCounsel team calls this the **"QAnon Shaman" problem**:

> If a person (like the QAnon Shaman) is famous and the AI "knows" about them, but they're NOT mentioned in the document you're analyzing, the AI must refuse to talk about them. It can't invent information.

**For Mise, this means:**
- If Tucker usually works 6 hours, but hours aren't in today's recording → **Don't assume 6**
- If Emily usually closes, but the recording doesn't say → **Don't assume she's closing**
- If tip pool is usually on Fridays, but today's recording doesn't mention it → **Don't assume it's on**

**The Golden Rule:** *If it impacts money, it must be explicitly stated or confirmed.*

---

## Current Problems with Mise

Let's be honest about what doesn't work well right now:

### Problem 1: Guessing When Data is Missing

**Example:** Manager records: *"Austin worked, made $150."*
**Missing:** How many hours?
**Current Mise:** Might use Austin's average hours from past weeks (6 hours) → Creates approval with 6 hours
**Issue:** What if Austin actually worked 8 hours this time? The guess is wrong, but Mise acted confident.

### Problem 2: No Way to Ask Questions

**Current flow:**
```
Audio → Transcribe → Parse → Approval (success or error)
```

If parsing fails, you get an error. If parsing "succeeds" but guessed wrong, you don't know until you review it.

**What we need:**
```
Audio → Transcribe → Parse → "Wait, I need clarification" → Ask questions → Manager answers → Parse again → Approval
```

### Problem 3: Can't Track Why Decisions Were Made

**Example:** Manager reports a bug: "Mise calculated Ryan's tipout wrong."

**Current situation:** We can't replay what happened. No log of:
- What the transcript said
- What decisions Mise made
- Why it chose those numbers
- Which AI model was used

**Result:** Can't reproduce the bug, can't fix it confidently.

### Problem 4: Monolithic Code Structure

Right now, PayrollAgent is one big class that does everything. This makes it:
- Hard to test individual pieces
- Hard to add new features (like Inventory, Ordering, Scheduling)
- Hard to swap AI models without breaking everything

---

## Overview: 8 Phases of Improvement

We're building 8 major improvements, structured in phases. Here's the high-level map:

| Phase | Name | What It Does | Priority |
|-------|------|--------------|----------|
| **1** | Clarification System | Mise asks questions when data is missing | Critical |
| **2** | Skills Architecture | Reorganize code so each task (Payroll, Inventory) is a "skill" | High |
| **3** | Grounding Enforcement | Force Mise to only use information it actually received | Critical |
| **4** | Regression Test Suite | Comprehensive tests to catch bugs before they reach you | High |
| **5** | Model Routing | Use cheaper/faster AI models for simple tasks | Medium |
| **6** | Conflict Resolution | Handle disagreements between data sources (transcript vs Toast vs schedule) | High |
| **7** | Instrumentation | Log everything so bugs can be reproduced and fixed | Medium |
| **8** | Enterprise Hardening | Polish for scale (multi-restaurant, backups, monitoring) | Medium |

---

## Phase 1: Clarification System (Week 1)

### The Goal
When Mise doesn't have complete information, it should **ask you** instead of guessing.

### How It Works (Simple Breakdown)

**Before:**
```
1. You record audio: "Austin worked"
2. Mise parses it
3. Mise guesses 6 hours (because Austin usually works 6)
4. Approval appears (possibly wrong)
```

**After:**
```
1. You record audio: "Austin worked"
2. Mise parses it
3. Mise detects: "Wait, no hours mentioned"
4. Mise shows you a question: "How many hours did Austin work?"
5. You type: "6"
6. Mise continues parsing with your answer
7. Approval appears (correct)
```

### What We're Building

**Four major pieces:**

#### 1.1: Question & Answer Data Structures

Create structured formats for:
- **Questions Mise asks:** "How many hours did Austin work?" (includes context, field name, suggested answer if applicable)
- **Answers you provide:** "6" (includes your confidence level, notes)
- **Conversation tracking:** Keep track of all questions and answers in one place

**Plain English:** Think of this like designing a form. When Mise has a question, it needs to know how to structure it clearly. When you answer, Mise needs to know how to save and use your answer.

#### 1.2: Multi-Turn Conversation Logic

Update PayrollAgent to support **back-and-forth conversation** instead of one-shot parsing.

**Plain English:** Right now, Mise takes one swing at parsing your audio. With multi-turn logic, Mise can:
1. Take a first swing
2. If something's missing, pause and ask
3. Take your answer
4. Take another swing with the new information
5. Repeat until complete

It's like having a conversation instead of a monologue.

#### 1.3: User Interface for Questions

Add a clarification page in the Mise web app where:
- You see questions Mise needs answered
- You can type or select answers
- You can add notes or context
- You submit answers and Mise continues

**Plain English:** Right now, when you upload audio, you either get an approval or an error. With this, you might get a "Clarification Needed" page with a form to fill out.

#### 1.4: Update Prompts with Grounding Rules

Rewrite the instructions we give to the AI to **explicitly forbid guessing**.

**Example instruction we'll add:**
> "CRITICAL GROUNDING RULES: You MUST NOT assume or invent any data that is not explicitly in the transcript. If an employee is mentioned but their hours are not stated, include that in 'clarifications_needed'. If it impacts money, it must be explicitly in the transcript."

**Plain English:** We're rewriting the AI's "job description" to say "when in doubt, ask—never guess."

---

## Phase 2: Skills Architecture (Week 2)

### The Goal
Reorganize Mise's code so each major task (Payroll, Inventory, Ordering, etc.) is a separate, testable "skill."

### Why This Matters

**Right now:** PayrollAgent is a giant class with 500+ lines. Adding Inventory means copying that pattern. Adding Ordering means copying again. If we want to improve one, we have to remember to improve all.

**After Skills:** Each task follows the same pattern:
- Has inputs (transcript, restaurant ID, etc.)
- Has validation (check for missing data)
- Has clarification (ask questions if needed)
- Has output (structured JSON)
- Has tests (verify it works)

### What We're Building

#### 2.1: Base Skill Interface

Create a "template" that all skills must follow.

**Think of it like a recipe card:** Every recipe has the same structure:
- **Ingredients** (inputs)
- **Steps** (execution)
- **Result** (output)
- **Notes** (validation)

Every skill (Payroll, Inventory, Ordering) will follow this template.

#### 2.2: Skill Registry

Create a "registry" (a list) of all available skills.

**Plain English:** When a request comes in, Mise looks up "which skill handles this?" in the registry, then runs that skill.

Benefits:
- Easy to add new skills (just register them)
- Easy to disable skills (unregister)
- Easy to test skills in isolation

#### 2.3: Refactor Payroll as a Skill

Take the existing PayrollAgent code and restructure it to follow the new skill template.

**Plain English:** We're not rewriting Payroll from scratch—we're reorganizing the existing code to fit the new pattern. Like cleaning your closet: same clothes, better organization.

#### 2.4: Create Inventory Skill Stub

Build a skeleton for Inventory (not full implementation yet, just the structure).

**Plain English:** Create an empty "Inventory Skill" that follows the template, so we know where to add inventory logic later.

---

## Phase 3: Grounding Enforcement (Week 1, Parallel)

### The Goal
Create automatic checks to verify Mise **only uses information it actually received**.

### How It Works

**After Mise generates an approval JSON**, we run it through a "grounding validator":

```
For each employee in the approval:
  1. Check: Is this employee's name in the roster? (Not invented)
  2. Check: Is their amount mentioned near their name in the transcript?
  3. Check: Are their hours mentioned (or answered in clarification)?

If any check fails → Flag as "grounding violation" → Require manager review
```

### What We're Building

#### 3.1: Grounding Validator

A "fact-checker" that runs after parsing.

**Plain English:** After Mise creates an approval, this validator asks: "Can you prove every number came from the transcript or a manager clarification?" If not, it flags the approval for review.

#### 3.2: Source Attribution

Add "receipts" to every data point.

**Example:**
```json
{
  "Austin Kelley": {
    "amount": 150.00,
    "source": "transcript_line_3",
    "hours": 6.0,
    "source": "manager_clarification_q001"
  }
}
```

**Plain English:** Every number now comes with a "where did this come from?" tag. Makes it easy to audit.

#### 3.3: Updated Prompts

Add explicit instructions to the AI:
- "Don't assume typical hours"
- "Don't infer tip pool from patterns"
- "Don't fill in missing data from historical averages"

**Plain English:** We're updating the AI's "rules of the road" to be much stricter about sources.

---

## Phase 4: Regression Test Suite (Week 3)

### The Goal
Build comprehensive automated tests to catch bugs **before** they reach production.

### What We're Building

**Test Categories:**

#### 4.1: Easy Tests (Baseline)
Simple, happy-path scenarios:
- *"Austin $150, Brooke $140"* → Should parse correctly
- No missing data, no edge cases
- **Purpose:** Verify core functionality works

#### 4.2: Missing Data Tests
Scenarios with incomplete information:
- *"Austin worked"* (no amount) → Should ask for amount
- *"Brooke $150"* (no hours) → Should ask for hours
- **Purpose:** Verify clarification system works

#### 4.3: Grounding Tests
Scenarios designed to catch "confident wrong" errors:
- Transcript mentions Austin but not Brooke → Should NOT add Brooke (even if she usually works with Austin)
- Hours not mentioned → Should NOT use Austin's average hours
- **Purpose:** Verify grounding enforcement works

#### 4.4: Parsing Edge Cases
Real-world messiness:
- *"Austin $12345"* (no decimal) → Should parse as $123.45
- *"lost him $150"* (Whisper misheard "Austin") → Should normalize to Austin
- *"Kevin 111 dollars and 12 cents"* → Should parse as $111.12
- **Purpose:** Verify robustness

### Integration Status

**Current:** 30 test functions exist, all with `pytest.skip()` (placeholders)
**Phase 4:** Remove skips, integrate with actual code, add mocks, run in CI

**Plain English:** We've written the test outlines. Now we connect them to the real code and make them run automatically on every change.

---

## Phase 5: Model Routing (Week 4)

### The Goal
Use the right AI model for each task to optimize cost and speed.

### Why This Matters

**Current:** We use Claude Sonnet for everything. It's powerful but expensive (~$3 per 1M input tokens).

**Reality:** Not every task needs the most powerful model.

**Example Task Breakdown:**
- **Parse transcript** → Sonnet (complex, needs good reasoning) - $$$
- **Verify hours are present** → Haiku (simple check) - $
- **Compute tipout totals** → No AI needed (deterministic math) - Free
- **Generate summary text** → Sonnet (better writing) - $$$
- **Ask clarification question** → Haiku (simple templating) - $

**Cost Savings:** Using Haiku for simple tasks could cut inference costs by 50-70%.

### What We're Building

#### 5.1: Model Router

A decision maker that picks the best model for each subtask.

**Plain English:** Before each AI call, Mise asks: "What kind of task is this?" then selects:
- **Haiku** for fast, simple tasks
- **Sonnet** for complex reasoning
- **No model** for deterministic math

#### 5.2: Task-Based Execution

Break PayrollSkill into subtasks:
1. Parse transcript (Sonnet)
2. Verify completeness (Haiku)
3. Compute totals (Python)
4. Generate summary (Sonnet)

Each subtask uses the appropriate model.

**Plain English:** Instead of one big "do everything" AI call, we break it into smaller calls, each using the right tool.

---

## Phase 6: Conflict Resolution (Week 4)

### The Goal
Handle situations where different data sources disagree.

### The Problem

**Example Scenario:**
- **Transcript says:** Austin worked 6 hours
- **Toast report says:** Austin clocked in at 5:00 PM, clocked out at 11:30 PM (6.5 hours)
- **Schedule says:** Austin was scheduled 5:00 PM - 11:00 PM (6 hours)

**Which is correct?** We need rules.

### What We're Building

#### 6.1: Source Priority Rules

Define which sources are most trustworthy:

| Priority | Source | Why |
|----------|--------|-----|
| 1 (Highest) | Manual Override | Manager explicitly entered it |
| 2 | Manager Approval | Manager confirmed in approval step |
| 3 | Transcript | Manager spoke it |
| 4 | Toast Report | POS system recorded it |
| 5 | Schedule | What was planned (not necessarily what happened) |
| 6 (Lowest) | Historical Pattern | Past behavior (don't trust for current data) |

#### 6.2: Conflict Detector

When sources disagree, flag it for manager review.

**Plain English:** If the transcript says 6 hours but Toast says 6.5 hours, Mise shows you both and asks "Which is correct?"

#### 6.3: Integration with Clarification System

Conflicts become clarification questions:

> "Transcript says Austin worked 6 hours, but Toast shows 6.5 hours. Which should I use?"

**Plain English:** Instead of silently picking one, Mise asks you to resolve the conflict.

---

## Phase 7: Instrumentation & Feedback (Week 4)

### The Goal
Log everything so bugs can be reproduced and fixed.

### The Problem

**Current:** When something goes wrong, we have:
- The approval JSON (maybe)
- No record of what the AI "thought"
- No record of intermediate steps
- No way to replay the execution

**Result:** Hard to debug, hard to learn from mistakes.

### What We're Building

#### 7.1: Execution Logger

Save a complete trace of every payroll parsing:
- Original audio transcript
- All AI calls made (prompts, responses, models used)
- All clarifications asked and answered
- All decisions made (and why)
- Final approval JSON
- Git commit hash (for reproducibility)

**Plain English:** A "black box recorder" for Mise. If something goes wrong, we can replay exactly what happened.

#### 7.2: "Report Problem" UI

Add a button to approvals: *"Something's wrong with this"*

When clicked:
- Loads the execution log for that approval
- Asks you: "What was wrong? What did you expect?"
- Saves as a bug report with full context
- **Automatically converts to a regression test**

**Plain English:** When you spot a bug, Mise makes it easy to report AND automatically prevents that bug from happening again.

---

## Phase 8: Enterprise Hardening (Bonus)

### The Goal
Production-ready polish for scale.

### What We're Building

#### 8.1: Multi-Restaurant Data Isolation
Already mostly done (Papa Surf + SoWal House). Ensure strict separation.

#### 8.2: Audit Logging
Track who did what, when (for compliance).

#### 8.3: Backup & Recovery
Automated backups, tested recovery procedures.

#### 8.4: Monitoring & Alerts
Health checks, error rate monitoring, alert on anomalies.

#### 8.5: API Rate Limiting
Don't let one restaurant's spike affect others.

---

## Key Concepts Explained Simply

### What is a "Skill"?

**Old analogy:** Mise is like a Swiss Army knife—one tool trying to do everything.
**New analogy:** Mise is like a toolbox—separate tools (Payroll, Inventory, Ordering), each designed for one job.

A "skill" is one tool in the toolbox.

### What is "Grounding"?

**Grounding** means "tied to source material."

**Grounded statement:** "Austin made $150 (transcript line 3)"
**Ungrounded statement:** "Austin probably made $150 (guessed based on pattern)"

We're enforcing grounding so Mise only makes grounded statements.

### What is a "Regression Test"?

**Definition:** A test that verifies old functionality still works after changes.

**Example:** After we add clarification logic, we run all old tests to make sure we didn't break existing payroll parsing.

**Why important:** Prevents "fix one thing, break another" scenarios.

### What is "Model Routing"?

**Routing** means "directing to the right destination."

**Analogy:** You wouldn't call a brain surgeon to check if you have a fever. You'd see a general practitioner first.

Model routing directs simple tasks to simple (cheap) models, complex tasks to complex (expensive) models.

### What is "Source-of-Truth Conflict"?

When multiple reliable sources disagree about the same fact.

**Example:** Transcript says $150, Toast says $148.50.

Both are "sources of truth," but they conflict. We need rules to resolve it (or ask the manager).

---

## What Changes for Users (You)

### Immediate Changes (After Phase 1)

**When recording payroll:**

**Before:**
- Record audio
- Wait for approval to appear
- Review approval (might have guessed data)

**After:**
- Record audio
- *Might* see: "I need clarification on 2 things"
- Answer questions
- See approval (with correct data)

**Net effect:** Slightly more interaction, but **much higher accuracy**.

### Medium-Term Changes (After Phase 2-4)

**New features:**
- Inventory skill (record inventory counts via voice)
- Ordering skill (place orders via voice)
- Better error messages ("Missing Austin's hours" vs "Parse failed")

**Reliability:**
- Fewer "confident wrong" errors
- Fewer support requests
- More trust in the system

### Long-Term Changes (After Phase 5-8)

**Performance:**
- Faster processing (model routing)
- Lower costs (cheaper models for simple tasks)

**Debugging:**
- "Report Problem" button makes bugs easy to flag
- Bugs get fixed faster (execution logs)

**Scale:**
- Ready for more restaurants
- Ready for more features
- Ready for bigger team

---

## Timeline & Risk Management

### Week-by-Week Plan

| Week | Phases | Deliverables |
|------|--------|--------------|
| 1 | Phase 1 + 3 | Clarification system + Grounding enforcement |
| 2 | Phase 2 | Skills architecture |
| 3 | Phase 4 | Regression tests fully integrated |
| 4 | Phase 5-7 | Model routing + Conflict resolution + Instrumentation |
| Bonus | Phase 8 | Enterprise hardening |

**Total: 4 weeks (20 working days)**

### Risk Management

**What could go wrong?**

1. **Breaking existing payroll parsing**
   **Mitigation:** Comprehensive tests + feature branch + gradual rollout

2. **Clarification UX feels clunky**
   **Mitigation:** Quick feedback loops, iterate on UI

3. **Model routing costs more than expected**
   **Mitigation:** Monitor costs closely, adjust routing rules

4. **Timeline slips**
   **Mitigation:** Phases are independent—can slip less critical phases (5-8) without blocking core improvements (1-4)

### Safety Protocols

**Before any code changes:**
- Create timestamped backup
- Create feature branch
- Document current behavior

**During development:**
- Test after each change
- Commit frequently with detailed messages
- Never push directly to main

**Before deployment:**
- Full test suite passes
- Manual QA completed
- Rollback procedure tested
- Gradual traffic shift (10% → 50% → 100%)

---

## Success Metrics

**How do we know this worked?**

### Phase 1 Success (Clarification)
- ✅ Zero "confident wrong" errors in payroll
- ✅ Clarification system used on ≥20% of recordings (where data is actually missing)
- ✅ Manager satisfaction: "Mise asks good questions when it needs to"

### Phase 2 Success (Skills)
- ✅ Can add Inventory skill in <2 days (proof of extensibility)
- ✅ PayrollSkill has ≥90% test coverage
- ✅ Code is easier to understand (measured by: new developer can contribute in <1 day)

### Phase 3 Success (Grounding)
- ✅ All approval JSON data points have source attribution
- ✅ Grounding validator catches ≥95% of violations in tests
- ✅ Zero production incidents of "invented data"

### Phase 4 Success (Regression Tests)
- ✅ 30+ tests fully integrated (no skips)
- ✅ Tests run in CI on every commit
- ✅ Can swap models confidently (tests verify no behavior change)

### Overall Success
- ✅ User trust increases (fewer bugs, more transparency)
- ✅ Development velocity increases (easier to add features)
- ✅ Support burden decreases (fewer "why did it do that?" questions)

---

## FAQ: Questions You Might Have

### Q: Will this break my current payroll workflow?

**A:** No. We're building on a feature branch, testing thoroughly, and rolling out gradually. Your current workflow stays the same unless you opt into the new features.

### Q: Will I have to answer questions every time I record payroll?

**A:** Only when data is genuinely missing. If your recording is complete (names, amounts, hours all mentioned), it'll work exactly like today—no questions.

### Q: What if I don't know the answer to a clarification question?

**A:** You can:
1. Skip that question (Mise will mark it as "needs follow-up")
2. Provide a partial answer with low confidence
3. Add notes ("Will check with Austin tomorrow")

### Q: Will this make Mise slower?

**A:** Slightly slower when clarifications are needed (you're answering questions). But Phase 5 (model routing) will make normal parsing **faster** (using faster models for simple tasks).

### Q: How much will this cost (API usage)?

**A:** Phase 5 (model routing) is designed to **reduce costs** by 50-70%. More AI calls, but cheaper models for simple tasks. Net effect: lower cost.

### Q: Can I test this before it goes live?

**A:** Yes. We'll deploy to a staging environment first, give you access, and you can test with real data before we roll out to production.

### Q: What if something goes wrong after deployment?

**A:** We have rollback procedures:
1. Gradual traffic shift (10% → 50% → 100%) - can stop at any point
2. One-click rollback to previous version
3. Feature flags to disable new features without redeploying

### Q: Will this work for SoWal House too?

**A:** Yes. All improvements apply to both Papa Surf and SoWal House. The skills architecture makes multi-restaurant support even better.

---

## Next Steps

### For You (Jonathan)

1. **Read this doc thoroughly**
2. **Upload to NotebookLM** (create a "CoCounsel Improvements" notebook)
3. **Ask NotebookLM questions** to deepen understanding
4. **Review Phase 1 plan** in detail (in the master plan file)
5. **Approve or request changes**

### For Us (Implementation)

1. **Create feature branch** (`feature/cocounsel-improvements`)
2. **Create backups** (code + data)
3. **Begin Phase 1.1** (Clarification Schemas)
4. **Test, commit, repeat**

### Communication

- **Daily updates** on progress
- **Ask questions anytime** (especially on critical decisions)
- **Review approvals at end of each phase** (before moving to next)

---

## Why This Matters

Mise is already helping Papa Surf save hours every week on payroll. But to scale (more restaurants, more features), we need a foundation of trust.

**Trust comes from:**
1. **Accuracy** (never confident wrong)
2. **Transparency** (show your work)
3. **Reliability** (same input → same output, every time)

These 8 phases build that foundation.

The CoCounsel team spent years learning these lessons. We're applying their learnings in weeks.

**End result:** Mise becomes a system you can trust completely, scale confidently, and extend easily.

---

*Mise: Everything in its place.*
