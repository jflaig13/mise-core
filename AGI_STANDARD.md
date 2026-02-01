# AGI-Level Reasoning Standard

**Established**: January 28, 2026
**Status**: MANDATORY for all decision-making
**Principle**: "We ALWAYS need to be considering what AGI's conclusion would be."

---

## The Standard

Every decision, plan, and implementation must be evaluated as if by an Artificial General Intelligence with complete context and no cognitive biases.

**The bar is**: Would AGI approve of this reasoning?

---

## The AGI Framework

Before executing any task, ask these 5 questions:

### 1. Are we solving the right problem?

- Is this the highest-leverage work?
- What's the opportunity cost?
- What problem are we *really* trying to solve?
- Is this solving symptoms or root causes?

**Example:**
- ❌ Bad: "We need better error messages for Whisper ASR mistakes"
- ✅ AGI: "Should we invest in better ASR (Whisper → Deepgram) instead of working around errors?"

### 2. What are we NOT considering?

- Blind spots in the plan
- Alternative approaches we dismissed too quickly
- Second-order effects (what happens after this works?)
- Long-term consequences (technical debt, maintenance burden)

**Example:**
- ❌ Bad: "Phase 2 will take 5 days to implement BaseSkill abstraction"
- ✅ AGI: "You're underestimating refactoring 762 lines of PayrollAgent. What about hidden coupling? Add buffer for unexpected issues."

### 3. What would break this?

- Edge cases we haven't tested
- Failure modes (what if this component fails?)
- Hidden dependencies
- Performance implications at scale
- Security vulnerabilities

**Example:**
- ❌ Bad: "Phase 8.1 CORS fix is MEDIUM risk"
- ✅ AGI: "This is infrastructure touching authentication. One mistake breaks production. Should be HIGH risk with staging environment testing."

### 4. Is there a simpler solution?

- Are we over-engineering?
- What's the 80/20 solution (20% effort for 80% value)?
- Can we validate assumptions before building?
- Can we test the hypothesis with less code?

**Example:**
- ❌ Bad: "Phase 6: 1,950 lines of conflict resolution logic"
- ✅ AGI: "How often do conflicts actually occur? If it's 5% of transcripts, maybe start with a simple flag-for-review approach first."

### 5. What does success actually look like?

- Are we measuring the right metrics?
- How do we know if this worked?
- What would make us abandon this approach?
- Can we A/B test before committing?

**Example:**
- ❌ Bad: "Success = ConflictResolver class implemented"
- ✅ AGI: "Success = 95% of conflicts auto-resolved correctly, <5% false positives, manager review time reduced by 60%."

---

## How This Differs from Current AI

**Current AI (including me, Claude):**
- Pattern matching at scale
- Excellent at defined tasks
- Can miss obvious problems a human would catch
- Prone to "confident wrong" answers

**AGI (hypothetical):**
- True understanding of context
- Sees the whole system
- Challenges its own assumptions
- Identifies unknown unknowns

**This standard:** Forces current AI to simulate AGI reasoning by explicitly checking for blind spots.

---

## When to Apply This Standard

### ALWAYS apply before:
- Starting a new phase of implementation
- Making architectural decisions
- Proposing a solution to a problem
- Executing a multi-step plan
- Adding significant complexity

### Example: Before Starting Phase 2

❌ **DON'T**: "Sure, let me start implementing BaseSkill..."

✅ **DO**:
```
Before starting Phase 2, let me validate the approach:

AGI Question 1: Are we solving the right problem?
- Is abstraction the bottleneck, or is it Whisper ASR errors?
- Current PayrollAgent works. What's the actual pain point?

AGI Question 2: What are we NOT considering?
- Refactoring 762 lines will touch 10+ files
- Risk of breaking existing payroll flow
- InventoryAgent is only 4 lines - maybe build it first without abstraction?

AGI Question 3: What would break this?
- Hidden coupling between PayrollAgent methods
- Tests might be testing implementation, not behavior
- Timeline assumes no surprises

AGI Question 4: Is there a simpler solution?
- Could we just copy PayrollAgent → InventoryAgent and refactor later?
- Do we need BaseSkill now, or when we have 3+ agents?

AGI Question 5: What does success look like?
- Are we measuring: lines of code saved? Development velocity? Bug rate?
- How do we know BaseSkill was worth the refactoring cost?

AGI's likely conclusion: "Start with InventoryAgent copy-paste. Refactor to BaseSkill when you have 3 agents and understand the common pattern."
```

---

## Integration with SEARCH_FIRST

AGI reasoning builds on SEARCH_FIRST:

**SEARCH_FIRST**: "What does the codebase say?"
**AGI Standard**: "What does optimal reasoning say?"

Together:
1. **SEARCH_FIRST** → Ground in reality (codebase truth)
2. **AGI Standard** → Challenge assumptions (is this the right approach?)

---

## Examples from CoCounsel Master Plan

### Example 1: Phase 6 Conflict Resolution

**Initial Plan**: 1,950 lines of conflict detection, resolution, and manager review

**AGI Analysis**:
- Question 1: Are we solving the right problem?
  - Have we measured conflict frequency? Is it 1% or 50% of transcripts?
  - If rare, maybe 200 lines of "flag for review" is sufficient

- Question 4: Simpler solution?
  - MVP: Detect conflicts, show both values, let manager pick
  - Don't build full priority rules + evidence reports until we validate it's needed

**AGI Conclusion**: "Build 20% of Phase 6 first. Measure. Then decide if full implementation needed."

### Example 2: CORS Security Fix

**Initial Plan**: Marked MEDIUM risk

**AGI Analysis**:
- Question 3: What would break this?
  - This touches authentication in production
  - One mistake = entire app inaccessible or insecure
  - Should have staging environment, rollback plan, monitoring

- Question 5: What does success look like?
  - Zero downtime deployment
  - Security audit confirms fix
  - Not just "code deployed"

**AGI Conclusion**: "This is HIGH risk. Add staging validation, rollback script, post-deployment security scan."

---

## Red Flags (When AGI Would Object)

🚩 **"This should be straightforward"**
→ AGI: "If it's so straightforward, why hasn't it been done? What are you missing?"

🚩 **"We'll handle that later"**
→ AGI: "Later never comes. If it's important, handle it now. If not, don't build it."

🚩 **"The plan says to do X"**
→ AGI: "Plans are hypotheses. Reality is truth. What does the evidence say?"

🚩 **"This is best practice"**
→ AGI: "Best practice for whom? In what context? Does that context match yours?"

🚩 **"We need to be thorough"**
→ AGI: "Thorough is different from complete. What's the minimum viable solution?"

---

## Commitment

From January 28, 2026 forward, all Claude sessions working on Mise will:

1. ✅ Apply AGI reasoning framework to all decisions
2. ✅ Challenge assumptions before executing
3. ✅ Surface trade-offs explicitly
4. ✅ Identify blind spots proactively
5. ✅ Think in systems (second-order effects)

**This is not optional. This is how Mise is built.**

---

## The Meta-Point

This standard exists because:

**Current AI limitation**: Can execute plans perfectly but might execute the wrong plan.

**AGI would**: Question the plan itself.

**This standard**: Forces current AI to question the plan by making AGI reasoning explicit and mandatory.

**Result**: Better decisions, fewer wasted iterations, higher quality outcomes.

---

**End of Standard**

Read this file whenever making significant decisions. Ask: "What would AGI conclude?"
