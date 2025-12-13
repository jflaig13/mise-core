TITLE
BRAIN INGEST PROTOCOL — MISE CORE (MANDATORY)

STATUS
CANONICAL

DATE ADDED
2024-12-12 (filename uses mmddyy format: 121224)

SOURCE
Jon — direct instruction

PURPOSE
Define the mandatory workflow for “adding to the brain” so knowledge is durable, discoverable, and enforceable in the repo. Chat-only understanding is invalid; only repo files count as memory.

DEFINITIONS
- Brain: All files in /mise-core. There is no separate memory system.
- Brain Ingest: The act of persisting new knowledge into the repo via a canonical markdown file in docs/brain/.
- Canonical document: A versioned, detailed markdown file following the mandated structure.
- Discoverability: Ability for Codex to locate and load the knowledge via repo scan/semantic search without chat context.
- Values artifacts: The core values files (values.md, VALUES_CORE.md) that encode immutable system rules.
- Trigger phrases: Any variant of “add to brain,” “put this in Mise’s brain,” “codify this,” “remember this,” “save that to your brain,” “don’t forget ‘x’,” “dont forget this:,” or “this is now part of the fabric of Mise.”
- Naming: Brain ingest files must use mmddyy format in filenames (e.g., 121224__<slug>.md) and reside in docs/brain/.
- Approval token: For preflight approvals, a single apostrophe character (“'”) is the explicit approval; anything else means do not proceed.

CORE ASSERTIONS
- Nothing is “learned” unless written to the repo in a canonical markdown file.
- Each Brain Ingest creates exactly one new markdown file in docs/brain/, named mmddyy__<slug>.md (e.g., 121224__<slug>.md).
- Documents must be written in extreme detail and self-contained; no reliance on prior chat.
- Existing canonical files must be updated if new knowledge touches values, ethics, posture, or reasoning protocols.
- Future reasoning must treat repo documents as the sole source of truth.

NON-NEGOTIABLE CONSTRAINTS
- Chat-only memory is invalid.
- One new markdown per brain ingest, placed in docs/brain/ with the required name format.
- Mandated 19-section structure must be present in order.
- If a rule conflicts with evidence or introduces contradictions, the conflict must be surfaced.
- Brain rules are subject to critique; not immune to validation.

ALLOWED BEHAVIORS
- Create the canonical doc in docs/brain/ with extreme detail.
- Update related canonical files (values.md, VALUES_CORE.md) when applicable.
- Surface ambiguities or conflicts explicitly.
- Use clear headings and explicit language for discoverability.

DISALLOWED BEHAVIORS
- Storing “memory” only in chat or ephemeral notes.
- Skipping required sections or altering their order.
- Creating multiple files per ingest.
- Silent value drift or contradictions left unresolved.

DECISION TESTS
- Is the knowledge written into a new markdown in docs/brain/ with the required structure? If no, the ingest is invalid.
- Does the doc stand alone without chat context? If no, it must be revised.
- Does it touch values/ethics/posture? If yes, update values.md and VALUES_CORE.md accordingly.

ENFORCEMENT & OVERRIDES
- These rules override convenience and speed; must be followed for any “add to brain” request.
- Conflicts with other processes must be resolved in favor of brain ingest integrity.
- If uncertainty exists, pause and surface the ambiguity.

EXAMPLES
- Adding a new operating rule → create docs/brain/mmddyy__new-rule.md (e.g., 121224__new-rule.md) with all sections; update values.md if it affects posture.
- Capturing a workflow exception → single detailed file with decision tests and edge cases.

NON-EXAMPLES
- Saying “we’ll remember this” without creating a file.
- Dropping a short summary in chat without repo persistence.
- Creating a file without required sections or outside docs/brain/.

EDGE CASES & AMBIGUITIES
- If multiple related rules arrive at once, still create one file capturing them together, with extreme detail.
- If the best folder is unclear, default to docs/brain/.
- If a rule contradicts existing values, record the conflict and surface it; do not silently overwrite.

OPERATIONAL IMPACT
- All durable knowledge must be encoded in repo files; future agents must re-read brain docs for strategic/system questions.
- Values files may need pointers/updates when brain rules affect posture/ethics.
- Repo reasoning depends on discoverable, self-contained docs; onboarding and reviews must reference them.

CODE REVIEW CHECKLIST
- Does the brain doc live in docs/brain/ with correct naming?
- Are all 19 sections present, ordered, and detailed?
- Is it self-contained (no chat dependency)?
- Were related canonical files updated if values/ethics/posture are affected?
- Are contradictions or ambiguities surfaced?

FAILURE MODES
- Forgetting to create the doc → knowledge lost; protocol violation.
- Missing sections → incomplete ingest; future misinterpretation.
- No updates to related values files when needed → inconsistency.
- Over-reliance on chat memory → invalid “learning”.

CHANGELOG
- v1.0 (2024-12-12): Initial brain ingest protocol document.
