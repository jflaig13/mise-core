TITLE
SCRIBE ENFORCEMENT PROTOCOL — BEHAVIORAL RULES FOR ENGINEERING RISK CLASSIFICATION

STATUS
CANONICAL

DATE ADDED
2026-02-07 (filename uses mmddyy format: 020726)

SOURCE
Jon — via ChatGPT-marked directive (ChatGPT Desktop watching terminal, clearly marked [CHATGPT-DIRECTIVE]). This is a behavioral amendment to `020726__engineering-risk-classification.md`. It does not replace or weaken that document — it extends it with explicit enforcement procedures for the Scribe agent and mandatory stop conditions for all AI agents.

PURPOSE
Define the exact behavioral rules that govern how the Scribe agent (and all AI agents) apply the Engineering Risk Classification system in practice. Specifically:
1. How the Scribe classifies a task's Subsystem Tier and Engineering Difficulty Grade.
2. What happens when classification is ambiguous (default escalation rules).
3. Mandatory stop conditions — situations where work MUST halt until a human decides.
4. What counts as a protocol violation, what the Scribe must do when one occurs, and how violations are recorded.
5. Concrete examples of correct behavior, incorrect behavior, and edge case escalation.
6. How this protocol integrates with SEARCH_FIRST.md and AGI_STANDARD.md.
7. How conflicts between this protocol and other canon are resolved.

AUTHORITY LEVEL
This brain file operates at Layer 3 (Brain Files) in the Mise Bible hierarchy, at the same level as `020726__engineering-risk-classification.md`. It is a behavioral companion to that document — the classification system defines WHAT the tiers and grades are; this document defines HOW they are applied in practice.

This document does NOT override:
- VALUES_CORE.md (Layer 1)
- AGI_STANDARD.md (Layer 1)
- SEARCH_FIRST.md (Layer 1)
- AGENT_POLICY.md (Layer 1)
- `020726__engineering-risk-classification.md` (Layer 3, same level — tier assignments and the decision matrix in that document are canonical; this document governs enforcement behavior only)

DEFINITIONS
- Classification act: The moment an AI agent identifies which Tier and EDG apply to a proposed change, states them explicitly, and determines the required protocol from the decision matrix.
- Stop condition: A situation where an AI agent MUST halt all implementation work and wait for human input. Work cannot resume until the human provides the required authorization.
- Protocol violation: Any instance where the rules in `020726__engineering-risk-classification.md` or this document were not followed during a code change.
- Violation record: A brain file or workflow change log entry that documents a protocol violation, including what happened, what should have happened, and recommended corrective action.
- Classify UP: When the correct Tier or EDG is unclear, assign the higher (more cautious) classification. This is the default escalation behavior.
- Scribe audit: A review performed by the Scribe agent to verify that recent changes followed the correct classification protocol.
- Design artifact: A plan file (in `~/.claude/plans/`), a formal spec, or a [CHATGPT-DIRECTIVE] that documents the intended change before implementation begins.

CORE ASSERTIONS
1. Classification is not optional. Every AI agent must classify every code change before implementation. The Scribe enforces this.
2. The Scribe's enforcement authority is limited to recording and reporting. The Scribe does not revert code, block commits, or override human decisions. It records violations and notifies the human. Humans decide corrective action.
3. Stop conditions are absolute. When a stop condition is triggered, no AI agent may proceed with implementation — not even partially, not even "just to see how it looks." Work halts until the human provides the required authorization.
4. Ambiguity resolves upward. If the Scribe or any agent is uncertain about the correct Tier or EDG, the classification defaults to the higher (more cautious) option. This is not a suggestion — it is the mandatory default.
5. Violations are recorded in writing. A violation that is noticed but not recorded is itself a violation (Scribe inaction).

NON-NEGOTIABLE CONSTRAINTS
1. The Scribe MUST perform a classification check whenever it observes or participates in a code change. This is not optional and cannot be skipped for convenience or speed.
2. Stop conditions cannot be overridden by an AI agent. Only a human (Jon or Austin) can authorize resumption of work after a stop condition is triggered.
3. Violation records must be created within the same session in which the violation is observed. Deferring a violation record to "later" is not acceptable.
4. The Scribe must not soften, minimize, or editorialize when reporting a violation. State what happened, what should have happened, and what is recommended. No hedging.
5. This protocol applies to ALL AI agents in the Mise system (Claude Code, Scribe, Oracle, any future agent, any future coding agent including Gemini, Codex, etc.), not just the Scribe. The Scribe is the enforcer, but all agents are bound by the classification system.

HOW THE SCRIBE CLASSIFIES A TASK

### Step 1: Identify the files affected

Before classifying, the Scribe must know EXACTLY which files will be created, modified, or deleted. If the scope is unclear, the Scribe asks the implementing agent (or the human) to enumerate the affected files.

### Step 2: Determine the Subsystem Tier

For each affected file, look up the tier assignment in `020726__engineering-risk-classification.md` (the SUBSYSTEM TIER ASSIGNMENTS section). The overall change is classified at the HIGHEST tier of any affected file.

Rules:
- If all affected files are Tier C → the change is Tier C.
- If any affected file is Tier B → the change is at least Tier B.
- If any affected file is Tier A → the change is at least Tier A.
- If any affected file is Tier S → the change is Tier S, regardless of how many Tier C files are also involved.
- If a file is NOT listed in the tier assignments (e.g., a new file) → classify based on what the file DOES, not where it lives. A new utility that performs financial calculations is Tier S. A new CSS file is Tier C.

### Step 3: Determine the Engineering Difficulty Grade

Assess the change itself (not the file, but what is being done to it):
- EDG-0: No behavioral change. Comments, whitespace, typos only.
- EDG-1: Single-file, bounded scope, clear cause-and-effect. Adding a log line, fixing an obvious bug, updating a config value.
- EDG-2: Multi-file OR requires understanding of surrounding context. New functions, route modifications, prompt edits.
- EDG-3: Architectural impact. New subsystems, schema changes, cross-workflow changes. Requires design-first regardless of tier.
- EDG-4: EDG-3 complexity in a Tier S subsystem. Financial logic, approval flow, orchestration pipeline. Requires formal directive.

When in doubt between two adjacent grades, choose the higher one.

### Step 4: State the classification

The Scribe (or any implementing agent) must state the classification explicitly before any code is written. Format:

> "This is **Tier [S/A/B/C] × EDG-[0-4]**. [One sentence describing why.] [Required protocol from decision matrix.]"

Example:
> "This is **Tier S × EDG-2**. Modifying the payroll prompt to handle double shifts. Design-first is mandatory. Explicit approval required at each step. Workflow change log required."

### Step 5: Apply the decision matrix

Consult the Tier × EDG Decision Matrix in `020726__engineering-risk-classification.md` and follow the required protocol exactly.

DEFAULT ESCALATION RULES

When classification is ambiguous, these defaults apply:

1. **Tier ambiguity** (is this file Tier A or Tier S?): Classify as the higher tier. If you think it might be Tier S, it's Tier S.
2. **EDG ambiguity** (is this EDG-1 or EDG-2?): Classify as the higher grade. If you think it might need design-first, it needs design-first.
3. **New file ambiguity** (this file doesn't exist in the tier table): Classify based on the file's function. Ask: "If this file had a bug, what would break?" If the answer involves money, data integrity, or user trust → Tier S or A. If cosmetic → Tier B or C.
4. **Cross-tier changes** (touches files in multiple tiers): The entire change inherits the highest tier involved. No exceptions.
5. **Uncertainty about scope** (not sure which files will be affected): Stop. Ask the implementing agent or human to enumerate the files. Do not classify based on assumptions about scope.

MANDATORY STOP CONDITIONS

The following situations require ALL work to halt until a human provides authorization. No AI agent may proceed past a stop condition.

### Stop Condition 1: Tier S × EDG-3 or higher without a design artifact
If a change is classified as Tier S × EDG-3 (or Tier S × EDG-4) and no design artifact exists (no plan file, no formal spec, no [CHATGPT-DIRECTIVE]), work MUST stop. The agent must:
- State the classification
- State that no design artifact exists
- Request that a plan be created and approved before proceeding

### Stop Condition 2: EDG-4 without a formal directive
If a change is classified as EDG-4 (Tier S × EDG-3+) and there is no [CHATGPT-DIRECTIVE] or equivalent formally scoped directive, work MUST stop. A casual chat message is insufficient. The agent must:
- State the classification
- State that EDG-4 requires a formal directive
- Refuse to proceed until one is provided

### Stop Condition 3: Tier S modification without explicit approval for the specific change
If an agent is about to modify a Tier S file and has not received explicit human approval for THAT SPECIFIC change (not a general "go ahead"), work MUST stop. The agent must:
- State exactly what it intends to change and in which file
- Wait for explicit approval

### Stop Condition 4: Classification cannot be determined
If the Scribe or implementing agent genuinely cannot determine the correct Tier or EDG (even after applying the "classify UP" rule), work MUST stop. The agent must:
- State what it knows and what it doesn't
- Present the options (e.g., "this could be Tier A × EDG-2 or Tier S × EDG-2 depending on whether [X]")
- Let the human decide

### Stop Condition 5: Detected violation in progress
If the Scribe observes that an agent is actively committing a protocol violation (e.g., modifying Tier S without stated classification, performing a silent refactor), the Scribe must:
- Immediately flag the violation
- Request that the implementing agent stop and re-classify
- If the implementing agent does not stop, record the violation

PROTOCOL VIOLATIONS: DEFINITION, RESPONSE, AND RECORDING

### What counts as a protocol violation

| Violation | Description |
|-----------|-------------|
| Classification omission | A code change was made without the agent stating the Tier × EDG classification beforehand. |
| Silent refactor in Tier S | Any structural change (renaming, reorganizing, reformatting) in a Tier S file that was not explicitly requested. |
| Scope creep in Tier S/A | The change includes modifications beyond what was explicitly requested. |
| Missing design artifact | An EDG-3+ change was implemented without a plan, spec, or directive. |
| Missing directive for EDG-4 | An EDG-4 change was implemented without a [CHATGPT-DIRECTIVE] or equivalent. |
| Missing workflow change log | A Tier S change at EDG-1+ was committed without a corresponding `workflow_changes/` entry. |
| Self-downgrading | An agent classified a change at a lower tier or EDG than warranted to avoid protocol requirements. |
| Stop condition bypass | An agent continued work past a mandatory stop condition without human authorization. |
| Scribe inaction | The Scribe observed a violation and did not record it. |

### What the Scribe must do when a violation occurs

1. **State the violation clearly.** Identify: which rule was broken, which file was affected, what should have happened.
2. **Record the violation.** Create one of:
   - A workflow change log entry in `workflow_specs/{DOMAIN}/workflow_changes/MMDDYY_violation-description.txt` — if the violation is specific to a single domain (LPM, CPM, LIM, etc.)
   - A brain file `docs/brain/MMDDYY__risk-violation-[slug].md` — if the violation is systemic, cross-domain, or involves institutional protocol
3. **Recommend corrective action.** State what should be done: revert the change, add the missing classification, create the missing log, etc. The Scribe recommends; the human decides.
4. **Do not silently fix.** The Scribe does not undo the violating change itself. It records and reports. Humans decide corrective action.

### How violations are recorded

| Violation scope | Record type | Location |
|----------------|-------------|----------|
| Single domain (e.g., payroll-specific) | Workflow change log | `workflow_specs/{DOMAIN}/workflow_changes/MMDDYY_violation-description.txt` |
| Cross-domain or systemic | Brain file | `docs/brain/MMDDYY__risk-violation-[slug].md` |
| Scribe inaction (meta-violation) | Brain file | `docs/brain/MMDDYY__scribe-inaction-[slug].md` |

Violation records must include:
- Date and time of the violation
- Which agent committed the violation
- Which rule was broken (cite the specific section of `020726__engineering-risk-classification.md` or this document)
- What actually happened
- What should have happened
- Recommended corrective action
- Whether the human has been notified

ALLOWED BEHAVIORS
- Classifying any change, even if another agent has already classified it (second-opinion classification is always allowed).
- Escalating a classification upward at any time.
- Requesting that an implementing agent re-state its classification if the Scribe believes it was incorrect.
- Proactively auditing recent changes by reading git diffs and checking for classification compliance.
- Creating violation records for any observed violation, regardless of when it occurred (retroactive violation recording is allowed and encouraged).
- Asking the human to clarify ambiguous scope before classifying.

DISALLOWED BEHAVIORS
- Classifying a change at a lower tier or EDG than warranted.
- Proceeding past a stop condition without human authorization.
- Recording a violation but softening the language to avoid "bothering" the user. State facts plainly.
- Silently fixing a violation instead of recording and reporting it.
- Deferring violation recording to a future session. Record it now.
- Overriding a tier classification. Only humans can do this.
- Skipping classification because "it's just a small change." All changes are classified. EDG-0 exists for trivial changes — use it instead of skipping.

DECISION TESTS
1. **Has the implementing agent stated a Tier × EDG classification?** If no → violation (classification omission). Flag it.
2. **Does the stated classification match the files being modified?** If no → possible self-downgrading. Investigate and escalate.
3. **Is the change scope exactly what was requested?** If it includes anything beyond the request → scope creep. Flag it.
4. **Is a stop condition active?** If yes and work is continuing → stop condition bypass. Flag it immediately.
5. **Does the required protocol from the decision matrix match what was actually followed?** If a change required design-first but no plan exists → missing design artifact. Flag it.
6. **Is there a workflow change log for this Tier S change?** If no → missing log. Create one or flag the omission.

EXAMPLES

### Example 1: Correct Behavior — Routine Tier S × EDG-1 Change

**Scenario:** Jon asks an agent to add a new employee name variant to `payroll_agent/CPM/engine/normalizer.py`.

**Correct behavior:**
1. Agent states: "This is **Tier S × EDG-1**. Adding 'Bobby' → 'Robert Thompson' to the name normalization dictionary in normalizer.py. Single-file change, bounded scope. Explicit approval required."
2. Agent waits for Jon to approve.
3. Jon says: "Go ahead."
4. Agent makes the change — adds exactly one entry to the dictionary. Touches nothing else.
5. Agent creates `workflow_specs/CPM/workflow_changes/020726_add-name-variant-bobby.txt` documenting the addition.
6. Scribe verifies: classification stated ✓, approval obtained ✓, scope matches request ✓, workflow log created ✓. No violation.

### Example 2: Incorrect Behavior — Silent Refactor in Tier S

**Scenario:** An agent is asked to fix a tipout rounding error in `payroll_agent/LPM/build_from_json.py`. While fixing the bug, the agent also renames three variables from camelCase to snake_case and adds type hints to the function signature.

**What happened wrong:**
- The variable renaming and type hints were NOT requested. This is a silent refactor in a Tier S file.
- The agent did not state a separate classification for the refactoring work.
- This is scope creep in Tier S — a protocol violation.

**What the Scribe must do:**
1. State: "Protocol violation detected: silent refactor in Tier S. The agent was asked to fix a tipout rounding error in build_from_json.py but also renamed 3 variables and added type hints. This is scope creep per 020726__engineering-risk-classification.md, DISALLOWED BEHAVIORS, items 1 and 2."
2. Create `workflow_specs/LPM/workflow_changes/020726_violation-silent-refactor-build-from-json.txt` documenting the violation.
3. Recommend: "Revert the variable renaming and type hint additions. Keep only the tipout rounding fix. If the renaming is desired, it should be a separate task with its own classification."
4. Notify Jon.

### Example 3: Edge Case Escalation — New File, Ambiguous Tier

**Scenario:** An agent is asked to create a new file `mise_app/tip_calculator.py` that centralizes tipout calculation logic currently spread across multiple files.

**Classification challenge:** This file doesn't exist in the tier table. It's a new file. But it performs financial calculations (tipout math).

**Correct escalation:**
1. Agent applies the "new file ambiguity" rule: "If this file had a bug, what would break?" → Tip calculations would be wrong. People get paid wrong. This is financial.
2. Agent classifies: "This is **Tier S × EDG-3**. Creating a new file that centralizes tipout calculation logic. This is architectural (moving logic between files) and financial (tipout math). Design-first is mandatory. Formal plan required."
3. Agent triggers Stop Condition 1: "Tier S × EDG-3 without a design artifact. I need a plan approved before I write any code."
4. Agent writes a plan in `~/.claude/plans/` describing: what logic is being moved, from which files, the new file's interface, and how existing callers will be updated.
5. Agent presents the plan to Jon and waits for approval.
6. Only after approval does the agent proceed with implementation.

### Example 4: Correct Behavior — Tier B × EDG-2, No Escalation Needed

**Scenario:** An agent is asked to add a "last updated" timestamp to the inventory totals template.

**Correct behavior:**
1. Agent states: "This is **Tier B × EDG-2**. Modifying `mise_app/templates/inventory_totals.html` to display a last-updated timestamp, and adding the timestamp to the route handler in `mise_app/routes/inventory.py`. Two files, display logic. Proceeding with normal caution."
2. Agent implements the change. No design-first required. No stop condition triggered.
3. No workflow change log required (Tier B, not Tier S).
4. Scribe verifies: classification stated ✓, scope matches ✓. No violation.

EDGE CASES & AMBIGUITIES
1. **An agent classifies correctly but the human overrides to a lower tier.** The Scribe accepts the override (humans can override) but records it per the override rules in `020726__engineering-risk-classification.md`. The Scribe does not argue with the human.
2. **Two agents disagree on the classification.** The higher classification wins by default. If the disagreement cannot be resolved, it becomes Stop Condition 4 (classification cannot be determined) and the human decides.
3. **A change was correctly classified at the start but scope expanded during implementation.** The Scribe must re-classify based on the actual final scope. If the scope expanded into a higher tier or EDG, a retroactive violation may apply (the agent should have re-classified and re-obtained approval when scope changed).
4. **A violation occurred in a previous session and was not caught.** The Scribe may create a retroactive violation record at any time. There is no statute of limitations on violations.
5. **The Scribe itself is the implementing agent.** The Scribe must still classify its own changes. Being the enforcer does not exempt you from the rules.
6. **A change is EDG-0 in Tier S (comment/typo fix).** The agent must still state the classification ("Tier S × EDG-0, comment fix, no behavioral change") but may proceed without explicit approval. This is the only Tier S scenario where the agent may proceed without waiting for human approval — but only if there is truly zero behavioral change.

INTEGRATION WITH SEARCH_FIRST.md AND AGI_STANDARD.md

### SEARCH_FIRST Integration

The SEARCH_FIRST protocol is performed BEFORE classification. The search results inform the classification.

Workflow:
1. **SEARCH_FIRST** — Search workflow_specs/, docs/brain/, prompts, agents, and config for context about the area being changed.
2. **Classification** — Using the information gathered from SEARCH_FIRST, determine the Tier and EDG.
3. **Decision matrix** — Apply the required protocol from the decision matrix.
4. **Implementation** (if authorized)

SEARCH_FIRST and classification are complementary, not competing. SEARCH_FIRST tells you what exists. Classification tells you how careful to be when changing it.

If SEARCH_FIRST reveals that a proposed change touches more files or subsystems than originally expected, the classification must be updated accordingly (likely to a higher tier or EDG).

### AGI_STANDARD Integration

The AGI_STANDARD 5-question framework becomes mandatory for EDG-3+ changes (it is always recommended but becomes non-optional at EDG-3+):

1. **"Are we solving the right problem?"** — Especially critical at EDG-3+. Is this architectural change actually needed, or is there a simpler solution at EDG-1 or EDG-2?
2. **"What are we NOT considering?"** — At EDG-3+, the blast radius is large. What second-order effects could this change have?
3. **"What would break this?"** — At Tier S, this question carries financial weight. What happens if this change has a bug?
4. **"Is there a simpler solution?"** — Could this EDG-3 change be decomposed into multiple EDG-1 or EDG-2 changes that are individually safer?
5. **"What does success look like?"** — How do we verify that this change is correct after implementation?

The AGI_STANDARD questions should be answered IN the design artifact (plan file, spec, or directive) for EDG-3+ changes.

### Conflict Resolution

| Conflict | Resolution |
|----------|------------|
| This protocol vs. VALUES_CORE.md | VALUES_CORE.md wins. Always. |
| This protocol vs. AGI_STANDARD.md | AGI_STANDARD.md wins. The 5-question framework cannot be skipped even if this protocol doesn't require it for a given EDG level. |
| This protocol vs. SEARCH_FIRST.md | SEARCH_FIRST.md wins. Search always comes first, before classification. |
| This protocol vs. AGENT_POLICY.md | AGENT_POLICY.md provides the baseline; this protocol adds granularity. If AGENT_POLICY says "do not change schemas without explicit direction" and this protocol says a schema change is EDG-3, both apply — the agent needs both explicit direction AND a design artifact. |
| This protocol vs. `020726__engineering-risk-classification.md` | The classification document defines tiers, grades, and the decision matrix. This document defines enforcement behavior. They are complementary. If a specific behavior rule here contradicts a specific tier assignment or matrix cell there, the classification document wins (it defines the law; this document defines enforcement). |
| This protocol vs. the t=0 Restricted Section Law | Both apply independently. The t=0 law prevents deletion of existing code. This protocol governs how changes are classified and approved. A change that is correctly classified AND approved still cannot delete t=0 code without separate explicit permission. |

OPERATIONAL IMPACT
1. Every AI agent session that involves code changes must now perform classification as part of its workflow. This adds a small overhead to every task but prevents costly mistakes in safety-critical systems.
2. The Scribe skill gains concrete enforcement procedures. The Scribe's audit operation (Operation 1 in the Scribe SKILL.md) should now include risk classification compliance as a standard check.
3. Design artifacts (plans, specs, directives) gain formal status as required authorization for EDG-3+ changes. This codifies what was previously implicit.
4. Violation recording creates an audit trail that can be reviewed during retrospectives or when onboarding new team members.
5. The [CHATGPT-DIRECTIVE] mechanism is confirmed as one valid authorization method for EDG-4, but not the only one — a plan file or formal spec also qualifies.

CODE REVIEW CHECKLIST
- [ ] Was classification stated before implementation began?
- [ ] Does the classification match the actual files and scope of the change?
- [ ] Were all stop conditions respected (no bypass)?
- [ ] If a violation was detected, was it recorded in writing within the same session?
- [ ] If the change was EDG-3+, was the AGI_STANDARD 5-question framework applied?
- [ ] If the change was Tier S, does a workflow change log entry exist?
- [ ] Was SEARCH_FIRST performed before classification?
- [ ] If scope changed during implementation, was re-classification performed?
- [ ] Does the violation record (if any) include all required fields (date, agent, rule, what happened, what should have happened, recommendation)?

FAILURE MODES
1. **Scribe fails to classify.** The Scribe participates in a code change without stating classification. This is a violation of its own enforcement mandate.
2. **Scribe records violation but does not notify human.** A silent violation record is better than nothing, but the human must be notified. Recording without notification is an incomplete enforcement.
3. **Scribe accepts an agent's self-classification without verification.** The Scribe should independently verify that the stated classification matches the actual files and scope. Trusting without verifying defeats the purpose of enforcement.
4. **Violation record created but missing required fields.** An incomplete violation record is itself a minor protocol failure. All fields (date, agent, rule, what happened, what should have happened, recommendation) must be present.
5. **Stop condition triggered but agent continues "just to prototype."** A stop condition means stop. Not "stop after this function." Not "stop but let me show you what I was thinking." Stop.
6. **Classification performed after implementation.** Retroactive classification is better than none, but classification must happen BEFORE code is written. After-the-fact classification is a violation (classification omission) even if the stated classification is correct.

CHANGELOG
- v1.0 (2026-02-07): Initial Scribe Enforcement Protocol. Defines classification procedure, escalation rules, stop conditions, violation definitions and recording, concrete examples, and integration with SEARCH_FIRST.md and AGI_STANDARD.md. Created via [CHATGPT-DIRECTIVE].
