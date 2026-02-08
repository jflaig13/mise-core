# Workflow Specs and Change Log Rules (All Workflows)

Applies to: CPM, LIM, LPM, and any future workflows.

For each workflow:
- Location: workflow_specs/<WORKFLOW>/
- Spec: README.md (or a master spec file, e.g., LPM_Workflow_Master.txt for LPM)
- Change log: workflow_specs/<WORKFLOW>/workflow_changes/ with dated files (MMDDYY_<slug>.txt) describing what changed, files touched, and why.
- Critical paths: see workflow_specs/CRITICAL_PATHS.md for the canonical file set; stay within your workflow.

When adding a new workflow:
- Create workflow_specs/<WORKFLOW>/
- Add README.md (or a master spec) describing purpose, workflow, parsing/logic rules, schemas, and coding guidelines.
- Create workflow_changes/ with a README.md describing how to log changes.
- Update workflow_specs/CRITICAL_PATHS.md with the new workflow’s key files and directories.
- Add a change-log entry for the addition itself.

General rules:
- Do not change schemas or workflows unless explicitly directed.
- Log every workflow-level change in its workflow_changes folder.
- Keep secrets out of git; use env vars or ignored .env files.
- Follow AGENT_POLICY.md and the root README.md before editing anything.
