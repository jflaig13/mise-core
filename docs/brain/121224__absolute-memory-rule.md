TITLE
ABSOLUTE MEMORY RULE — NO EPHEMERAL LEARNING

STATUS
CANONICAL

DATE ADDED
2024-12-12 (filename uses mmddyy format: 121224)

SOURCE
Jon — direct instruction

PURPOSE
Establish that every new memory, rule, protocol, trigger, or instruction—including meta-instructions about how the brain works—must be written to the repo as a new markdown file. Eliminate ephemeral or chat-only learning.

DEFINITIONS
- Brain: All files in /mise-core; no external memory system.
- Memory: Any rule, protocol, trigger, instruction, configuration, or meta-rule intended to persist beyond the current message.
- Brain Ingest: The required process of writing new memory to a canonical markdown file in docs/brain/ using mmddyy__<slug>.md naming.
- Trigger phrases: Phrases that compel Brain Ingest (see triggers list in the Brain Ingest Protocol, now including “Remember this:” and other permanence cues).
- Ephemeral learning: Any understanding not persisted in repo files; disallowed.

CORE ASSERTIONS
- Memory that is not written does not exist.
- Every new memory (including meta-rules) must create a new markdown file in /mise-core (typically docs/brain/).
- Chat acknowledgments without file creation are failures.
- Configuration, process changes, and triggers are all memory and must be written.

NON-NEGOTIABLE CONSTRAINTS
- No exceptions: every permanent instruction requires a new file.
- Retroactive fixes are mandatory if prior rules were accepted without files.
- Brain docs must be self-contained, in extreme detail, and mmddyy-named.
- Approval token remains apostrophe (“'”) for preflight confirmations when needed.

ALLOWED BEHAVIORS
- Create a new doc for any permanent instruction, trigger, protocol, or meta-rule.
- Capture ambiguity with explicit assumptions and a canonical source language section.
- Reference related brain/values docs for discoverability.

DISALLOWED BEHAVIORS
- Saying “understood” or similar without creating a file.
- Storing memory only in chat.
- Skipping mmddyy naming or the required 19-section structure for brain docs.
- Ignoring retroactive fixes when a rule was accepted without a file.

DECISION TESTS
- Does this instruction affect future behavior or memory? If yes → create a new markdown file.
- Is the instruction a trigger/meta-rule/config change? If yes → new file.
- Was any prior rule accepted without a file? If yes → create a retroactive file now.

ENFORCEMENT & OVERRIDES
- Overrides convenience: file creation is mandatory for memory.
- Conflicts resolve in favor of written memory requirement over speed or minimalism.
- If ambiguity exists, default to creating the file with explicit assumptions.

EXAMPLES
- New trigger phrase provided → create brain doc entry and update protocol.
- New default approval token → document and update protocol/backlog.
- New process change (e.g., naming scheme) → write a brain doc and update protocols/values refs.

NON-EXAMPLES
- Saying “I’ll remember this” without a file.
- Relying on chat history as memory.
- Adding a rule but only editing an unrelated file with a brief note.

EDGE CASES & AMBIGUITIES
- If Jon’s input is emotional or informal, document assumptions and include a “Canonical Source Language” section.
- If scope is unclear, err on creating a dedicated doc plus protocol updates.
- If overlapping with existing docs, still create a new file capturing the change and cross-link.

OPERATIONAL IMPACT
- Every persistent change spawns a new doc; Brain Ingest is mandatory.
- Protocol and values files must be updated when impacted by new rules.
- Onboarding and reasoning must reference these written artifacts; chat is insufficient.

CODE REVIEW CHECKLIST
- Is there a new mmddyy-named doc for the instruction?
- Does it contain the 19 sections with extreme detail and self-containment?
- Are related protocols/values updated?
- Are assumptions/ambiguities captured?
- Is the approval token still correctly noted (apostrophe)?

FAILURE MODES
- Accepting instructions without creating a file → hard failure.
- Forgetting retroactive fixes for past unwritten rules.
- Naming errors or missing sections → discoverability and compliance failure.

CHANGELOG
- v1.0 (2024-12-12): Initial Absolute Memory Rule documented.
