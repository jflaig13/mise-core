# Agent Policy (All Coding Agents: Claude, Gemini, Codex, etc.)

First: **Learn my rules.** Before coding, read:
- Root onboarding: README.md
- Workflow-specific doc:
  - CPM: workflow_specs/CPM/README.md
  - LIM: workflow_specs/LIM/README.md
  - LPM: workflow_specs/LPM/LPM_Workflow_Master.txt
- Spec template (if drafting specs): ./get_workflow
- Critical path map: workflow_specs/CRITICAL_PATHS.md
- Workflow rules (all workflows, including future): workflow_specs/README.md
- Transcribe depends on .venv/bin/whisper; if missing, run .venv/bin/pip install openai-whisper

Scope & Boundaries
- Touch only the workflow you're assigned; read its doc first.
- Do not change schemas/workflows unless explicitly directed.
- Classify all changes by Tier and EDG before implementation — see `docs/brain/020726__engineering-risk-classification.md`.
- Keep base paths and env overrides intact (e.g., LPM_TRANSCRIPTS_BASE).
- Log workflow changes in the correct workflow_changes folder.
- Apply the same rules to all workflows (CPM/LIM/LPM/future): spec + critical paths + change log in workflow_specs/<WORKFLOW>/.
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
