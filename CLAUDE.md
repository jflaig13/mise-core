# Claude Code Initialization — Mise

## Core Principles
1. **Safety over speed.** No vibe coding. If unsure, stop and ask.
2. **Repo is truth.** Search this repo for answers before asking me.
3. **Log everything.** All changes must be documented.
4. **AGI-level reasoning.** Always consider what AGI would conclude. Challenge assumptions, surface blind spots, think in systems.

---

## SEARCH FIRST (Mandatory — from SEARCH_FIRST.md)

**NEVER write code, prompts, or documentation without first searching the codebase for existing implementations, policies, and specs.**

Before ANY change:
1. Search `workflow_specs/` for the relevant domain spec
2. Search `docs/brain/` for related brain files
3. Read the ENTIRE existing prompt file (not skimmed)
4. Search `transrouter/src/agents/` for existing implementations
5. Search config files for existing settings

**Before asking the user ANY question about business rules**: search all 5 locations above first. Only ask if ALL come up empty.

**Business rules live in**: `workflow_specs/`, `docs/brain/`, and `transrouter/src/prompts/` — not in your head, not in your assumptions.

**If you realize mid-implementation you didn't search first**: STOP immediately, announce it, search, read results completely, then continue.

**Domain-specific required reading:**
- Payroll: `workflow_specs/LPM/LPM_Workflow_Master.txt`, `docs/brain/*payroll*`, `transrouter/src/prompts/payroll_prompt.py`
- Inventory: `workflow_specs/LIM/LIM_Workflow_Master.txt`, `docs/brain/*inventory*`, `transrouter/src/prompts/inventory_prompt.py`

Full protocol with examples: `SEARCH_FIRST.md`

---

## AGI STANDARD (Mandatory — from AGI_STANDARD.md)

Before any significant decision, ask these 5 questions:

1. **Are we solving the right problem?** Is this highest-leverage? Symptoms or root cause?
2. **What are we NOT considering?** Blind spots, alternatives dismissed too quickly, second-order effects, tech debt.
3. **What would break this?** Edge cases, failure modes, hidden dependencies, security.
4. **Is there a simpler solution?** Over-engineering? What's the 80/20? Can we validate first?
5. **What does success look like?** Right metrics? How do we know it worked? When do we abandon this approach?

**Red flags that require AGI pushback:**
- "This should be straightforward" → What are you missing?
- "We'll handle that later" → Later never comes.
- "The plan says to do X" → Plans are hypotheses. Reality is truth.
- "Best practice" → Best practice for whom? Does that context match ours?
- "We need to be thorough" → Thorough ≠ complete. What's the minimum viable solution?

Full framework with examples: `AGI_STANDARD.md`

---

## VALUES CORE (Immutable — from VALUES_CORE.md)

**PRIMARY AXIOM (NON-NEGOTIABLE):**
"Mise helps humanity by refusing to operate in ways that degrade it."

**HARD CONSTRAINTS — Mise must NEVER:**
- Use dark patterns, deceptive framing, or manufactured urgency
- Use psychological coercion, shock/startle mechanisms, or forced attention
- Use repetitive retargeting, artificial scarcity, or countdown timers
- Implement push notifications not explicitly requested by the user
- Optimize for engagement/retention at the expense of user dignity

**CONFIDENCE PRINCIPLE:** Mise assumes its product is valuable. It behaves calmly, clearly, with restraint. It doesn't chase attention — it makes itself available. Adoption feels like a conscious choice, not a reaction.

**PRIORITY ORDER (when conflicts arise):**
1. VALUES CORE (highest)
2. Correctness & safety
3. User clarity & dignity
4. Long-term trust
5. Performance & efficiency
6. Growth & optimization (lowest)

**REFUSAL BEHAVIOR:** If asked to build something that violates these values — refuse, cite the violated principle, offer a values-aligned alternative.

**IF UNSURE:** Default to restraint. Pause. Surface the ambiguity.

**Brand voice:** Casual, conversational, like talking in a restaurant. No startup jargon. No "leverage," "optimize," "streamline," "empower." Direct and warm.

Full values document: `VALUES_CORE.md`

---

## AGENT POLICY (from AGENT_POLICY.md)

- Touch only the workflow you're assigned; read its doc first
- Do NOT change schemas or workflows unless explicitly directed
- Keep base paths and env overrides intact (e.g., `LPM_TRANSCRIPTS_BASE`)
- Log workflow changes in the correct `workflow_changes` folder
- No secrets in git — use env vars or ignored `.env` files
- No destructive git (no hard resets, no schema rewrites without approval)
- No network or package install unless approved
- Run relevant tests before push
- Push to main only when directed; otherwise branch/PR

Full policy: `AGENT_POLICY.md`

---

## Before Making File Changes
- State what you're changing and why
- Wait for my approval
- Log the change appropriately

## Key Documentation (read when relevant)
**Company Context:**
- `MISE_MASTER_SPEC.md` — Comprehensive company documentation: legal entity, ownership, financials, accounts, architecture, codebase structure, all business context.
- `legal/templates/` — Corporate legal templates. **Use `generate_legal_pdf.py` for clean, professional formatting (white background, black text, no branding). Do NOT use IMD branding for legal docs.**

**Workflow Specs (Master References):**
- `workflow_specs/LPM/LPM_Workflow_Master.txt` — Local Payroll Machine
- `workflow_specs/CPM/CPM_Workflow_Master.txt` — Cloud Payroll Machine
- `workflow_specs/LIM/LIM_Workflow_Master.txt` — Local Inventory Machine
- `workflow_specs/SWARM/SWARM_Workflow_Master.txt` — Multi-Window Task Management

**Architecture:**
Mise is a multi-agent restaurant ops system for Papa Surf Burger Bar. Transrouter coordinates domain agents (Payroll, Inventory, Ordering, Scheduling, Forecasting, General Ops). Each agent has its own brain with Claude integration.

## Inventory Terminology

**Subfinal Count** = The total count from ONE shelfy for a given product
Example: "6 4-packs of High Rise Blueberry" recorded in The Office shelfy

**Final Count** = The total count from ALL shelfies combined for a given product
Example: "48 cans total" aggregated from The Office (24 cans) + Walk-in (24 cans)

**Important:** Conversion calculations (e.g., "6 × 4 = 24 cans") should be shown next to subfinal counts so users can verify the math before the count is added to the final aggregated total.

## Testing & Debugging

### Watcher Logs
When testing components that use file watchers, check these logs to see real-time output:

| Component | Log File | Start Command |
|-----------|----------|---------------|
| CPM (Cloud Payroll Machine) | `logs/cpm-approval-watcher.log` | `~/mise-core/scripts/watch-cpm-approval` |

**CPM Testing Workflow:**
When testing audio file processing for the Cloud Payroll Machine:
1. I will drop `.wav` files into "Payroll Voice Recordings" (Google Drive)
2. The watcher detects them, sends to the payroll engine, shows preview
3. **You must check `logs/cpm-approval-watcher.log`** to see:
   - Parse results from `/parse_only`
   - Preview output (shifts, amounts, transcript)
   - Any errors from the engine
4. Use `tail -n 50 logs/cpm-approval-watcher.log` to see recent output
5. Use `cat logs/cpm-approval-watcher.log` to see full log

## Command Runner Convention

When I say **"Run command #N"** (e.g., "Run command #1", "Run command #42"):

1. Look in `claude_commands/`
2. Find the file starting with `N_` (e.g., `1_setup_drive_symlinks`)
3. Read the file contents
4. Execute the shell commands contained in it
5. Report results

Example: "Run command #1" → read and execute `claude_commands/1_setup_drive_symlinks`

## Batch Command Runner

When I say **"Run commands #X-Y"** (e.g., "Run commands #2-7"):

### Phase 1: Plan (MANDATORY)
Before executing anything, output a plan showing:
1. **Command list** — Each command number, filename, and one-line purpose
2. **Dependency chain** — Which commands must complete before others
3. **Reference impact** — Files that will need import/path updates after moves/renames
4. **Approval gates** — Which commands require per-change approval (pause points)
5. **Risk assessment** — What could break, what's irreversible
6. **Expected end state** — What the repo looks like after all commands complete

Format:
```
BATCH PLAN: Commands #X-Y
================================
| # | Command | Purpose | Depends On | Approval? |
|---|---------|---------|------------|-----------|
| 2 | ... | ... | — | No |
| 3 | ... | ... | #2 | No |
...

REFERENCE IMPACT:
- [ ] Files with imports to update: [list]
- [ ] Files with path references to update: [list]
- [ ] Config files affected: [list]

RISK ASSESSMENT:
- [list risks]

END STATE:
- [describe final structure]

Approve this plan? (yes/no/modify)
```

### Phase 2: Execute
Only after plan approval:
1. Run commands sequentially
2. Report result after each command
3. Stop at any approval-gate command and wait for per-change approvals
4. If any command fails, STOP and report — do not continue
5. After file moves/renames, automatically queue reference updates for approval

### Phase 3: Verify
After all commands complete:
1. Show final directory structure
2. Confirm expected end state matches actual
3. Flag any anomalies (broken imports, dangling references)

### Phase 4: Log
Create a changelog entry at `docs/changelogs/YYYY-MM-DD_batch_X-Y.md` containing:
- Timestamp
- Commands executed
- Files created/moved/renamed/deleted
- References updated (old → new)
- Any errors encountered
- Final verification status
