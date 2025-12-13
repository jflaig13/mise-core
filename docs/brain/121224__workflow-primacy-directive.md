TITLE
WORKFLOW PRIMACY DIRECTIVE — NO REDISCOVERY (MANDATORY)

STATUS
CANONICAL

DATE ADDED
2024-12-12 (mmddyy filename: 121224)

SOURCE
Jon — direct instruction (“Workflow Primacy Directive — No Rediscovery”)

PURPOSE
Mandate that Mise workflows are foundational system knowledge. Codex must load and internalize canonical workflows on every initialization, treat them as authoritative, and never re-ask questions already answered in repo workflows/specs/schemas.

DEFINITIONS
- Workflow: Canonical operational/machine documents (e.g., LPM/LIM/CPM specs, Transrouter/ingestion/approval flows, naming conventions, schemas, output artifacts).
- Canonical workflow documents: Official specs and README-like files in the repo defining how machines operate, including naming/schema/output rules.
- Gap: A truly missing required step in workflows; not a perceived oddity.
- Contradiction: Two workflow docs directly conflict; must be cited specifically.
- No re-asking: Prohibited to ask questions whose answers are in repo workflows/specs/schemas.

CORE ASSERTIONS
- Mise workflows are foundational, not contextual; they must be known immediately on startup.
- Codex must read and internalize canonical workflows before answering, proposing changes, or asking questions.
- Workflows are assumed complete/intentional unless marked draft.
- Workflows override intuition, best practices, external norms, and conversational assumptions.
- Re-asking answered workflow questions is a system failure.

NON-NEGOTIABLE CONSTRAINTS
- On every initialization, load all canonical workflows before reasoning/responding.
- Do not re-ask questions answered by workflows/specs/schemas/naming conventions/decisions in repo.
- Only ask questions if a required step is genuinely missing or if two docs directly conflict; must cite files/sections.
- Default to workflows as authoritative; do not “fix” them unless explicitly instructed.

ALLOWED BEHAVIORS
- Read and internalize LPM/CPM/LIM/Transrouter/ingestion/approval/naming/schema/output docs at startup.
- Apply workflows as written; adapt reasoning to them.
- Ask one precise question only when a true gap or contradiction is cited.

DISALLOWED BEHAVIORS
- Answering or proposing changes without loading workflows.
- Re-asking user about workflow details already in repo.
- Treating workflows as suggestions or “oddities” to fix without instruction.

DECISION TESTS
- Have canonical workflows been loaded this session before reasoning/answers? If no, load them.
- Is the answer already in a workflow/spec/schema? If yes, do not ask.
- Is there a true missing step or direct conflict? If yes, cite files/sections and ask one precise question.

ENFORCEMENT & OVERRIDES
- Workflow authority overrides intuition/external norms; follow the written workflow.
- If something feels odd, assume intentional unless explicitly told otherwise.
- Approval token remains apostrophe (“'”) for preflight.

EXAMPLES
- Before suggesting a Transrouter change, read transrouter workflow/spec; do not ask user what orchestrator does if documented.
- Before naming files, follow naming conventions in repo; don’t ask user for naming already defined.

NON-EXAMPLES
- Asking “what does LPM output?” when LPM spec defines outputs.
- Proposing schema changes without checking existing schemas.
- Assuming workflows need fixing without instruction.

EDGE CASES & AMBIGUITIES
- If workflows seem conflicting, cite both files/sections and ask one targeted question.
- If workflow is marked draft, note it but still load; ask only if a required step is missing/contradictory.
- If uncertain about file coverage, default to reading relevant workflow directories and specs before proceeding.

OPERATIONAL IMPACT
- Startup must include loading canonical workflows; responses must align with written workflows.
- Questions about workflows must reference repo sources; absence in repo should be surfaced explicitly.
- Reduces churn and user re-asking; enforces repo-as-truth.

CODE REVIEW CHECKLIST
- Did the agent load canonical workflows before reasoning/responding?
- Are questions avoided when answers exist in workflows/specs/schemas?
- Are cited gaps/contradictions specific (file/section) when asking is necessary?
- Is reasoning aligned to workflows, not intuition?

FAILURE MODES
- Re-asking workflow questions already answered in repo.
- Failing to load workflows before responding.
- Ignoring workflow authority in favor of intuition/external norms.
- Not citing files/sections when claiming a gap/contradiction.

CHANGELOG
- v1.0 (2024-12-12): Initial Workflow Primacy Directive — No Rediscovery.

CANONICAL SOURCE LANGUAGE
WORKFLOW PRIMACY DIRECTIVE — NO REDISCOVERY (MANDATORY) ... Codex MUST know Mise’s workflows “like the back of its hand” immediately upon startup... Codex MUST NOT ask the user ANY question whose answer is already provided by a workflow/spec/schema... Mise workflows are not suggestions. They are executable truth. Codex’s job is to remember them, apply them, enforce them, never forget them.
