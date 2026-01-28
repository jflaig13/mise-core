# Claude Code Onboarding - Mise

Read this file to get up to speed quickly on the mise-core project.

## Step 1: Read Core System Files (in order)

1. **CLAUDE.md** - Initialization protocol, command runner convention, safety rules
2. **VALUES_CORE.md** - Core principles and immutable constraints
3. **docs/brain/121224__system-truth-how-mise-works.md** - File-based intelligence system
4. **docs/brain/121224__absolute-memory-rule.md** - No ephemeral memory; repo files are truth
5. **docs/brain/121224__workflow-primacy-directive.md** - Load workflows first, don't re-ask answered questions

## Step 2: Read Domain-Specific Workflow (choose one)

### For LPM (Local Payroll Machine):
- **workflow_specs/LPM/LPM_Workflow_Master.txt** - Complete LPM workflow and approval JSON spec
- **workflow_specs/roster/employee_roster.json** - Canonical employee name mappings

**Critical LPM Rules:**
- DEFAULT tip behavior = tip pooling (unless "NOT tip pooling" is explicitly stated)
- NEW approval files go in `/approvals/` (runner moves to `/archive/` after processing)
- Always normalize employee names using roster

### For CPM (Cloud Payroll Machine):
- **workflow_specs/CPM/CPM_Workflow_Master.txt** - Cloud payroll workflow

### For LIM (Local Inventory Machine):
- **workflow_specs/LIM/LIM_Workflow_Master.txt** - Local inventory workflow
- **inventory_agent/products/** - Product catalog source files

## Step 2.5: Check for Pending Plans

Check if there are active plan files:

```bash
ls -la ~/.claude/plans/ 2>/dev/null || echo "No plans directory"
```

If any `.md` files exist in `~/.claude/plans/`, ask the user:

**"I found pending plan files. Would you like me to execute them?"**

List the plan files found and let the user choose which one to execute.

**Example plans you might find:**
- Authentication implementation
- Feature additions
- Refactoring tasks
- Bug fixes

If the user says yes, read the plan file and execute it step-by-step.

## Step 3: Check Recent Work (optional)

```bash
git log --oneline -10
```

Shows recent commits and changes.

## Step 4: Signal Ready

After reading the above files, say:

**"Ready for work. What do you need?"**

---

## Architecture Overview

Mise is a multi-agent restaurant ops system:
- **Transrouter** coordinates domain agents
- **Payroll Agent** (LPM + CPM)
- **Inventory Agent** (LIM)
- **Future agents:** Ordering, Scheduling, Forecasting, General Ops

Each agent has file-based intelligence with Claude Code integration.

---

## Quick Reference

**Key Directories:**
- `payroll_agent/LPM/` - Local payroll machine (transcripts, approvals, runner)
- `payroll_agent/CPM/` - Cloud payroll machine
- `inventory_agent/` - Inventory processing
- `workflow_specs/` - Master workflow specifications
- `docs/brain/` - System truth and memory rules
- `claude_commands/` - Command runner scripts

**Key Concepts:**
- File-based intelligence (no ephemeral memory)
- Workflow primacy (load workflows first)
- Brain docs override all other instructions
- Git is source of truth for code
- GitHub is primary backup (not Google Drive)
