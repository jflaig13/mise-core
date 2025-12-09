# Agent Policy (All Coding Agents: Claude, Gemini, Codex, etc.)

First: **Learn my rules.** Before coding, read:
- Root onboarding: README.md
- Workflow-specific doc:
  - CPM: transcribe/README.md
  - LIM: mise_inventory/README.md
  - LPM: transcripts/LPM_Workflow_Master.txt
- Spec template (if drafting specs): ./get_workflow

Scope & Boundaries
- Touch only the workflow you’re assigned; read its doc first.
- Do not change schemas/workflows unless explicitly directed.
- Keep base paths and env overrides intact (e.g., LPM_TRANSCRIPTS_BASE).
- Log workflow changes in the correct workflow_changes folder.
- No secrets in git. Use env vars or ignored .env files.

Commands & Safety
- Prefer rg for search; avoid destructive git (no hard resets, no schema rewrites without approval).
- No network or package install unless approved/directed.
- No destructive filesystem ops outside the repo.
- Keep outputs local; do not upload secrets.

Testing & Pushing
- Run relevant smoke/tests for the workflow before push.
- Push to main only when directed; otherwise branch/PR if protections are added.

Session Checklist
- Read the relevant workflow doc and this policy.
- Confirm paths/bases; respect naming conventions.
- Update change logs for workflow changes.
- Preserve deterministic behavior and logging paths noted in docs.
