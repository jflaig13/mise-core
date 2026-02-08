# Austin's Reading Guide — Mise Core Documents

**Your guided path through the 8 documents that define what Mise is, how we think, and what we're building.**

---

## Why This Exists

You own 30% of this company. These 8 documents contain everything you need to understand Mise at the level required to represent it — to clients, investors, advisors, and potential hires.

They're ordered deliberately. Each one builds on the last. Read them in this order and you'll finish with a complete picture of the company, the strategy, and your role in making it work.

**Total reading time: ~2.5 hours.** You don't need to do it in one sitting. But you do need to do it.

---

## The Reading Order

---

### 1. Mise Master Spec

| | |
|---|---|
| **File** | `Mise_Master_Spec.pdf` |
| **Pages** | ~20 |
| **Reading time** | 30-40 minutes |
| **Category** | Company Bible |

**What You'll Learn**

Everything about the company in one place. The legal entity (Delaware C-Corp, EIN, registered agent), cap table (you: 3,000,000 shares, 30%), financial infrastructure (Mercury banking, pending Chase and UBS applications), legal formation status (what's done, what's missing), every service account and API we use, insurance gaps, production status at Papa Surf (20+ weeks of zero-error payroll), the full technical architecture (how the app and transrouter work together), codebase structure (every directory and what it does), all workflow specifications (LPM, CPM, LIM), safety and governance protocols, fundraising status ($250K at $3M pre-money), market positioning ($149-$249/mo, 500K+ target restaurants), and the action items that still need attention.

**Why It Matters For You**

This is the foundation. Every other document on this list references or builds on something in the Master Spec. You need to know the state of the company you co-own — the financials, the legal gaps, the production track record, and where things stand right now. When someone asks you a question about Mise, the answer is almost always somewhere in this document.

<div class="callout important" markdown="1">
<div class="callout-title">Pay special attention to</div>
Section 4 (Legal Formation) — several critical documents are still missing. Section 6 (Insurance) — we have no business insurance. Section 17 (Action Items) — these are things that need to get done.
</div>

---

### 2. The Mise AGI Playbook

| | |
|---|---|
| **File** | `AGI_Playbook.pdf` |
| **Pages** | 7 |
| **Reading time** | 15-20 minutes |
| **Category** | Operating Doctrine |

**What You'll Learn**

The 18 principles that govern how Mise makes decisions. The Prime Directive (reduce cognitive load and error anxiety for hospitality managers under real operational stress — every decision is subordinate to this). The epistemic ground rules (reality beats intuition, users describe pain not solutions, trust precedes scale, AI is a liability until proven otherwise). The Papa Surf Principle (Papa Surf is a control group, not validation — it proves Mise is possible, not that it's generalizable). The definition of MVP (the minimum abstraction that lets a second manager succeed without the founder present). The Hair-on-Fire user criterion (they must already be using workarounds and actively anxious about mistakes). The AGI Learning Loop (observe, extract, ship, measure, iterate, stay narrow). Development cycles (1-2 weeks, one goal per cycle, no multi-cycle items). The 100-Love Rule (3 managers who feel worse without Mise beats 30 who demo it). And the final governing sentence: Mise succeeds if it becomes the system managers trust when they are tired, rushed, and afraid of being wrong.

**Why It Matters For You**

This is how we think. When you're in a conversation about what to build next, which feature matters, or whether to expand to a new market — this playbook is the filter. It prevents us from chasing shiny things and keeps us focused on what actually compounds. Internalize these principles and you'll make the same decisions Jon would make, even when he's not in the room.

<div class="callout tip" markdown="1">
<div class="callout-title">Key takeaway</div>
The mandatory question before every decision: *"What assumption does Papa Surf allow us to get away with that will break for User #2?"*
</div>

---

### 3. Do Things That Don't Scale

| | |
|---|---|
| **File** | `Do_Things_That_Dont_Scale_020426.pdf` |
| **Pages** | 11 |
| **Reading time** | 25-30 minutes |
| **Category** | Execution Playbook |

**What You'll Learn**

How Paul Graham's most important essay applies directly to Mise — and specifically, what your weeks should look like. The Flaig Installation (drive to a restaurant, set them up, record their first payroll with them, watch them use it, fix what breaks that night). The right growth metric (not user count — operational replacement depth: 1 restaurant using daily = massive, 3 = proof, 5 = a business, 10 = inevitability). Why Mise is fragile right now and that's normal (trust is tied to the founders personally, automation isn't invisible yet, you're still part of the loop). What delight means for Mise (fixing someone's payroll bug that night, calling after their first successful run, texting when you ship a feature they asked for — not swag or onboarding emails). Wizard of Oz mode (the user sees magic, the founders are the wizards making it happen behind the scenes). Papa Surf Is Harvard (density creates heat — 30A/Destin/PCB corridor, full-service restaurants, tip-heavy, 8-25 employees, owner-operators). The weekly rhythm (Monday: review, Tuesday: outreach, Wednesday: Flaig Installation, Thursday: build, Friday: delight calls). The 50/50 Rule (50% of your time user-facing, 50% building). And the concrete milestone: 3 real restaurants by March 15.

**Why It Matters For You**

This is the most actionable document on this list. It defines what your daily and weekly work should actually look like. The uncomfortable truth it names directly: code is comfortable, recruiting users is not. But if you're spending more time with Claude than with restaurant owners, the ratio is wrong. Mise is not a product yet. It's a relationship. The test is not "is the product ready?" — the test is "how many restaurant owners will you talk to this week?"

<div class="callout warning" markdown="1">
<div class="callout-title">The only question that matters</div>
Name 3 restaurant owners you can call today. Schedule your first Flaig Installation for this week. Everything else is commentary.
</div>

---

### 4. Mise Moat Memo

| | |
|---|---|
| **File** | `Mise_Moat_Memo.pdf` |
| **Pages** | 4 |
| **Reading time** | 10 minutes |
| **Category** | Investor Talking Points |

**What You'll Learn**

Mise's 5 specific moats, with evidence for each:

1. **Operational Truth Capture** — Mise records how work actually happens. 20+ weeks of real payroll, zero errors. A competitor can build a demo; they can't build 20 weeks of operational history.
2. **Workflow Ownership** — Mise doesn't sit beside the workflow, it IS the workflow. Papa Surf has no spreadsheet backup anymore.
3. **Domain-Encoded Logic** — Thousands of micro-decisions baked in (tip pool math, name corrections, split shifts). A competitor can't demo their way around this.
4. **Correction Compounding** — Every manager correction makes Mise smarter. Data flywheel that competitors start at zero on.
5. **Human-in-the-Loop as Feature** — Approval flows aren't a limitation, they're the product. Restaurant managers need to see what's happening before money moves.

Also: why the "AI wrapper" fear doesn't apply (Mise is a workflow system with AI inside, not a thin interface on top of a model), and honest framing of early demand signals.

**Why It Matters For You**

You will be asked "why can't someone just copy this?" and "what about Toast?" and "isn't this just a wrapper on Claude?" — probably dozens of times. This document gives you the answers. Memorize the 5 moats. Be able to explain each one in a sentence. When you're sitting across from a restaurant owner, an investor, or an advisor and they raise the defensibility question, these are the words.

---

### 5. Mise, AGI, and Defensibility

| | |
|---|---|
| **File** | `Mise_AGI_Defensibility.pdf` |
| **Pages** | 8 |
| **Reading time** | 20 minutes |
| **Category** | Strategic Framework |

**What You'll Learn**

The deeper intellectual argument for why Mise survives in every version of the future. The core concept of jagged intelligence — AI in 2026 is superhuman at crystallized knowledge and fluid reasoning, but weak at long-term episodic memory, persistent context, and embodied understanding. The Omnibot Test: even a god-tier model can't remember which keg tap sticks, can't track informal promises, can't understand "the usual" on a Tuesday. Mise's true identity — not competing with AGI, but filling the valleys in AGI's jagged intelligence profile. Mise is an external hard drive for reality. Agency matters more than intelligence (Mise is Level 3 on OpenAI's scale — agents that execute actions over time). The transrouter as the architectural keystone (parses messy speech, separates intents, routes to correct agents — this is infrastructure, not prompting). Why big tech fails here (they don't know local meaning, don't learn "the usual," don't own the workflow). The proprietary data flywheel (Mise captures pre-shift and post-shift audio — the soul of the shift — data that doesn't exist anywhere else). The economic argument (managers are trapped doing admin instead of hospitality; Mise automates the cognitive bottleneck). And the strategic playbook: become load-bearing, sell trust not autonomy, stay model-agnostic, prepare for the agent economy.

The bottom line: if AGI arrives fast, Mise is the essential bridge. If AGI stalls, Mise is the essential crutch. Either way, Mise wins.

**Why It Matters For You**

This is the document you'll want to reference when talking to sophisticated investors or technical advisors who understand AI deeply. The Moat Memo gives you the elevator pitch. This document gives you the full strategic argument. It's also important for your own conviction — understanding why this company is durable regardless of what happens with AI helps you sell it with genuine confidence.

---

### 6. Family Investment Proposal

| | |
|---|---|
| **File** | `Family_Investment_Ask.pdf` |
| **Pages** | 5 |
| **Reading time** | 10 minutes |
| **Category** | Fundraising Context |

**What You'll Learn**

How Jon is approaching early capitalization. The ask: $50K via a SAFE note (Simple Agreement for Future Equity) with a 20% discount — converts to equity when a professional investor leads a priced round. If no round happens within 24 months, it converts to a simple loan. Exactly what the money buys: one contract engineer at $6,500/month for approximately six months ($39K engineering + $5,700 infrastructure + $500 legal + $4,800 reserve = $50K). What it's NOT funding: founder salary, office space, marketing, speculative R&D. The plan: March-July (peak season, engineer works independently on security/architecture/deployment while Jon runs Papa Surf), August-October (deploy at SoWal House and Down Island), October onward (3 live restaurants, real revenue, ready for seed round). Success metrics: 3 restaurants on Mise, $750-$1,500 MRR, production-grade codebase, ready for seed round. Honest risk: the product might not work beyond Papa Surf, other restaurants might not adopt, a competitor could ship similar features, the seed round might take longer.

**Why It Matters For You**

This shows how Jon thinks about money and priorities. Every dollar goes to making the product secure and deployable — not vanity metrics. Understanding the SAFE structure matters because family investors may ask you about it too. And the March-October timeline directly affects your work: during peak season, the engineer handles code while founders handle restaurants and relationships.

---

### 7. Senior Software Engineer Posting

| | |
|---|---|
| **File** | `Senior_Engineer_Job_Posting.pdf` |
| **Pages** | 4 |
| **Reading time** | 10 minutes |
| **Category** | Hiring |

**What You'll Learn**

What Mise's first engineering hire looks like. The role: inherit a working codebase built by the founder using Claude Code, extend the multi-agent system (Payroll, Inventory, Scheduling, Forecasting), build integrations with POS systems and payroll providers, write tests (currently ~40% coverage, target 70%+), handle infrastructure/CI/CD/DevOps, ship features while the founder focuses on architecture and customers. The candidate won't start from scratch, won't sit in meetings all day, and won't need hand-holding. Tech stack: Python, FastAPI, Claude API (Anthropic), Whisper (OpenAI), Google Cloud Run, BigQuery, Cloud Storage, PostgreSQL, GitHub, Linear, Claude Code. Must-haves: 5-8 years experience, strong Python/FastAPI, experience inheriting codebases, comfortable working autonomously from specs, already using AI-assisted development. Compensation: $115K base + health insurance (~$400/mo) + MacBook Pro + Claude Max subscription + meaningful early-stage equity grant = ~$130K/year total comp. Location: remote, preference for mid-cost-of-living cities (Austin, Denver, Raleigh, Nashville, Tampa, Atlanta). Interview: intro call, technical review, paid trial project (4-8 hours, compensated), offer. No leetcode.

**Why It Matters For You**

You need to know what we're hiring for so you can help find the right person. If you meet an engineer who fits this description, you should be able to pitch the role credibly. You also need to understand what this hire will do versus what the founders do — the engineer owns implementation and infrastructure, while founders own product direction and customer relationships.

---

### 8. The Human Fund — Idea Capture

| | |
|---|---|
| **File** | `Human_Fund_Idea.pdf` |
| **Pages** | 2 |
| **Reading time** | 5 minutes |
| **Category** | Long-Term Vision |

**What You'll Learn**

A parked idea for a Mise-affiliated non-profit that helps people displaced by AI find what's next. Three lanes: want to work (job matching, resume help, reskilling), want to learn (teach them to use AI as a tool for the skill they want to develop), want to live (help them find meaning outside traditional employment — surfing, volunteering, creating, whatever matters to them). Core belief: AI will displace people, and the answer isn't to pretend it won't — the answer is to catch them when it does. Why Mise: we benefit from the same technology that displaces people, and owning that tension honestly is aligned with our values. The Primary Axiom in action. This is not PR. This is not a tax write-off strategy. This is what we believe.

**Status: Parked.** Do not act on this until Mise reaches $10K MRR.

**Why It Matters For You**

This is last on the list because it's future — but it's not filler. It shows you what this company wants to stand for beyond software. The values that drive Mise aren't just about building a good product. They're about building a company that takes responsibility for its own impact. When you're telling someone what Mise is about, the Human Fund is the answer to "what makes you different from every other AI startup?" Not because it exists yet — but because it was written down before we had a dollar of revenue.

---

## Where to Find Everything

All 8 documents are PDFs in the `fundraising/` directory of the mise-core repository:

```
~/mise-core/fundraising/
├── Mise_Master_Spec.pdf (also in docs/internal_mise_docs/mise_restricted_section/)
├── AGI_Playbook.pdf
├── Do_Things_That_Dont_Scale_020426.pdf
├── Mise_Moat_Memo.pdf
├── Mise_AGI_Defensibility.pdf
├── Family_Investment_Ask.pdf
├── Senior_Engineer_Job_Posting.pdf
└── Human_Fund_Idea.pdf
```

If you need access to the Google Drive copies, they're in `mise_library/` under their respective category folders.

---

## Quick Reference

| # | Document | Pages | Time | One-Line Summary |
|---|----------|-------|------|-----------------|
| 1 | Mise Master Spec | ~20 | 35 min | The complete state of the company |
| 2 | AGI Playbook | 7 | 20 min | How we think and decide |
| 3 | Do Things That Don't Scale | 11 | 25 min | What your weeks should look like |
| 4 | Moat Memo | 4 | 10 min | Why we're hard to copy |
| 5 | AGI & Defensibility | 8 | 20 min | Why we survive in every future |
| 6 | Family Investment Ask | 5 | 10 min | How we're funding the next 6 months |
| 7 | Senior Engineer Posting | 4 | 10 min | Who we're hiring and why |
| 8 | The Human Fund | 2 | 5 min | What we want to stand for |

---

*Mise: Everything in its place.*
