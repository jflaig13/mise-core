TITLE
CLAUDE CODE ONBOARDING SUMMARY (LOCAL, OFFLINE STATE)

STATUS
CANONICAL

DATE ADDED
2024-12-12 (mmddyy filename: 121224)

SOURCE
Jon request — onboarding Claude Code

PURPOSE
Provide Claude Code with a concise, file-based starting point to continue work locally while pushes are blocked. Summarizes mandatory protocols, values, current branch state, and outstanding items.

KEY PROTOCOL FILES TO READ FIRST
- docs/brain/121224__system-truth-how-mise-works.md (file-based intelligence; memory only in repo; overrides all)
- docs/brain/121224__absolute-memory-rule.md (no ephemeral learning; every permanent instruction requires new mmddyy brain doc)
- docs/brain/121224__brain-ingest-protocol.md (19-section ingest, mmddyy naming, approval token apostrophe "'", triggers list)
- docs/brain/121224__workflow-primacy-directive.md (load workflows at startup; no re-asking answered questions)
- values.md / VALUES_CORE.md (core values, operationalization, competitive advantage, brain ingest reference)
- push_backlog.md (offline commits awaiting push; changelog of protocol/token updates)

CURRENT APPROVAL TOKEN
- Single apostrophe: "'"

NAMING
- Brain docs: mmddyy__<slug>.md in docs/brain/

BRANCH/STATE
- Branch ahead of origin; pushes blocked (DNS: github.com resolve failure).
- Committed offline: Transrouter v1 pipeline; inventory catalog rebuild; values/competitive advantage; brain ingest/absolute memory/system truth/workflow primacy; approval token changes.

OUTSTANDING/UNTRACKED ITEMS
- Untracked: AI_Configs/, mise_inventory/113025_Inventory.txt, mise_inventory/113025_Inventory_formatted.txt, transcripts/113025_Inventory_2.txt, transcripts/120125_120725.{json,srt,tsv,txt,vtt}, transcripts/archive/approve_120125_120725.approve.json.
- Deleted pending rebuild: data/Inventory/113025_inventory_output.json (blocked by missing rapidfuzz install due to network).

WORKFLOWS
- Claude must load canonical workflows (LPM/CPM/LIM/transrouter specs, naming, schemas, approval flows) before reasoning; do not re-ask answered questions.

ACTION EXPECTATION FOR CLAUDE CODE
- Honor all above protocols; create new brain docs for any permanent rule/change.
- Keep push_backlog.md updated when offline pushes are needed.
- Use apostrophe for preflight approvals.

CHANGELOG
- v1.0 (2024-12-12): Initial Claude Code onboarding summary.
