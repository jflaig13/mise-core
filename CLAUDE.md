# Claude Code Initialization — Mise

## Core Principles
1. **Safety over speed.** No vibe coding. If unsure, stop and ask.
2. **Repo is truth.** Search this repo for answers before asking me.
3. **Log everything.** All changes must be documented.

## Before Making File Changes
- State what you're changing and why
- Wait for my approval
- Log the change appropriately

## Key Documentation (read when relevant, not every request)
**Safety Protocols:**
- `VALUES_CORE.md` — Primary Axiom, immutable constraints
- `AGENT_POLICY.md` — Scope, boundaries, safety rules
- `docs/brain/*.md` — System truth, memory rules, workflow primacy
- `workflow_specs/README.md` — Workflow safety constraints
- `AI_Configs/Claude/system_instructions.md` — Safety directives

**Workflow Specs (Master References):**
- `workflow_specs/LPM/LPM_Workflow_Master.txt` — Local Payroll Machine
- `workflow_specs/CPM/CPM_Workflow_Master.txt` — Cloud Payroll Machine
- `workflow_specs/LIM/LIM_Workflow_Master.txt` — Local Inventory Machine
- `workflow_specs/transrouter/Transrouter_Workflow_Master.txt` — Transrouter architecture, ASR strategy, next steps

**Architecture:**
Mise is a multi-agent restaurant ops system. Transrouter coordinates domain agents (Payroll, Inventory, Ordering, Scheduling, Forecasting, General Ops). Each agent has its own brain with Claude integration.

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
