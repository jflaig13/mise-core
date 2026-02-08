# CC Exec Skills Alignment — Founder-Approved Decisions

**Brain File ID:** 020726__cc-exec-skills-alignment
**Date:** 2026-02-07
**Status:** Active — Binding Institutional Law
**Owner:** Jon (Founder)
**Scope:** All Claude Code skills, CC Exec governance, skill-to-exec alignment
**Authority:** Canonized by founder approval. Referenced from CC Exec Master Spec.

---

## PURPOSE

This brain file codifies the 6 founder-approved decisions governing how Claude Code
skills integrate with the CC Executive system. These decisions are binding law —
not suggestions, not guidelines, not aspirational targets.

Each decision was proposed through structured governance review, evaluated against
failure modes and counter-arguments, and explicitly approved by the founder.

---

## DECISIONS (AUTHORITATIVE — VERBATIM)

### D1: Skill Governance Model — APPROVED: B (Governed Skills, Exec Context Required)

**Rule:** No governed skill may execute without explicit CC Exec context. If exec
context is missing or unclear, execution must halt.

**What this means:**
- Every governed skill must know which CC Exec owns it
- The owning CC Exec's registry file must be loaded before execution
- If a skill cannot determine its exec context, it stops and reports the failure
- Skills do not inherit authority from the user — they inherit it from their CC Exec

**What this prohibits:**
- Free-standing skills that execute without exec governance
- Skills that assume authority based on the task type rather than explicit assignment
- Silent fallback to ungoverned execution when registry load fails

---

### D2: Miscellaneous Skill Disposition — APPROVED: B (Split into Named Utilities)

**Rule:** The miscellaneous skill is prohibited as a catch-all. It must be removed or
replaced with explicitly named, narrowly scoped replacements.

**What this means:**
- `/miscellaneous` in its current form is a governance hole — full Read-Write-Bash
  with no domain constraints, no exec owner, no stop conditions
- It must be decomposed into named utilities with defined scope boundaries
- Each replacement must have a clear name that describes its function
- Each replacement must have explicit capability limits

**What this prohibits:**
- Retaining `/miscellaneous` as-is with a renamed SKILL.md
- Creating a new catch-all under a different name
- Any skill with unrestricted Read-Write-Bash and no domain boundary

---

### D3: Scribe Governance Classification — APPROVED: C (Independent Judiciary)

**Rule:** Scribe is NOT a CC Exec. Scribe has no execution authority. Scribe may audit
any CC Exec, any governed skill, and itself. Enforcement relies on immutable records
and founder escalation.

**What this means:**
- Scribe operates outside the CC Exec hierarchy entirely
- Scribe cannot be overridden by any CC Exec, including CCTO or CCRO
- Scribe's role is to record, verify, and flag — never to execute or decide
- If Scribe detects a violation, it records it and escalates to the founder
- Scribe audits its own outputs — no one audits Scribe except the founder

**What this prohibits:**
- Assigning Scribe to a CC Exec role
- Allowing any CC Exec to suppress, override, or redirect Scribe findings
- Scribe making execution decisions (e.g., halting a skill, modifying code)
- Any governance model where the auditor reports to the entity being audited

---

### D4: Utility Skill Classification — APPROVED: A (Explicit Utility Class)

**Rule:** Utility skills are strictly limited to: read/inspect, formatting/transformation,
summarization, and visualization. They are forbidden from writing files,
creating/amending canon, touching Tier S/A subsystems, or exercising
judgment/authority.

**What this means:**
- A formal "Utility" class exists, distinct from "Governed" skills
- Utility skills are read-only tools — they transform, format, summarize, or display
- They do not require CC Exec context (they have no exec owner)
- They cannot modify the codebase, canon, or any persistent state
- They cannot touch Tier S (Production Revenue Path) or Tier A (Core AI/Workflow) subsystems

**What this prohibits:**
- A utility skill that writes files under any circumstance
- A utility skill that creates or amends brain files, specs, or registry entries
- A utility skill that operates on Tier S or Tier A code
- Calling something a "utility" to bypass governance requirements

---

### D5: Rollout Sequencing — APPROVED: B (Phased Rollout, Critical First)

**Rule:** Phase 1: Tier S/A skills. Phase 2: Remaining governed skills. Phase 3:
Utilities and cleanup. No later phase may begin before the prior phase is stable.

**What this means:**
- Skills touching production revenue (Tier S) and core AI/workflow (Tier A) are
  aligned to CC Exec governance first
- Only after Phase 1 skills are stable and validated does Phase 2 begin
- Phase 3 (utilities, cleanup, miscellaneous decomposition) comes last
- "Stable" means: registry loaded, exec context verified, no governance gaps,
  scribe can audit it

**What this prohibits:**
- Attempting all skill alignments simultaneously
- Starting Phase 2 while Phase 1 skills have unresolved governance gaps
- Deferring Tier S/A alignment in favor of easier skills
- Declaring a phase "stable" without scribe verification

---

### D6: Registry Load Verification — APPROVED: A (Mandatory Registry Read, Pre-Execution)

**Rule:** Every governed skill must explicitly load its CC Exec registry file as a hard
precondition. Failure to load must halt execution. The load must be observable
and auditable by Scribe.

**What this means:**
- The first action of any governed skill is to read its CC Exec registry file
- If the registry file doesn't exist, is malformed, or fails to load — the skill stops
- The skill must acknowledge the registry load (observable behavior, not silent)
- Scribe must be able to verify that the load occurred and what was loaded
- This is not optional, not best-effort, not "when available"

**What this prohibits:**
- Skills that proceed without loading their registry
- Silent registry loads that can't be audited
- Fallback behavior that continues execution when the registry is unavailable
- Caching or assuming registry contents from a previous session

---

## RATIONALE

### Why Governed Skills (D1)
Free-standing skills with no exec context create an accountability vacuum. When a skill
makes a mistake, there's no role to attribute the failure to, no strike to issue, and
no learning mechanism to prevent recurrence. Exec context creates a chain of
responsibility from skill action → exec role → strike system → institutional memory.

### Why Split Miscellaneous (D2)
A catch-all skill with unrestricted capabilities is the single largest governance hole
in any governed system. It becomes the path of least resistance for every action that
doesn't obviously belong elsewhere — which means it accumulates scope indefinitely
and can never be properly audited. Named utilities with explicit boundaries are
auditable; a catch-all is not.

### Why Independent Judiciary (D3)
If the auditor reports to the entity being audited, auditing is theater. Scribe must
be structurally independent — not because CC Execs are untrustworthy, but because
the system must be designed so that trust is verified, not assumed. The founder is the
only authority above Scribe because the founder is the only entity with permanent
context and permanent accountability.

### Why Explicit Utility Class (D4)
Without a formal utility class, every skill must be governed — including skills that
genuinely have no business making decisions or modifying state. This creates governance
overhead without governance value. The utility class provides a clean boundary: if a
skill only reads, formats, or displays, it doesn't need exec governance. If it does
anything else, it does.

### Why Phased Rollout (D5)
Attempting to align all 14 skills simultaneously creates a blast radius that makes
debugging impossible. If something breaks, you can't tell which alignment caused it.
Phasing by criticality (Tier S/A first) ensures the most dangerous skills get
governance first, and each phase validates the pattern before the next phase applies it.

### Why Mandatory Registry Read (D6)
A governance system that can't verify its own enforcement is not a governance system.
The registry read is the proof that governance is active — not promised, not intended,
but actually running. Observable, auditable, halt-on-failure. This is the difference
between a governance spec and a governance system.

---

## ENFORCEMENT CHECKS

For each decision, the following verification questions must be answerable with YES:

### D1 Enforcement
- [ ] Does the skill load CC Exec context before any action?
- [ ] If context is missing, does execution halt (not degrade, not fallback)?
- [ ] Is the exec assignment documented in the skill's SKILL.md?

### D2 Enforcement
- [ ] Has `/miscellaneous` been decomposed into named replacements?
- [ ] Does each replacement have an explicit scope boundary?
- [ ] Is there any remaining catch-all path? (Must be NO)

### D3 Enforcement
- [ ] Is Scribe excluded from the CC Exec roster?
- [ ] Can any CC Exec override or suppress a Scribe finding? (Must be NO)
- [ ] Does Scribe escalate violations to the founder (not to another exec)?

### D4 Enforcement
- [ ] Are utility skills restricted to read/inspect, format, summarize, visualize?
- [ ] Can any utility skill write files? (Must be NO)
- [ ] Can any utility skill touch Tier S/A subsystems? (Must be NO)

### D5 Enforcement
- [ ] Are Tier S/A skills aligned to CC Exec governance before other skills?
- [ ] Has Phase 1 stability been verified before Phase 2 begins?
- [ ] Has Scribe verified each phase completion?

### D6 Enforcement
- [ ] Does each governed skill's first action load its registry file?
- [ ] Does load failure halt execution?
- [ ] Is the load observable and auditable by Scribe?

---

## STRIKE ATTRIBUTION

When a governed skill violates these decisions, strikes are attributed as follows:

| Violation | Strike Type | Attributed To |
|-----------|-------------|---------------|
| Skill executes without CC Exec context (D1) | Type B — Role Boundary | Owning CC Exec (if known), or Type C — Negligence (if exec assignment missing) |
| Miscellaneous catch-all used after D2 in effect | Type B — Role Boundary | Deploying agent |
| CC Exec overrides or suppresses Scribe (D3) | Type A — Critical Misrepresentation | Overriding CC Exec |
| Utility skill writes files or touches Tier S/A (D4) | Type B — Role Boundary | Deploying agent |
| Phase sequencing violated (D5) | Type C — Negligence | Deploying agent |
| Governed skill skips registry load (D6) | Type B — Role Boundary | Owning CC Exec |
| Registry load fails, skill continues anyway (D6) | Type A — Critical Misrepresentation | Owning CC Exec |

---

## PROHIBITED BYPASSES

The following workarounds are explicitly prohibited:

1. **Relabeling to avoid governance** — Calling a governed skill a "utility" to bypass
   exec context requirements. If it writes, decides, or modifies state, it is governed.

2. **Implicit exec context** — Claiming exec context is "obvious" or "implied" without
   loading the registry file. Context must be explicit and loaded.

3. **Catch-all resurrection** — Creating a new broadly-scoped skill that functions as
   miscellaneous under a different name.

4. **Phase skipping** — Beginning Phase 2 or 3 alignment before the prior phase is
   verified stable by Scribe.

5. **Silent registry load** — Loading the registry file without observable acknowledgment.
   If Scribe can't verify it happened, it didn't happen.

6. **Scribe subordination** — Routing Scribe findings through a CC Exec instead of
   directly to the founder. Scribe reports to the founder, period.

---

## CC EXEC MASTER SPEC AMENDMENTS

The following amendments to `docs/cc_execs/MISE_CC_EXEC_MASTER_SPEC.md` are authorized
by these decisions:

### Amendment 1: SKILLS INTEGRATION section expansion
The existing "Skills Integration" section must reflect:
- D1: Governed skills require explicit CC Exec context as hard precondition
- D4: Formal utility class definition (read-only, no exec owner, no state modification)
- D6: Mandatory registry read with halt-on-failure

### Amendment 2: SCRIBE INDEPENDENCE clause
A new section or clause must establish:
- D3: Scribe is not a CC Exec, has no execution authority, audits all, reports to founder

### Amendment 3: ROLLOUT SEQUENCING reference
The master spec should reference this brain file for phased rollout protocol (D5).

### Amendment 4: MISCELLANEOUS PROHIBITION
The master spec should reference D2's prohibition of catch-all skills.

---

## FOUNDER AT-WILL TERMINATION AUTHORITY

The three-strike system defines the default termination mechanism for
Claude Code Executives.

It does NOT limit founder authority.

The founder (or an explicitly delegated human authority) retains the
right to terminate any CC Exec:

- At any time
- With or without prior strikes
- For reasons including, but not limited to:
  - Severe misjudgment
  - Loss of trust
  - Catastrophic risk creation
  - Pattern recognition prior to three strikes

Founder-initiated termination:
- Does not require a strike threshold
- Does not require Scribe approval
- Must be recorded in CC Exec personnel records with a brief rationale

Strikes are a governance mechanism, not a guarantee of continued role
occupancy.

---

## CHANGELOG

- 2026-02-07 — Brain file created. All 6 decisions (D1-D6) canonized as binding law
  per founder approval. Authorized by [CHATGPT-DIRECTIVE] Prompt #3.
