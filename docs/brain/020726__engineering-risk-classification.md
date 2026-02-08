TITLE
ENGINEERING RISK CLASSIFICATION — SUBSYSTEM TIERS & DIFFICULTY GRADES (INSTITUTIONAL LAW)

STATUS
CANONICAL

DATE ADDED
2026-02-07 (filename uses mmddyy format: 020726)

SOURCE
Jon — via ChatGPT-marked directive (ChatGPT Desktop watching terminal, clearly marked [CHATGPT-DIRECTIVE]). This is higher-order intent, carefully scoped, and architecturally informed per the ChatGPT-Marked Prompt Agreement established 2026-02-06.

PURPOSE
Define a permanent, institution-level risk classification system for all engineering work within the Mise codebase. This system establishes:
1. Safety-Critical Subsystem Tiers (S, A, B, C) that classify every part of the codebase by operational risk.
2. Engineering Difficulty Grades (EDG-0 through EDG-4) that classify the complexity and danger of individual changes.
3. A Tier × EDG matrix that determines required caution, mandatory protocols, and escalation behavior for every combination.
4. Enforcement rules for the Scribe agent and all other agents.
5. Override rules specifying who can override, how, and how overrides are recorded.

This system exists to prevent silent regressions, unchecked scope creep, and cowboy engineering in safety-critical systems. It is institutional law — not advice, not a suggestion, not a guideline.

AUTHORITY LEVEL
This brain file operates at Layer 3 (Brain Files) in the Mise Bible hierarchy. It does NOT override:
- VALUES_CORE.md (Layer 1 governance — the Primary Axiom and hard constraints remain supreme)
- AGI_STANDARD.md (Layer 1 governance — the 5-question framework is always mandatory for significant decisions)
- SEARCH_FIRST.md (Layer 1 governance — mandatory search protocol always applies)

It DOES supplement and extend:
- AGENT_POLICY.md — adds granularity to "touch only the workflow you're assigned" and "do not change schemas/workflows unless explicitly directed"
- The t=0 Restricted Section Law (MEMORY.md) — adds a classification system on top of the existing protection

When this document conflicts with Layer 1 governance, Layer 1 wins. When this document conflicts with Layer 2 workflow specs, this document provides the risk framework that governs HOW changes to those specs are made, but the specs themselves remain authoritative for business logic content. When this document conflicts with other Layer 3 brain files, the conflict must be surfaced and resolved explicitly — neither document silently wins.

DEFINITIONS

- Subsystem Tier: A classification (S, A, B, C) assigned to a region of the codebase based on how much operational damage a bug in that region could cause.
- Tier S (Safety-Critical): Systems where a bug directly causes financial harm, data corruption, or trust destruction. A single error here can end a client relationship or cause legal liability. These are the load-bearing walls of the system.
- Tier A (High-Impact): Systems where a bug degrades the user experience significantly, causes data inconsistency, or blocks a critical workflow. Serious but recoverable.
- Tier B (Moderate-Impact): Systems where a bug causes inconvenience, cosmetic issues, or non-critical workflow degradation. Noticeable but not dangerous.
- Tier C (Low-Impact): Systems where a bug affects development ergonomics, internal tooling, or documentation. No user-facing impact.
- Engineering Difficulty Grade (EDG): A classification (0–4) assigned to a specific change based on how complex, dangerous, or architecturally significant the change is.
- EDG-0 (Trivial): Typo fixes, comment updates, whitespace changes. Zero behavioral impact.
- EDG-1 (Simple): Single-file changes with clear scope. Adding a log line, fixing an obvious bug, updating a config value.
- EDG-2 (Moderate): Multi-file changes, new functions, route modifications, prompt edits. Requires understanding of the surrounding context.
- EDG-3 (Complex): Architectural changes, new subsystem features, schema modifications, changes that affect multiple agents or workflows. Requires design-first approach.
- EDG-4 (Critical): Changes that touch Tier S systems AND are EDG-3 complexity. Changes that modify approval flows, financial calculations, data schemas, or agent orchestration logic. The highest-risk category.
- Design-First: The requirement to write a plan (in ~/.claude/plans/ or as a formal spec) and get explicit human approval BEFORE writing any code.
- Silent Refactor: Any change to code structure, naming, imports, or organization that is not explicitly requested by the user. Disallowed in Tier S.
- Scope Creep: Adding functionality, refactoring, or "improving" code beyond what was explicitly requested. Disallowed in Tier S and Tier A.
- [CHATGPT-DIRECTIVE]: A prompt written by ChatGPT Desktop and clearly marked as such. Per the ChatGPT-Marked Prompt Agreement, these are treated as higher-order intent.

CORE ASSERTIONS

1. Every file in the Mise codebase belongs to exactly one Subsystem Tier.
2. Every proposed change has exactly one Engineering Difficulty Grade.
3. The combination of Tier and EDG determines the required operating behavior. This is not optional.
4. Tier S systems are the financial and operational backbone of Mise. A bug in Tier S directly harms the restaurant operator who trusts us. The Primary Axiom ("Mise helps humanity by refusing to operate in ways that degrade it") makes Tier S protection a values-level concern.
5. No AI agent may self-assess a change as lower-risk than it actually is to avoid protocol. When in doubt, classify UP (higher tier, higher EDG).
6. Design-first is mandatory for any change classified as Tier S × EDG-2 or higher, or any change classified as EDG-3 or higher regardless of tier.
7. The Scribe agent is the enforcement mechanism. If the Scribe observes a violation, it must record it in a brain file and notify the user.

NON-NEGOTIABLE CONSTRAINTS

1. Tier S systems must NEVER be modified without explicit human approval for the specific change.
2. Silent refactors in Tier S are absolutely prohibited. Every line change must be stated, justified, and approved.
3. Scope creep in Tier S and Tier A is absolutely prohibited. If the request says "fix the tipout calculation," you fix the tipout calculation. You do not also rename variables, add docstrings, refactor imports, or "clean up" surrounding code.
4. EDG-4 changes (Tier S × EDG-3+) require a [CHATGPT-DIRECTIVE] or equivalent formally scoped directive. Ad-hoc chat prompts are insufficient authorization for EDG-4 work.
5. All Tier S changes must be logged in the appropriate `workflow_changes/` folder with a dated entry.
6. The t=0 Restricted Section Law applies independently and is not weakened by this classification. Even a Tier C file at t=0 cannot be deleted without explicit permission.
7. When classifying a change, agents must state the classification explicitly before proceeding (e.g., "This is Tier A × EDG-2. Design-first is not mandatory but recommended. Proceeding with implementation.").

SUBSYSTEM TIER ASSIGNMENTS

### Tier S — Safety-Critical

| Subsystem | Key Files | Why Tier S |
|-----------|-----------|------------|
| Payroll Machine (LPM) | `payroll_agent/LPM/build_from_json.py`, `payroll_agent/LPM/PayrollExportTemplate.csv` | Directly generates payroll reports, tip calculations, and Toast CSV exports. Errors here mean people get paid wrong. |
| Payroll Machine (CPM) | `payroll_agent/CPM/engine/payroll_engine.py`, `parse_shift.py`, `commit_shift.py`, `normalizer.py` | Deterministic payroll parser with BigQuery writes. 1200+ lines of shift parsing, 50+ name normalizations. Errors here corrupt the financial database. |
| Payroll Agent (Transrouter) | `transrouter/src/agents/payroll_agent.py`, `transrouter/src/prompts/payroll_prompt.py` | Claude-based payroll parsing that produces approval JSON. The prompt shapes financial output. |
| Approval Artifacts | `mise_app/routes/recording.py` (approval/process endpoints), approval queue JSON schema | The approval flow is the human-in-the-loop safety mechanism. If approval is broken, unchecked data reaches payroll. |
| Inventory Engine (Canonical Spec) | `workflow_specs/LIM/LIM_Workflow_Master.txt`, `inventory_agent/parser.py`, `inventory_agent/inventory_catalog.json` | The canonical inventory specification and the 880-product catalog. Errors here mean wrong counts reach MarginEdge. |
| Transrouter Core | `transrouter/src/transrouter_orchestrator.py`, `transrouter/src/domain_router.py`, `transrouter/src/brain_sync.py` | The orchestration pipeline that routes audio to the correct agent. Misrouting means payroll audio goes to inventory or vice versa. |

### Tier A — High-Impact

| Subsystem | Key Files | Why Tier A |
|-----------|-----------|------------|
| Inventory Agent (Transrouter) | `transrouter/src/agents/inventory_agent.py`, `transrouter/src/agents/inventory_consolidator.py`, `transrouter/src/prompts/inventory_prompt.py` | Claude-based inventory parsing. Important but errors are caught in the approval flow before reaching MarginEdge. |
| Authentication & Sessions | `mise_app/auth.py`, `mise_app/middleware.py` | Controls who can access the system. Bugs could expose data or lock out users. |
| Storage Backends | `mise_app/storage_backend.py`, `mise_app/local_storage.py`, `mise_app/gcs_audio.py`, `mise_app/shelfy_storage.py` | Data persistence layer. Bugs could lose recordings, approvals, or shelfy data. |
| ASR / Transcription | `transrouter/src/asr_adapter.py`, `mise_app/direct_transcription.py` | Audio-to-text pipeline. Bad transcription degrades all downstream parsing. |
| Client Configuration | `clients/papasurf/config.json`, `clients/*/roster.csv` | Per-restaurant settings and employee data. Wrong roster = wrong names in payroll. |
| Config & State | `mise_app/config.py` (PayPeriod, ShiftyStateManager, ShiftyConfig) | Shift definitions, period boundaries, state machine. Wrong config = wrong shift calculations. |

### Tier B — Moderate-Impact

| Subsystem | Key Files | Why Tier B |
|-----------|-----------|------------|
| Web UI Routes (non-approval) | `mise_app/routes/home.py`, `mise_app/routes/totals.py`, `mise_app/routes/auth.py` | Display logic. Bugs are visible to users but don't corrupt data. |
| Templates | `mise_app/templates/*.html` | Visual presentation. Cosmetic issues, not data issues. |
| Inventory Utilities | `inventory_agent/tokenizer.py`, `inventory_agent/normalizer.py`, `inventory_agent/validator.py`, `inventory_agent/generate_inventory_file.py` | Supporting tools for inventory parsing. Important but downstream of the core agent. |
| Sheets Integration | `transrouter/src/sheets/` | Google Sheets integration. Potentially unused or secondary. |
| Conversation Manager | `transrouter/src/conversation_manager.py` | Multi-turn state. Important for UX but not for data integrity. |

### Tier C — Low-Impact

| Subsystem | Key Files | Why Tier C |
|-----------|-----------|------------|
| Static Assets | `mise_app/static/css/`, `mise_app/static/icons/`, `mise_app/static/logos/` | Visual assets. No behavioral impact. |
| Scripts & Utilities | `scripts/*`, root-level debug/test scripts | Development tools. No production impact. |
| Test Suites | `tests/`, `transrouter/tests/` | Tests themselves. Bugs here don't affect production (but DO affect safety verification). |
| Documentation | `docs/` (non-brain), `docs/internal_mise_docs/`, `fundraising/` | Documents and IMDs. Important for institutional knowledge but not for system behavior. |
| Claude Code Skills | `.claude/skills/` | Agent skill definitions. Affect agent behavior but not production code directly. |
| AI Configs | `AI_Configs/` | Model configuration. Affects AI behavior in development but production prompts live in `transrouter/src/prompts/`. |
| Command Queue | `claude_commands/` | Numbered shell commands. Internal tooling only. |

ENGINEERING DIFFICULTY GRADES

### EDG-0: Trivial
- Typo fixes in comments or documentation
- Whitespace or formatting changes
- Adding a comment to explain existing code
- **Risk:** None. No behavioral change.

### EDG-1: Simple
- Single-file changes with clear, bounded scope
- Fixing an obvious bug with a known root cause
- Adding a log line or debug output
- Updating a configuration value (e.g., changing a port number, updating a timeout)
- Adding a new entry to an existing mapping/dictionary
- **Risk:** Low. Change is isolated and easy to verify.

### EDG-2: Moderate
- Multi-file changes with understood dependencies
- Adding a new function or method to an existing class
- Modifying a route handler's logic
- Editing a prompt (system or user prompt for an agent)
- Adding a new template or modifying template logic
- **Risk:** Medium. Requires understanding of context. Could have unintended side effects.

### EDG-3: Complex
- Architectural changes (new subsystems, new agents, new pipelines)
- Schema modifications (approval JSON, inventory catalog, database tables)
- Changes that affect multiple agents or cross workflow boundaries
- New integrations with external services
- Refactoring that changes control flow or data flow
- **Risk:** High. Requires design-first. Multiple failure modes possible.

### EDG-4: Critical
- Any EDG-3 change that touches a Tier S subsystem
- Changes to financial calculation logic (tipout math, shift hours, pay period boundaries)
- Changes to the approval flow (what gets approved, how, by whom)
- Changes to the orchestration pipeline (how intents are classified, how agents are routed)
- Database schema changes in production (BigQuery, GCS storage schemas)
- **Risk:** Maximum. Requires formal directive, design-first, explicit approval at every step.

TIER × EDG DECISION MATRIX

| | EDG-0 (Trivial) | EDG-1 (Simple) | EDG-2 (Moderate) | EDG-3 (Complex) | EDG-4 (Critical) |
|---|---|---|---|---|---|
| **Tier S** | State classification. Proceed with care. | State classification. Explicit approval required before implementation. | Design-first MANDATORY. Explicit approval at each step. Log in workflow_changes/. | Design-first MANDATORY. Formal plan required. [CHATGPT-DIRECTIVE] or equivalent formal scoping recommended. Log in workflow_changes/. | Design-first MANDATORY. [CHATGPT-DIRECTIVE] or equivalent formal directive REQUIRED. Plan must be approved before any code is written. Full audit trail in workflow_changes/. |
| **Tier A** | Proceed. State classification. | State classification. Proceed with normal caution. | State classification. Design-first recommended but not mandatory. Explicit approval before implementation. | Design-first MANDATORY. Formal plan required. Explicit approval. | N/A (EDG-4 is defined as Tier S × EDG-3+; Tier A changes max out at EDG-3) |
| **Tier B** | Proceed freely. | Proceed. State classification if changing behavior. | State classification. Proceed with normal caution. | Design-first MANDATORY. | N/A |
| **Tier C** | Proceed freely. | Proceed freely. | Proceed. State classification. | Design-first recommended. | N/A |

Key for the matrix:
- "State classification" = The agent must explicitly say the Tier and EDG before proceeding (e.g., "Tier B × EDG-1. Proceeding.").
- "Design-first MANDATORY" = A plan must be written and approved before code is written. No exceptions.
- "Explicit approval" = The human must say yes to the specific proposed change. Blanket "go ahead" is insufficient for Tier S.
- "[CHATGPT-DIRECTIVE] or equivalent" = A formally scoped, clearly marked directive. Not a casual chat message.
- "Log in workflow_changes/" = A dated change log entry must be created in the appropriate workflow's change folder.

ALLOWED BEHAVIORS

- Classifying any file or change according to this system.
- Escalating a classification upward (e.g., treating a Tier B change as Tier A out of caution). When in doubt, classify UP.
- Requesting design-first even when the matrix says it's optional. More caution is always allowed.
- The Scribe agent may proactively audit recent changes for classification compliance.
- Any agent may ask "What tier is this subsystem?" and expect an authoritative answer based on this document.
- Creating workflow_changes/ entries for any Tier S or Tier A change.

DISALLOWED BEHAVIORS

1. **Silent refactors in Tier S.** No renaming variables, reorganizing imports, adding type hints, reformatting code, or "cleaning up" any Tier S file unless that specific change was explicitly requested. Every character change must be stated and justified.
2. **Scope creep in Tier S or Tier A.** If the request is "fix the tipout calculation for bussers," you fix the tipout calculation for bussers. You do not also fix the tipout calculation for expos, add validation for edge cases you noticed, refactor the surrounding function, or improve error handling. Stay in the box.
3. **Self-downgrading classification.** An agent may not reclassify a Tier S subsystem as Tier A to avoid protocol. The tier assignments in this document are canonical. Only a human can override them (see ENFORCEMENT & OVERRIDES).
4. **Proceeding without stating classification.** For any change at EDG-1 or above in Tier S or Tier A, the agent MUST state the Tier × EDG classification before writing code. Omitting this is a protocol violation.
5. **Ad-hoc EDG-4 changes.** EDG-4 changes cannot be initiated by a casual chat message. They require a formally scoped directive (a [CHATGPT-DIRECTIVE], a plan file in ~/.claude/plans/, or an explicit multi-step approval sequence with the user).
6. **Skipping workflow_changes/ logs for Tier S.** Every Tier S change at EDG-1 or above must have a corresponding dated entry in the appropriate `workflow_specs/{DOMAIN}/workflow_changes/` folder.
7. **Modifying this brain file without a new brain ingest.** This document may only be updated by creating a NEW brain file that explicitly supersedes specific sections, per the append-only brain file protocol.

DECISION TESTS

1. **Am I about to touch a Tier S file?** → Stop. State the classification. Get explicit approval for the specific change. If EDG-2+, write a plan first.
2. **Is my change affecting more than what was explicitly requested?** → That's scope creep. Stop. Do only what was asked.
3. **Did I state my Tier × EDG classification before writing code?** → If no, pause and state it now.
4. **Is this an EDG-3+ change?** → Design-first is mandatory regardless of tier. Write the plan, get approval, then implement.
5. **Is this an EDG-4 change?** → Is there a formal directive authorizing it? If not, do not proceed. Request one.
6. **Am I tempted to "also fix" something nearby?** → That's scope creep. Note it separately. Do not include it in the current change.
7. **Am I uncertain about the tier or EDG?** → Classify UP. Treat it as higher-risk. More caution never hurts.

ENFORCEMENT & OVERRIDES

### Enforcement (The Scribe's Role)

The Scribe agent (`/scribe`) is the enforcement mechanism for this classification system:

1. **Audit authority.** The Scribe may audit any recent change and assess whether the correct Tier × EDG protocol was followed.
2. **Violation recording.** If the Scribe identifies a violation (e.g., a silent refactor in Tier S, a missing classification statement, a skipped workflow_changes/ log), it MUST:
   a. Create a brain file documenting the violation (`docs/brain/MMDDYY__risk-violation-[slug].md`)
   b. Notify the user (Jon or Austin) of the violation and what needs to be corrected
   c. Recommend corrective action (revert, add missing logs, etc.)
3. **Proactive classification.** When assisting with any change, the Scribe should state the Tier × EDG classification even if other agents did not.
4. **No enforcement without record.** The Scribe does not silently fix violations. It records them and reports them. Humans decide the corrective action.

### Override Rules

1. **Who can override:** Only Jon (President & CEO) or Austin (Secretary & Treasurer) — the two directors of Mise, Inc.
2. **How to override:** The human must explicitly state the override and the reason. Example: "Override: reclassify transrouter_orchestrator.py as Tier A for this specific change because [reason]."
3. **How overrides are recorded:** Every override must be logged in a workflow_changes/ entry or a brain file. The log must include: (a) what was overridden, (b) who authorized it, (c) why, (d) the date. Overrides without written records are invalid.
4. **Scope of override:** An override applies to the specific change for which it was granted. It does not permanently reclassify the subsystem. The tier assignments in this document remain canonical unless superseded by a new brain file.
5. **AI agents cannot override.** No AI agent (Claude, ChatGPT, Gemini, Codex, or any future agent) may override a tier classification. Only humans can.

EXAMPLES

### Example 1: Fixing a typo in a comment inside payroll_agent.py
- **Classification:** Tier S × EDG-0
- **Required behavior:** State classification. Proceed with care. "This is Tier S × EDG-0. Fixing a comment typo in payroll_agent.py line 47. No behavioral change."

### Example 2: Adding a new product to inventory_catalog.json
- **Classification:** Tier S × EDG-1
- **Required behavior:** State classification. Get explicit approval. "This is Tier S × EDG-1. Adding 'Oatly Barista Edition 32oz' to inventory_catalog.json under the bar category. No existing entries are modified. Approval required."

### Example 3: Modifying the payroll system prompt
- **Classification:** Tier S × EDG-2
- **Required behavior:** Design-first mandatory. State classification. Write a plan describing the prompt change and its expected effect. Get explicit approval at each step. Log in workflow_changes/. "This is Tier S × EDG-2. Modifying payroll_prompt.py to handle split-shift tipout calculations. Plan required before implementation."

### Example 4: Adding a new agent to the transrouter
- **Classification:** Tier S × EDG-3
- **Required behavior:** Design-first mandatory. Formal plan required. [CHATGPT-DIRECTIVE] or equivalent recommended. Full workflow_changes/ log. "This is Tier S × EDG-3. Adding a Scheduling Agent to the transrouter pipeline. Formal plan and directive required."

### Example 5: Restructuring the approval flow
- **Classification:** Tier S × EDG-4
- **Required behavior:** [CHATGPT-DIRECTIVE] or equivalent formal directive REQUIRED. Design-first mandatory. Plan must be approved before any code is written. Full audit trail. "This is Tier S × EDG-4. Restructuring how approval_queue.json is generated and consumed. Formal directive required. Cannot proceed without one."

### Example 6: Updating a CSS color in the inventory template
- **Classification:** Tier B × EDG-0
- **Required behavior:** Proceed freely. No classification statement needed.

### Example 7: Adding a new route for a dashboard page
- **Classification:** Tier B × EDG-2
- **Required behavior:** State classification. Proceed with normal caution. "Tier B × EDG-2. Adding /dashboard route to mise_app/routes/. Proceeding."

NON-EXAMPLES

1. **NOT a valid Tier S classification:** Treating `mise_app/static/css/styles.css` as Tier S because "it's part of the app." Static assets are Tier C.
2. **NOT a valid EDG-0:** Renaming a variable inside payroll_engine.py. That's a silent refactor in Tier S — it changes behavior (import paths, grep-ability) even if it doesn't change logic. This is EDG-1 at minimum and requires explicit approval.
3. **NOT a valid override:** An AI agent saying "I'm reclassifying this as Tier B because the change is small." AI agents cannot override tier classifications. Period.
4. **NOT a valid scope:** Being asked to fix a bug in `commit_shift.py` and also "cleaning up" `normalizer.py` while you're in there. That's scope creep in Tier S. Fix the bug. Stop.
5. **NOT a valid EDG-4 authorization:** A chat message saying "yeah go ahead and refactor the approval flow." EDG-4 requires a formally scoped directive, not casual approval.

EDGE CASES & AMBIGUITIES

1. **A change touches both Tier S and Tier B files.** → Classify the entire change at the highest tier involved. If you're modifying payroll_agent.py (Tier S) and a template (Tier B), the change is Tier S.
2. **A new file is being created that doesn't exist in any tier.** → Classify based on what the file DOES, not where it lives. A new financial calculation utility is Tier S even if it's in a new directory.
3. **A test file for a Tier S subsystem.** → The test itself is Tier C (tests don't affect production), but the test's assertions about Tier S behavior should be reviewed with Tier A caution.
4. **A prompt edit that changes Claude's behavior.** → Prompts in `transrouter/src/prompts/` shape the output of financial and inventory agents. Treat prompt edits as the same tier as the agent they serve (payroll prompt = Tier S, inventory prompt = Tier A).
5. **An "improvement" that wasn't requested.** → If it touches Tier S or Tier A, it's scope creep regardless of how beneficial it seems. Note it for a future task. Do not include it.
6. **Emergency hotfix.** → An emergency does not remove the requirement to state classification and log the change. It MAY reduce the design-first requirement for Tier S × EDG-2 to "state the plan verbally and get approval before implementing" rather than writing a formal plan file. The workflow_changes/ log is still mandatory and must be created immediately after the fix, not deferred.
7. **Changes to this brain file itself.** → Per the append-only protocol, this file is never edited. A new brain file must be created to supersede specific sections. That new brain file would itself be classified as Tier A × EDG-3 minimum (it affects institutional governance).

OPERATIONAL IMPACT

1. **All AI agents** (Claude Code, Scribe, Oracle, any future agent) must be aware of this classification system. It applies to every coding task.
2. **The Scribe** gains enforcement responsibility. The Scribe skill definition should reference this brain file as part of its audit operations.
3. **Claude Code sessions** should reference this system when the `SEARCH_FIRST` protocol identifies that a proposed change touches a Tier S subsystem.
4. **The AGI_STANDARD** 5-question framework becomes especially critical for EDG-3+ changes: "Are we solving the right problem?" and "What would break this?" are non-negotiable questions at that difficulty level.
5. **Workflow change logs** (`workflow_specs/{DOMAIN}/workflow_changes/`) become mandatory (not just recommended) for all Tier S changes at EDG-1+.
6. **New team members and engineers** must be briefed on this system during onboarding. The classification is not just for AI agents — it applies to human engineers too.
7. **The [CHATGPT-DIRECTIVE] mechanism** gains formal status as a required authorization method for EDG-4 changes. This codifies what was previously an informal practice.

CODE REVIEW CHECKLIST

For any change, verify:
- [ ] Was the Tier × EDG classification stated before implementation?
- [ ] Does the classification match the actual files and scope of the change?
- [ ] If Tier S: was explicit human approval obtained for the specific change?
- [ ] If Tier S × EDG-1+: does a workflow_changes/ log entry exist?
- [ ] If EDG-2+ in Tier S: was design-first followed (plan written and approved)?
- [ ] If EDG-3+: was a formal plan written regardless of tier?
- [ ] If EDG-4: was a [CHATGPT-DIRECTIVE] or equivalent formal directive provided?
- [ ] Was scope creep avoided? Does the change contain ONLY what was requested?
- [ ] Were no silent refactors performed in Tier S files?
- [ ] If an override was used: is it recorded with who, why, and when?

FAILURE MODES

1. **Classification omission.** An agent makes a Tier S change without stating the classification. → The Scribe must flag this and create a violation record.
2. **Silent refactor in Tier S.** An agent renames a variable, reorganizes imports, or reformats code in a Tier S file as part of another task. → Protocol violation. The change should be reverted or explicitly approved after the fact.
3. **Scope creep in Tier S/A.** An agent "fixes" something adjacent to the requested change. → Protocol violation. The additional change should be reverted and logged as a separate task.
4. **EDG-4 without directive.** A critical change is made based on a casual chat message. → Protocol violation. The change should be reviewed and a retroactive directive created if the change is correct, or reverted if it is not.
5. **Missing workflow_changes/ log.** A Tier S change is committed without an audit trail entry. → The Scribe must create a retroactive log entry and flag the omission.
6. **Self-downgrading.** An agent classifies a Tier S file as Tier A to avoid protocol overhead. → Hard failure. The tier assignments in this document are canonical.
7. **Override without record.** A human verbally overrides a classification but no written record is created. → Invalid override. Must be recorded to take effect.
8. **Scribe inaction.** The Scribe observes a violation and does not record it. → The Scribe has failed its enforcement mandate. The violation and the Scribe's inaction must both be surfaced.

CHANGELOG
- v1.0 (2026-02-07): Initial Engineering Risk Classification system. Established Tier S/A/B/C subsystem classifications, EDG-0 through EDG-4 difficulty grades, Tier × EDG decision matrix, Scribe enforcement rules, and human-only override protocol. Created via [CHATGPT-DIRECTIVE].

CANONICAL SOURCE LANGUAGE
The Mise Engineering Risk Classification system assigns every subsystem a TIER (S, A, B, C) based on operational risk, and every change an ENGINEERING DIFFICULTY GRADE (EDG-0 through EDG-4) based on complexity and danger. The combination determines required caution: Tier S × EDG-0 requires stating the classification; Tier S × EDG-2+ requires design-first; Tier S × EDG-4 (also known as EDG-4) requires a formal directive. SILENT REFACTORS IN TIER S ARE ABSOLUTELY PROHIBITED. SCOPE CREEP IN TIER S AND TIER A IS ABSOLUTELY PROHIBITED. Only humans can override tier classifications, and overrides must be recorded in writing to be valid. The Scribe agent enforces this system and must record any violation. This system does NOT override VALUES_CORE.md or AGI_STANDARD.md. When in doubt, classify UP.
