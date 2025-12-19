# Push Backlog (offline changes)

Tracking commits and work done while GitHub push is blocked (e.g., network/DNS issues). Push these when connectivity is restored.

- 3a32b24: Add catalog rebuild script with On Inventory filtering (scripts/rebuild_catalog.py; filters "On Inventory" = Yes; excludes food except Tajin; 164 products).
- 8096956: Add Claude Code onboarding summary.
- 217bfa1: Add workflow primacy directive.
- cb81ff1: Add foundational system truth file.
- fb2d219: Add 'Remember this:' trigger and absolute memory rule.
- 212b4a3: Add 'save that to your brain' trigger.
- f50d05f: Set preflight approval token to apostrophe.
- 5b6c06c: Set preflight approval token to z (superseded).
- 5f09859: Update brain ingest protocol with spacebar approval (superseded).
- 971d0c8: Enforce mmddyy brain ingest naming and restore values.
- 93a5a8e: Update push backlog for brain ingest and values.
- c595b02: Add brain ingest protocol and reference in values.
- c580965: Add canonical values artifacts and backlog entries.
- 0a5ea1a: Add inventory transcript formatter script.
- 154a38f: Add push backlog log for offline changes.
- 066fd97: Rebuild inventory catalog from product CSVs (regenerate data/inventory_catalog.json from inventory_agent/products, include only "On Inventory" = Yes).
- 6686613: Implement Transrouter v1 pipeline (orchestration, ASR providers, classifier, entities, routing stubs, tests).
- c580965: Add canonical values artifacts and backlog entries (values.md, VALUES_CORE.md; backlog updated).
- c595b02: Add brain ingest protocol and reference in values.
- 93a5a8e: Update push backlog for brain ingest and values.
- 5b6c06c: Set preflight approval token to z (superseded).
- 5f09859: Update brain ingest protocol with spacebar approval (superseded).
- f50d05f: Set preflight approval token to apostrophe (current token).
- 212b4a3: Add 'save that to your brain' trigger.
- fb2d219: Add 'Remember this:' trigger and absolute memory rule.
- cb81ff1: Add foundational system truth file.
- docs/brain/121224__brain-ingest-protocol.md: Brain ingest protocol (mandatory, 19-section structure, mmddyy naming; approval token apostrophe; triggers include “remember this:” and related phrases; absolute memory noted).
- docs/brain/121224__absolute-memory-rule.md: Absolute Memory Rule (no ephemeral learning; every permanent instruction must create a new brain doc).
- docs/brain/121224__system-truth-how-mise-works.md: System Truth — Mise is a file-based intelligence system; memory only exists in repo files; this rule overrides all others.
- docs/brain/121224__workflow-primacy-directive.md: Workflow Primacy Directive — No Rediscovery (must load workflows at startup; no re-asking answered questions; workflows are authoritative).
- values.md/VALUES_CORE.md: Updated with brain ingest reference, operationalization, and competitive advantage (unchanged in this batch).

Untracked items to reconcile later:
- transcripts/113025_Inventory_2.txt
- transcripts/120125_120725.{json,srt,tsv,txt,vtt}
- transcripts/archive/approve_120125_120725.approve.json
- AI_Configs/ (contents not tracked)
- data/Inventory/113025_inventory_output.json deleted (pending rebuild when rapidfuzz available)
