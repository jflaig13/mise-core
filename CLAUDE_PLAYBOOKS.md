# Claude Operational Playbooks

These are operational protocols referenced from CLAUDE.md. Read them when triggered by the relevant command pattern.

---

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
