# Mise Moat Memo

**Why Mise Is Hard to Copy**

---

## Why This Exists

Investors ask about moats. Fair question — especially for AI companies, where the fear is that anyone can clone you with a weekend and an API key.

This document answers one question: **What specifically makes Mise defensible?**

Not philosophy. Not theory. Concrete moats that compound over time.

---

## Mise's Five Moats

### 1. Operational Truth Capture

Mise records how work actually happens — not how it should happen on paper.

Every voice memo captures the messy reality of restaurant operations: who actually worked, what really happened with tips, which product was actually counted. This creates a ground-truth dataset that can't be faked or reconstructed.

**Evidence:**
- 20+ consecutive weeks of real payroll at Papa Surf
- Zero payroll errors in production
- Every transcript, correction, and approval is logged

A competitor can build a demo. They can't build 20 weeks of operational history.

---

### 2. Workflow Ownership

Mise doesn't sit beside the workflow — it IS the workflow.

When a manager does payroll through Mise, they're not using Mise to help with payroll. They're doing payroll inside Mise. The system owns the process end-to-end: recording, parsing, calculating, approving, exporting.

**Evidence:**
- Papa Surf has fully replaced manual payroll with Mise
- Jon (the founder) uses it every week for his own restaurant
- There's no spreadsheet backup anymore — Mise is the system of record

You can't rip Mise out without recreating payroll from scratch. That's workflow ownership.

---

### 3. Domain-Encoded Logic

Thousands of micro-decisions are baked into Mise that a competitor would have to rediscover.

Examples:
- How tip pools work when 2 vs 3 servers share a shift
- How tipouts calculate based on food sales for expo, busser, utility roles
- How to handle split shifts, no-shows, and mid-shift role changes
- How to parse "Sarah" when the employee roster has "Sara" and "Sarah M."

This isn't documented anywhere. It's the accumulated knowledge of running payroll at a real restaurant for months. A competitor can't demo their way around this — they'd have to live it.

**Evidence:**
- Mise correctly handles Papa Surf's specific tip pool structure
- Name correction logic accounts for nicknames, typos, and ambiguous references
- Edge cases (split shifts, role changes mid-day) are already solved

---

### 4. Correction Compounding

Every time a manager corrects a parse, Mise gets smarter.

Did the system mishear "Sarah" as "Serra"? The manager fixes it. That correction becomes training signal. Over time, Mise learns the specific vocabulary of each restaurant — employee names, product names, local slang, brand variations.

This is a data flywheel. Competitors start at zero. We compound.

**Evidence:**
- Correction patterns at Papa Surf inform parsing logic
- Product catalog matching improves with each inventory session
- The system gets more accurate the longer it runs — not less

---

### 5. Human-in-the-Loop as Feature

Approval flows aren't a limitation — they're the product.

Restaurant managers don't want AI that "just handles it." They need to see what's happening before money moves. Mise is built around this: every payroll, every inventory count gets a preview and requires explicit approval.

This isn't a workaround for AI limitations. It's how trust works in ops-critical environments. Competitors who try to automate away the human will lose to competitors who make the human feel in control.

**Evidence:**
- Every Papa Surf payroll goes through manager preview and approval
- Managers catch and correct edge cases before submission
- This is the workflow managers actually want — not full automation

---

## Why Common AI Moat Fears Don't Apply

The "AI wrapper" fear assumes the product is just a thin interface on top of a model. That doesn't apply here.

**Mise is not a wrapper. It's a workflow system with AI inside.**

The value isn't the transcription or the LLM parsing — those are commodities. The value is:
- The specific domain logic encoded in the system
- The operational truth captured from real use
- The corrections and refinements accumulated over time
- The trust built with managers who rely on it weekly

A competitor can access the same models. They can't access Mise's operational history, domain encoding, or correction data. They'd have to earn those from scratch.

---

## Early Demand Signals

Let's be honest: Mise is early. But the signals are real.

Before any formal launch, marketing, or sales, inbound interest has already appeared. One hospitality operator heard about Mise organically and reached out asking: "How quickly could you have me up and running?"

That's one conversation. It's anecdotal. But the question wasn't theoretical — it was practical and urgent. That's exactly how real demand starts.

Multiple people have independently mentioned that others in their network are excited once they hear Mise explained. Payroll and inventory are persistent pain points. Nobody loves their current solution.

We're not manufacturing interest. We're converting pull that already exists.

---

## How We Deliberately Deepen These Moats

Every decision at Mise is filtered through one question: **Does this make us harder to copy?**

- **Capture more operational truth** — expand to more restaurants, more workflows, more edge cases
- **Own more of the workflow** — don't integrate with payroll providers, become the payroll system
- **Encode more domain logic** — every edge case solved is a moat deepened
- **Compound more corrections** — every user interaction makes the system smarter
- **Build more trust** — approval flows, transparency, and reliability earn the right to handle more

Moats are not chosen. They're earned through execution.

---

*Mise: Everything in its place.*
