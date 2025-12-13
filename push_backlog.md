# Push Backlog (offline changes)

Tracking commits and work done while GitHub push is blocked (e.g., network/DNS issues). Push these when connectivity is restored.

- 6686613: Implement Transrouter v1 pipeline (orchestration, ASR providers, classifier, entities, routing stubs, tests).
- 066fd97: Rebuild inventory catalog from product CSVs (regenerate data/inventory_catalog.json from mise_inventory/products, include only “On Inventory” = Yes).
- 154a38f: Add push backlog log for offline changes.
- c580965: Add canonical values artifacts and backlog entries (values.md, VALUES_CORE.md; backlog updated).
- c595b02: Add brain ingest protocol and reference in values.
- 93a5a8e: Update push backlog for brain ingest and values.
- 5b6c06c: Set preflight approval token to z.
- 5f09859: Update brain ingest protocol with spacebar approval (superseded by apostrophe).
- docs/brain/121224__brain-ingest-protocol.md: Brain ingest protocol (mandatory, 19-section structure, mmddyy naming; approval token now apostrophe "'").
- values.md/VALUES_CORE.md: Updated with brain ingest reference, operationalization, and competitive advantage.

Untracked items to reconcile later:
- transcripts/113025_Inventory_2.txt
- transcripts/120125_120725.{json,srt,tsv,txt,vtt}
- transcripts/archive/approve_120125_120725.approve.json
- AI_Configs/ (contents not tracked)
- data/Inventory/113025_inventory_output.json deleted (pending rebuild when rapidfuzz available)
