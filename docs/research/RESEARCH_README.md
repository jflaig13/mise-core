# Mise Research Project

## What This Is

The Research project is a structured exploration workspace for Mise, Inc. It exists to investigate questions, evaluate options, and surface insights that may be useful to the company — across product, strategy, operations, legal, and technical domains.

Research outputs are **non-authoritative**. They inform decisions. They do not make them.

---

## What This Is Not

- **Not canon.** Nothing in this directory constitutes company policy, product specification, or institutional law.
- **Not the codebase.** This project does not write, modify, or deploy code. It does not touch `mise_app/`, `transrouter/`, `workflow_specs/`, or any production system.
- **Not the brain.** Files here are not part of `docs/brain/`. Brain files are canon. Research files are not.
- **Not self-enacting.** A research output may recommend a change. That recommendation has no force until a founder reviews it, approves it, and enacts it through the appropriate channel (Code project, brain file, legal document, etc.).

---

## How to Use Research Outputs

Each research output should be read as: "Here is what we found, here is what it might mean, and here is what we recommend — if anything."

When reading a research file:

1. **Treat findings as provisional.** They reflect the best available information at time of writing. They may be incomplete, outdated, or wrong.
2. **Check the date.** Research has a shelf life. Older findings should be re-validated before acting on them.
3. **Look for the recommendation section.** If the research suggests a concrete action, it will be stated explicitly. If no action is recommended, the research is informational only.
4. **Do not cite research as authority.** If a research insight needs to become policy, it must be promoted to canon first.

---

## How Insights Graduate to Canon

Research does not enact changes. It recommends them. The promotion path:

1. **Research identifies an insight** worth preserving or acting on.
2. **Research output states the recommendation** clearly, including what would change and where.
3. **A founder reviews the recommendation** and decides whether to act on it.
4. **If approved, the founder directs the change** through the appropriate channel:
   - Product/architecture changes go through the Code project.
   - Policy/strategy changes become brain files in `docs/brain/`.
   - Legal changes go through `legal/documents/` with proper review.
   - Workflow changes update the relevant spec in `workflow_specs/`.
5. **The research file remains as-is.** It is not modified to reflect the promotion. It stays in `docs/research/` as a record of the investigation.

Until step 4 happens, the insight is a suggestion. Nothing more.

---

## Relationship to the Mise Codebase

The Research project and the Code project are separate workspaces with different authorities:

| | Code Project | Research Project |
|---|---|---|
| **Can modify code** | Yes | No |
| **Can modify brain files** | Yes (with approval) | No |
| **Can deploy to production** | Yes (with approval) | No |
| **Can create research files** | Not its purpose | Yes |
| **Outputs are canon** | Yes, once merged | No |
| **Outputs are authoritative** | Yes | No |

Research may reference code, architecture, and brain files to inform its analysis. It does not alter them. If research determines that something in the codebase should change, it writes a recommendation. A founder decides whether to act on it.

---

## File Naming Convention

Research files in this directory should follow the pattern:

```
YYMMDD__short-descriptive-name.md
```

Example: `260207__case-conversion-logic-review.md`

This matches the brain file dating convention for consistency, while keeping research outputs in their own directory and clearly separated from canon.

---

## Summary

Research explores. Canon decides. The boundary is absolute.
