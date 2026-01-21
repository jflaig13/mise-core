# Mise Swarm - Multi-Window Task Management

**Version:** 1.0
**Last Updated:** 2026-01-20

## Overview

The Mise Swarm is a file-based task management system for Claude Code that enables parallel development across multiple windows. Instead of a traditional task queue database, Swarm uses simple markdown files in designated directories to coordinate work across up to 6 simultaneous Claude Code windows.

## Quick Start

### Running a Task Queue

```bash
# User creates a task file
echo "# Fix typo in README\n..." > ~/mise-core/claude_commands/ccw1/fix_typo.md

# User triggers execution
# In Claude Code: "Run the ccw1 command"

# Claude reads, executes, archives the task
# Result: Task completed and moved to ccw1/archive/
```

### Checking Queue Status

```bash
# See pending tasks in a window
ls ~/mise-core/claude_commands/ccw1/

# See completed tasks
ls -lt ~/mise-core/claude_commands/ccw1/archive/ | head -10
```

## Architecture

```
~/mise-core/claude_commands/
├── ccw1/     # Primary window (also called "ccqb")
├── ccw2/     # Testing window
├── ccw3/     # Documentation window
├── ccw4/     # Deployment window
├── ccw5/     # Hotfix window
└── ccw6/     # Research window
```

Each window directory contains:
- **`*.md` files**: Pending tasks (visible in main folder)
- **`archive/` folder**: Completed tasks (moved after execution)

## How It Works

1. **User creates task file** in appropriate window directory (e.g., `ccw4/deploy_fix.md`)
2. **User says "Run the ccw4 command"** to trigger execution
3. **Claude Code reads all `.md` files** in ccw4/ (alphabetically)
4. **Claude executes each task** sequentially
5. **Claude moves completed files** to ccw4/archive/
6. **Claude reports results** for each task

## Window Assignments

| Window | Purpose | Typical Tasks |
|--------|---------|---------------|
| ccw1 (ccqb) | Primary development | Features, refactoring, general dev work |
| ccw2 | Testing & validation | Writing tests, running test suites, QA |
| ccw3 | Documentation | Specs, READMEs, workflow docs |
| ccw4 | Deployment | Building, deploying, traffic switching |
| ccw5 | Bug fixes | Hotfixes, urgent bugs |
| ccw6 | Research | Exploration, prototyping, investigation |

**Note:** These are guidelines - tasks can go in any window based on availability.

## Task File Format

Each task file (`.md`) should contain:

### Required Sections
- **Title/Header**: Brief description of the task
- **Context**: Why this task is needed
- **Actions**: Step-by-step instructions for Claude
- **Success Criteria**: How to verify completion

### Example Task File

```markdown
# Deploy Name Normalization Fix

## Context
Production bug: Claude hallucinating employee names instead of using roster.
Fix committed to payroll_prompt.py, needs deployment.

## Actions
1. Build transrouter: `gcloud run deploy --source .`
2. Switch traffic to new revision (100%)
3. Test with transcript containing "Mark" → should output "Mark Buryanek"

## Success Criteria
- Deployment completes without errors
- Traffic switched to new revision
- Name normalization test passes
```

## Common Workflows

### Single Task Execution

```bash
# Create task
echo "..." > ~/mise-core/claude_commands/ccw1/task.md

# Execute (in Claude Code window)
User: "Run the ccw1 command"

# Claude:
# - Reads task.md
# - Executes actions
# - Moves to archive/
# - Reports: "✓ Completed task.md"
```

### Sequential Multi-Task

```bash
# Create numbered tasks for explicit ordering
~/mise-core/claude_commands/ccw2/
  1_write_tests.md
  2_run_tests.md
  3_fix_failures.md

# Execute (in Claude Code window)
User: "Run the ccw2 command"

# Claude executes 1 → 2 → 3 in order
```

### Parallel Execution

```bash
# Distribute independent tasks across windows
ccw1/update_lpm.md
ccw2/test_cpm.md
ccw3/write_inventory_spec.md

# Open 3 Claude Code windows, run each:
Window 1: "Run the ccw1 command"
Window 2: "Run the ccw2 command"
Window 3: "Run the ccw3 command"

# All 3 execute in parallel
```

## Best Practices

### Task Design
- ✓ One task per file (clear separation of concerns)
- ✓ Descriptive filenames (`deploy_hotfix.md` not `task.md`)
- ✓ Include success criteria (enables verification)
- ✓ Self-contained tasks (all context in the file)

### Window Management
- ✓ Use window assignments as guidelines (ccw4 for deploys, ccw2 for tests)
- ✓ Avoid modifying same file in multiple windows simultaneously
- ✓ Put dependent tasks in same window (guaranteed sequential execution)

### Archive Hygiene
- ✓ Never delete archive files (full audit trail)
- ✓ Let Claude handle archiving (automatic on completion)
- ✓ Review archives periodically for patterns/insights

## Integration with Mise

### Brain Integration
The Swarm workflow is integrated into Mise's file-based intelligence system:
- **Workflow Master**: `workflow_specs/SWARM/SWARM_Workflow_Master.txt`
- **Changes Tracking**: `workflow_specs/SWARM/workflow_changes/`
- **Brain Loading**: `transrouter/src/brain_sync.py` includes Swarm domain

### Other Workflows
Swarm coordinates development across all Mise domains:
- **LPM** (Local Payroll Machine) - Local payroll processing
- **CPM** (Cloud Payroll Machine) - Cloud payroll engine
- **LIM** (Local Inventory Machine) - Inventory management
- **Transrouter** - API routing and domain coordination

## Aliases & Terminology

- **ccqb** = **ccw1** (same directory, different names used in conversation)
- **Command Queue Board (ccqb)** = Primary window alias
- **Worker Window** = Any ccw window (ccw1-6)
- **Task** = Markdown file in a ccw directory
- **Archive** = Completed task moved to archive/ folder

## Troubleshooting

### Task Not Executing

**Problem:** User says "Run the ccw1 command" but nothing happens

**Solutions:**
1. Check if task files exist: `ls ~/mise-core/claude_commands/ccw1/`
2. Verify files have `.md` extension
3. Ensure files are readable: `cat ~/mise-core/claude_commands/ccw1/task.md`

### Task Stuck in Queue

**Problem:** Task file not being archived after completion

**Solutions:**
1. Task may have failed mid-execution (check Claude's error output)
2. Success criteria may not have been met
3. Manually verify and move to archive if appropriate

### Duplicate Work

**Problem:** Same task running in multiple windows

**Solutions:**
1. Check all ccw folders for duplicate task files
2. User should distribute tasks carefully to avoid conflicts
3. If conflict detected, Claude should flag and ask for clarification

## Examples

See `SWARM_Workflow_Master.txt` for detailed examples including:
- Example 1: Simple single-window task (typo fix)
- Example 2: Multi-file sequential task (test suite)
- Example 3: Deployment task (hotfix deployment)

## References

- **Full Specification**: `SWARM_Workflow_Master.txt`
- **Workflow Changes**: `workflow_changes/` directory
- **Brain Integration**: `../../transrouter/src/brain_sync.py`
- **Claude Instructions**: `../../CLAUDE.md`
- **Other Workflows**: `../LPM/`, `../CPM/`, `../LIM/`, `../transrouter/`

## Changelog

### v1.0 (2026-01-20)
- Initial Swarm workflow specification
- Established ccw1-6 architecture
- Created command queue protocol
- Integrated with Mise brain system

---

**Maintained by:** Mise Development Team
**Questions?** See `SWARM_Workflow_Master.txt` or consult `CLAUDE.md`
