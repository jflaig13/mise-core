# SEARCH FIRST: Mandatory Protocol for All Code Changes

**THIS IS NOT A SUGGESTION. THIS IS A REQUIREMENT.**

## The Cardinal Rule

**NEVER write code, prompts, or documentation without first searching the codebase for existing implementations, policies, and specifications.**

## What Just Happened (The Mistake)

During Phase 1 of the CoCounsel improvements (Jan 27, 2026), I added "grounding rules" to the payroll prompt that **directly contradicted existing canonical policies** because I didn't read the brain files first.

**I wrote:** "DO NOT assume typical hours"
**Codebase already said:** "If hours not mentioned, use standard shift duration"

This violated the user's trust and could have broken production functionality.

**This can NEVER happen again.**

## Before ANY Change, You MUST Search

### Before Adding New Features

```bash
# 1. Search for existing implementations
grep -r "feature_name" --include="*.py" --include="*.md"

# 2. Check workflow specs
ls workflow_specs/
cat workflow_specs/[RELEVANT_SPEC]/[SPEC_FILE]

# 3. Check brain files
ls docs/brain/
grep -r "topic" docs/brain/

# 4. Check existing prompts
grep -r "topic" transrouter/src/prompts/

# 5. Check agent implementations
ls transrouter/src/agents/
```

### Before Modifying Prompts

**MANDATORY READING (in order):**

1. **Read the current prompt file COMPLETELY**
   - Don't skim, don't assume
   - Understand what's already there
   - Note any policies or rules

2. **Search brain files for the domain**
   ```bash
   ls docs/brain/ | grep -i payroll
   ls docs/brain/ | grep -i inventory
   # READ EVERY MATCHING FILE
   ```

3. **Search workflow specs**
   ```bash
   ls workflow_specs/LPM/  # For payroll
   ls workflow_specs/LIM/  # For inventory
   # READ THE MASTER SPEC
   ```

4. **Search for related documentation**
   ```bash
   grep -r "tip pool" docs/
   grep -r "shift duration" workflow_specs/
   ```

### Before Adding Business Rules

**STOP. The business rules already exist.**

Business rules do NOT live in your head. They live in:
- `workflow_specs/[DOMAIN]/[DOMAIN]_Workflow_Master.txt`
- `docs/brain/*.md`
- Existing prompt files in `transrouter/src/prompts/`

**Read them. All of them. Before writing a single line of code.**

### Before Asking the User Questions

**REQUIRED SEARCH PROTOCOL:**

Before asking "What are the shift hours?" or "What's the tip pool policy?":

1. Search docs/brain/
2. Search workflow_specs/
3. Search existing prompts
4. Search existing agent code
5. Search config files

**Only if ALL FIVE searches come up empty** may you ask the user.

## Specific Searches Required by Domain

### Payroll Changes

**MUST READ (no exceptions):**
- `workflow_specs/LPM/LPM_Workflow_Master.txt`
- `docs/brain/*lpm*.md`
- `docs/brain/*payroll*.md`
- `docs/brain/*shift*.md`
- `docs/brain/*tip*.md`
- `transrouter/src/prompts/payroll_prompt.py` (ENTIRE FILE)

### Inventory Changes

**MUST READ:**
- `workflow_specs/LIM/LIM_Workflow_Master.txt`
- `docs/brain/*lim*.md`
- `docs/brain/*inventory*.md`
- `transrouter/src/prompts/inventory_prompt.py` (if exists)

### Ordering Changes

**MUST READ:**
- `workflow_specs/ordering/` (if exists)
- `docs/brain/*ordering*.md`

## The "I've Read Everything" Checklist

Before submitting ANY code change that touches business logic, prompts, or policies, you MUST confirm:

- [ ] I have read the complete workflow spec for this domain
- [ ] I have searched and read all relevant brain files
- [ ] I have read the ENTIRE existing prompt file (not skimmed)
- [ ] I have searched for existing implementations of this feature
- [ ] I have verified my changes do NOT contradict existing policies
- [ ] I have confirmed that canonical policies are preserved
- [ ] I can cite specific files/line numbers that support my changes

**If you cannot check ALL boxes, DO NOT PROCEED.**

## How to Announce Your Search

When you're about to make a change, SAY THIS:

> "Before implementing [feature], I will search:
> 1. [specific files/directories]
> 2. [specific grep patterns]
> 3. [specific keywords]
>
> I will read [list specific files] completely before proceeding."

Then DO IT. Then show the results.

## Consequences of Violating This

Violating this protocol:
1. **Wastes the user's time** (explaining things that are documented)
2. **Breaks trust** (shows you're not thorough)
3. **Risks production bugs** (contradicting existing logic)
4. **Requires rollback** (wasted effort)

## The User's Explicit Instruction

From the user (Jan 27, 2026):

> "You should NOT be asking me questions like this."
> "Check my damn workflow specs/brain files before asking me questions like this!"
> "This can never happen again."

## Emergency Protocol

If you realize mid-implementation that you DIDN'T search first:

1. **STOP IMMEDIATELY**
2. Announce: "I need to pause and search the codebase first"
3. Conduct the searches listed above
4. Read the results COMPLETELY
5. **Only then** continue or restart

## Remember

**The codebase IS the brain. The brain IS the source of truth.**

Not your memory. Not your assumptions. Not "what usually happens."

**THE. CODEBASE.**

---

*This file was created after a critical mistake in Phase 1 of the CoCounsel improvements. It must be referenced from CLAUDE.md and enforced in all future work.*
