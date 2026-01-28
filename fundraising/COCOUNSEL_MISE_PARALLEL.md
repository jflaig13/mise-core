# The CoCounsel-Mise Parallel

**A Complete Strategic Framework for 2026–2035**

---

## Part 1: The Core Thesis

### The $650 Million Validation

Thomson Reuters acquired Casetext (CoCounsel) for $650 million in cash in August 2023. This wasn't an acqui-hire or a technology play—it was a strategic acquisition of a company that had cracked the code on AI for professional work.

**The thesis:** If AI can do legal work reliably enough that lawyers trust it with their careers, AI can do restaurant operations reliably enough that operators trust it with their businesses.

Both domains share the same fundamental challenge: professionals drowning in administrative work that prevents them from doing what they're actually good at. Lawyers want to practice law, not do document review. Restaurant operators want to run restaurants, not calculate tipouts at 2am.

**CoCounsel proved the architecture. Mise is applying it to a market with identical pain and zero existing solutions.**

---

## Part 2: Architectural Parallels (The "How")

### 2.1 Skills-Based Workflow Engine, Not Chatbot

**CoCounsel's Approach:**
CoCounsel is not a chatbot you ask questions to. It's a skills-based system where each "skill" is a purpose-built workflow for a specific legal task: document review, deposition preparation, contract analysis, legal research. Users don't prompt—they invoke skills with structured inputs and receive structured outputs.

**Mise's Implementation:**
Mise is not a chatbot you ask questions to. It's a domain agent system where each agent handles a specific operational workflow: Payroll Machine for compensation, Inventory Agent for stock management, Closeout Agent for end-of-day reconciliation. Operators don't prompt—they speak naturally about their day, and Transrouter invokes the right agents with structured inputs.

**Why This Matters:**
Chatbots are unpredictable. Professional work requires predictability. By constraining AI to specific workflows with defined inputs and outputs, you get:

- Consistent results
- Auditable processes
- Testable behavior
- Professional-grade reliability

**Pitch Language:**

> "CoCounsel isn't ChatGPT for lawyers—it's a system of specialized legal skills. Mise isn't ChatGPT for restaurants—it's a system of specialized operational agents. The architecture that made AI trustworthy for lawyers is the same architecture we're using for restaurants."

---

### 2.2 Grounding and Faithfulness Over General Knowledge

**CoCounsel's Approach:**
Jake Heller (CoCounsel CEO) used the "QAnon Shaman" example to illustrate grounding. When asked about the case, CoCounsel doesn't speculate from general knowledge—it only responds based on actual case documents in its context. If the documents don't contain information about sentencing, CoCounsel says so rather than hallucinating an answer.

This is critical for legal work where a wrong citation or fabricated precedent could destroy a case and a career.

**Mise's Implementation:**
When asked about payroll, Mise doesn't calculate from assumptions—it only responds based on actual POS data, time clock records, and tip reports. If data is missing (an employee forgot to clock out), Mise flags it rather than guessing.

Every output is grounded in:

- Toast POS transaction data
- Time clock records
- Configured tip pool rules
- Historical patterns (for anomaly detection)

**Why This Matters:**
Restaurant payroll has the same "one mistake destroys trust" dynamic as legal work:

- Underpay an employee → Department of Labor complaint
- Miscalculate tips → Staff revolt
- Miss overtime → Lawsuit
- Wrong tax withholding → IRS problems

**Pitch Language:**

> "CoCounsel's breakthrough was grounding—AI that only responds based on actual documents, never hallucination. Mise applies the same principle: every payroll calculation is grounded in your actual POS data and time records. We don't guess. We don't assume. If data is missing, we tell you."

---

### 2.3 Human-in-the-Loop as Feature, Not Bug

**CoCounsel's Approach:**
CoCounsel doesn't file motions automatically. It prepares documents for lawyer review. The lawyer remains the decision-maker, the licensed professional who signs off. CoCounsel is the highly capable assistant that does the grunt work, but the human is always in control.

This isn't a limitation—it's the design. Lawyers need to be accountable for their work. CoCounsel makes them more efficient without removing their judgment.

**Mise's Implementation:**
Mise doesn't submit payroll automatically. It prepares everything for manager approval:

- Reviews the calculations
- Presents the summary
- Flags anomalies
- Waits for explicit "approved" before anything moves

The manager remains the decision-maker. Mise is the highly capable assistant that does the grunt work, but the human is always in control.

**Why This Matters:**
This solves the trust problem. Operators don't have to wonder "what did the AI do?" They see exactly what's proposed, why, and approve it themselves. If something's wrong, they catch it before it matters.

It also solves the liability problem. The operator made the decision. Mise provided the analysis. Clear accountability.

**Pitch Language:**

> "CoCounsel doesn't replace lawyers—it makes them faster. The lawyer reviews everything before it goes out. Mise doesn't replace managers—it makes them faster. You review everything before payroll runs. Same architecture, same accountability model, same trust framework."

---

### 2.4 Task-Based Model Routing

**CoCounsel's Approach:**
CoCounsel doesn't use one model for everything. Different legal tasks have different requirements:

- Document review needs high accuracy on classification
- Legal research needs broad knowledge and citation accuracy
- Contract analysis needs precise extraction

CoCounsel routes tasks to the right model (or model configuration) based on what the task requires.

**Mise's Implementation:**
Transrouter is explicitly designed for this. Different operational tasks have different requirements:

- Payroll calculations need mathematical precision and rule compliance
- Natural language intake needs conversational understanding
- Anomaly detection needs pattern recognition

Transrouter analyzes the input and routes to the appropriate domain agent with the appropriate model configuration.

**Why This Matters:**
One-size-fits-all AI is mediocre at everything. Task-specific routing means:

- Better accuracy per task
- Lower costs (use expensive models only when needed)
- Optimized latency per workflow
- Easier testing and improvement

**Pitch Language:**

> "CoCounsel uses different AI configurations for different legal tasks—document review is different from legal research. Mise's Transrouter does the same: payroll calculations use different processing than inventory forecasting. This isn't one chatbot trying to do everything. It's specialized agents orchestrated intelligently."

---

### 2.5 Evaluation Infrastructure as Competitive Moat

**CoCounsel's Approach:**
CoCounsel's real moat isn't the models—those are commoditizing. The moat is the evaluation infrastructure: thousands of test cases covering edge cases in legal work, regression suites that catch when model updates break existing functionality, domain-specific benchmarks that measure what actually matters for lawyers.

When a new model comes out, CoCounsel can evaluate it against their test suite in hours and know exactly how it performs on real legal tasks.

**Mise's Implementation:**
Every edge case at Papa Surf becomes a test case:

- Employee clocked in but forgot to clock out
- Manager gave verbal override on a tip pool
- Server worked double shift spanning two pay periods
- Cash tip reported after closeout
- Partial tip pool participation (employee opted out)

These accumulate into a regression suite that any competitor would need years to replicate.

**Why This Matters:**
Models will get better and cheaper. The evaluation infrastructure that ensures reliability on domain-specific tasks is the durable advantage. It's also the hardest thing to replicate—you can't fake real-world edge cases.

**Pitch Language:**

> "CoCounsel's moat isn't the AI—it's the thousands of legal test cases that ensure reliability. Our moat is the same: every weird edge case from real restaurant operations becomes a test case. That corpus of domain-specific evaluations is what makes the system trustworthy, and it's what competitors can't copy."

---

### 2.6 Clarification Over Guessing

**CoCounsel's Approach:**
When a lawyer's request is ambiguous, CoCounsel asks clarifying questions rather than guessing. "Do you want cases from all jurisdictions or just federal?" "Should I include dissenting opinions?"

This prevents the AI from confidently producing wrong output that wastes the lawyer's time.

**Mise's Implementation:**
When an operator's input is ambiguous, Mise asks clarifying questions:

- "I see Sarah worked a double but her clock-out is missing. What time did she leave?"
- "The tip pool calculation came out lower than usual. Did you want to exclude the private event tips?"
- "Marcus is showing 42 hours this week. Should I flag this for overtime review?"

**Why This Matters:**
Guessing creates errors. Errors destroy trust. Clarification takes an extra 30 seconds but prevents hours of cleanup.

**Pitch Language:**

> "CoCounsel asks clarifying questions instead of guessing—because a wrong assumption in legal work is catastrophic. Mise does the same. If something doesn't add up, we ask. We'd rather take 30 seconds to clarify than waste your time fixing errors."

---

### 2.7 Professional-Grade Outputs (Deliverables, Not Advice)

**CoCounsel's Approach:**
CoCounsel doesn't give legal advice ("you should file this motion"). It produces deliverables (the actual motion, ready for review). The output is the work product lawyers need, in the format they need it, ready for the next step in their workflow.

**Mise's Implementation:**
Mise doesn't give operational advice ("you should pay your employees"). It produces deliverables:

- Payroll-ready export file for Gusto/ADP
- Tip distribution sheets
- Cash reconciliation reports
- Audit-ready logs

The output is the work product operators need, in the format they need it, ready for the next step in their workflow.

**Why This Matters:**
Advice is cheap. Deliverables are valuable. Operators don't need to be told they should do payroll—they need the payroll done.

**Pitch Language:**

> "CoCounsel produces court-ready documents, not legal advice. Mise produces payroll-ready files, not suggestions. The output is the work product—ready for the next step."

---

## Part 3: Market Parallels (The "Where")

### 3.1 Professional Services Under Administrative Burden

**The Legal Market Before CoCounsel:**
Lawyers spent 60%+ of their time on administrative tasks: document review, research, contract analysis. This was work that required legal knowledge but not legal judgment. Associates billing $400/hour were doing work that should cost $40/hour.

**The Restaurant Market Before Mise:**
Operators spend hours every week on administrative tasks: payroll prep, tip calculations, inventory counts, closeout reconciliation. This is work that requires operational knowledge but not operational judgment. Managers earning $25/hour are doing work that should take minutes.

**The Parallel:**
Both professions have highly skilled people doing low-skill work because no tool exists to do it reliably.

**Pitch Language:**

> "Lawyers were spending $400/hour billing time on document review. Restaurant managers are spending their limited time on spreadsheet work. CoCounsel freed lawyers to practice law. Mise frees operators to run restaurants."

---

### 3.2 High-Stakes Error Environments

**Legal:**

- Missed citation → malpractice claim
- Wrong filing deadline → case dismissed
- Incorrect contract clause → multi-million dollar exposure

**Restaurant:**

- Underpaid employee → Department of Labor investigation
- Miscalculated tips → wage theft lawsuit
- Overtime violation → class action exposure
- Tax withholding error → IRS penalties

**The Parallel:**
Both domains have asymmetric risk: small errors cause massive consequences. This is why reliability matters more than features.

**Pitch Language:**

> "Legal malpractice claims can end careers. Restaurant wage violations can end businesses. Both domains require AI that's reliable enough to stake your livelihood on. That's why we built Mise the same way CoCounsel was built—reliability first."

---

### 3.3 Fragmented Technology Landscape

**Legal Before CoCounsel:**
Law firms used Westlaw for research, separate tools for document management, separate tools for time tracking, separate tools for billing. Nothing talked to anything else. Data lived in silos.

**Restaurants Before Mise:**
Restaurants use Toast for POS, separate tools for scheduling, separate tools for payroll, separate tools for inventory. Nothing talks to anything else. Data lives in silos.

**The Parallel:**
Both markets have tool sprawl with no integration layer. CoCounsel became the integration layer for legal work. Mise becomes the integration layer for restaurant operations.

**Pitch Language:**

> "Law firms had Westlaw, document management, time tracking, billing—none of it connected. Restaurants have POS, scheduling, payroll, inventory—none of it connected. CoCounsel became the AI layer that unified legal workflows. Mise is the AI layer that unifies restaurant operations."

---

### 3.4 Underserved by Existing Technology

**Legal:**
Westlaw and LexisNexis had been the standard for decades. They were research databases, not workflow tools. When AI arrived, they bolted on features rather than rethinking from first principles.

CoCounsel was AI-native—built from scratch around what AI could do, not constrained by legacy architecture.

**Restaurants:**
Toast and Square are POS systems with bolted-on features. They're transaction processors, not workflow tools. Their "AI features" are add-ons, not architecture.

Mise is AI-native—built from scratch around what AI can do for operations.

**Pitch Language:**

> "Westlaw adding AI features couldn't compete with CoCounsel built AI-native. Toast adding AI features can't compete with Mise built AI-native. The architecture matters."

---

### 3.5 Market Size Comparison

**Legal Market:**

- ~450,000 law firms in the US
- CoCounsel acquired for $650M
- Target: firms of all sizes, starting with smaller firms

**Restaurant Market (Mise's Target):**

- ~150,000 single-location full-service restaurants
- ~114,000 restaurants opened in past 3 years or opening soon (Mise's beachhead)
- 70% of all US restaurants are single-unit operations

**The Honest Framing:**
The markets are comparable in establishment count. The revenue per establishment is different (law firms bill more than restaurants gross), but the operational pain is identical.

**Pitch Language:**

> "There are 450,000 law firms in the US. There are 150,000 single-location full-service restaurants—our exact target. Both markets have the same problem: professionals drowning in admin work. CoCounsel proved the model works. We're applying it to comparable market size."

---

## Part 4: Strategic Parallels (The "Why")

### 4.1 Narrow Wedge, Then Expand

**CoCounsel's Path:**
CoCounsel didn't launch as "AI for all legal work." They started with legal research—a specific, high-value, well-defined task. Once they proved reliability there, they expanded to document review, contract analysis, deposition prep.

The wedge was narrow enough to execute well, valuable enough to prove the model, and expandable to adjacent workflows.

**Mise's Path:**
Mise isn't launching as "AI for all restaurant operations." We're starting with payroll—a specific, high-pain, well-defined task. Once we prove reliability there, we expand to inventory, scheduling, forecasting.

The wedge is narrow enough to execute well, valuable enough to prove the model, and expandable to adjacent workflows.

**Pitch Language:**

> "CoCounsel started with legal research, then expanded to document review, contracts, depositions. We're starting with payroll, then expanding to inventory, scheduling, forecasting. Same playbook: nail one workflow, prove reliability, expand from strength."

---

### 4.2 Pain-Driven Adoption

**CoCounsel:**
Lawyers adopted CoCounsel because document review was painful—hours of tedious work that associates hated and partners didn't want to pay for. The pain was acute and universal.

**Mise:**
Operators will adopt Mise because payroll prep is painful—hours of tedious work that managers hate and owners don't want to pay for. The pain is acute and universal.

**Pitch Language:**

> "Lawyers didn't adopt CoCounsel because AI is cool. They adopted it because document review at 2am sucks. Operators won't adopt Mise because AI is cool. They'll adopt it because calculating tipouts at 2am sucks. Pain drives adoption."

---

### 4.3 Founder-Market Fit

**CoCounsel:**
Jake Heller was a lawyer. He understood legal workflows from the inside. He knew what mattered and what didn't. He could build for lawyers because he was one.

**Mise:**
Jon is a restaurant operator. He understands restaurant workflows from the inside. He runs Papa Surf. He's done the 2am payroll runs. He knows what matters and what doesn't.

**Pitch Language:**

> "CoCounsel was built by lawyers who understood legal workflows. Mise is built by an operator who's done 2am payroll runs after 14-hour shifts. Founder-market fit matters."

---

### 4.4 Exit Path Validation

**CoCounsel's Exit:**
Thomson Reuters (owner of Westlaw) acquired CoCounsel for $650M. The strategic acquirer was the incumbent who couldn't build AI-native fast enough.

**Mise's Potential Acquirers:**

- Toast (dominant restaurant POS, $1B+ market cap)
- Square (SMB payment/operations platform)
- SpotOn (growing restaurant tech player)
- Gusto (payroll provider wanting vertical depth)
- ADP (enterprise payroll wanting restaurant expertise)

**Pitch Language:**

> "Thomson Reuters bought CoCounsel because building AI-native legal tools from scratch was harder than acquiring them. Toast, Square, Gusto—they'll face the same calculus. The exit path is proven."

---

## Part 5: Differentiation Arguments (The "Why Us")

### 5.1 Voice-First in a Screen-Last Environment

**What CoCounsel Didn't Need:**
Lawyers work at desks with screens. Text-based interfaces work fine.

**What Mise Requires:**
Restaurant operators work on their feet, hands full, in loud environments. They can't stop to type. Voice-first isn't a nice-to-have—it's a requirement.

**Mise's Advantage:**
Speech-to-JSON-to-deliverable is core architecture, not a feature. The operator talks through their day: "Sarah worked a double, Marcus left early, we had that private event..."

Transrouter converts this to structured data and routes to the right agents.

**Pitch Language:**

> "CoCounsel could be text-based because lawyers sit at desks. Restaurant operators are on their feet, hands full, in loud kitchens. Voice-first isn't optional—it's the only way this works. Our speech-to-JSON architecture is built for how restaurants actually operate."

---

### 5.2 Price Point Accessibility

**CoCounsel's Pricing:**
CoCounsel charges $400-500/month per user. Lawyers billing $300+/hour can easily justify this.

**Mise's Pricing:**
Mise charges $149/month for Payroll, $249/month for the full suite. This works for restaurant economics where margins are thin.

**Why This Matters:**
If the architecture works at restaurant price points, it proves the model scales to any professional vertical—not just high-margin ones. This is a platform validation, not a limitation.

**Pitch Language:**

> "CoCounsel charges $400-500/month because lawyers can afford it. We charge $149-249/month because restaurant margins demand it. If we can deliver CoCounsel-quality reliability at restaurant price points, we've proven the architecture works for any professional vertical."

---

### 5.3 Greenfield vs. Incumbent

**CoCounsel's Challenge:**
CoCounsel had to compete with Westlaw—decades of legal research infrastructure, established relationships, switching costs.

**Mise's Advantage:**
There is no Westlaw for restaurant operations. Toast is a POS, not an operations platform. Gusto is payroll processing, not payroll prep. MarginEdge is invoice processing, not inventory intelligence.

We're not displacing an incumbent. We're filling a vacuum.

**Pitch Language:**

> "CoCounsel had to compete with Westlaw's decades of legal research infrastructure. We're not competing with anyone—there's no AI-native operations layer for restaurants. We're filling a vacuum, not displacing an incumbent."

---

## Part 6: Objection Handling Framework

### "AI isn't reliable enough for payroll"

> "That's exactly what lawyers said about legal research. They trusted Westlaw searches done by paralegals who might miss things, but didn't trust AI. CoCounsel proved that the right architecture—grounding, human approval, comprehensive testing—makes AI more reliable than the alternative. Our tip calculation is more accurate than a tired manager doing spreadsheet math at 2am."

### "Restaurants won't pay for software"

> "Restaurants already pay for payroll processing (Gusto: $40-80/month + per employee). They pay for scheduling (7shifts: $35-150/month). They pay bookkeepers ($200-500/month). They pay MarginEdge for invoice processing ($300-500/month). They pay for things that save time. At $149/month, if Mise saves 5 hours/week, that's $5/hour. What manager's time is worth less than $5/hour?"

### "Toast/Square will just add this feature"

> "Westlaw could have added AI features. They did. It wasn't enough. Building AI-native from scratch is fundamentally different from bolting features onto legacy architecture. Thomson Reuters—the company that owns Westlaw—bought CoCounsel for $650M rather than building it themselves. Toast and Square will face the same choice: build it (hard, slow, outside core competency) or buy it."

### "What's your moat?"

> "Same as CoCounsel's: domain expertise encoded in testing infrastructure. Every edge case from real restaurant operations—missing clock-ins, partial tip pool participation, manager verbal overrides, split shifts, cash tips reported after closeout—becomes a test case. That regression suite for restaurant operations doesn't exist anywhere else. Models commoditize. Evaluation infrastructure that ensures reliability on domain-specific tasks does not."

### "This is too niche"

> "CoCounsel started with legal research for smaller firms. That looked niche too—until Thomson Reuters paid $650M for it. We're starting with payroll for single-unit restaurants. The expansion path is clear: multi-unit groups, adjacent hospitality (hotels, catering, food trucks), other professional services with operational overhead. The beachhead is small and focused. The platform is not."

### "Why would I trust AI with my payroll?"

> "You're not trusting AI with your payroll. You're reviewing what AI prepares and approving it yourself. That's how CoCounsel works with lawyers—the AI does the research, the lawyer reviews and signs off. Same model: Mise does the calculation, you review and approve. You're always in control. The AI just saves you from doing the math yourself at 2am."

---

## Part 7: Narrative Frameworks

### 7.1 The "Same Architecture, Different Domain" Story

> "In August 2023, Thomson Reuters paid $650 million in cash for Casetext's CoCounsel—an AI system that does legal work reliably enough that lawyers trust it with their careers.
>
> CoCounsel isn't a chatbot. It's a skills-based workflow system. Each skill handles a specific legal task: document review, deposition prep, contract analysis. The AI is grounded in actual documents, never hallucinates. Lawyers review everything before it goes out. And the moat is the thousands of legal test cases that ensure reliability.
>
> We looked at that architecture and asked: where else do professionals drown in administrative work that AI could handle—if you built it right?
>
> Restaurants.
>
> Restaurant operators spend hours every week on payroll prep, tip calculations, inventory counts, closeout reconciliation. Work that requires operational knowledge but not operational judgment. Work that happens at 2am after a 14-hour shift. Work that's error-prone because humans are tired.
>
> Mise is CoCounsel's architecture applied to restaurant operations. Domain agents instead of legal skills. Grounded in POS data instead of case documents. Human approval before anything executes. And an ever-growing test suite of restaurant-specific edge cases.
>
> CoCounsel proved the architecture works. We're proving it works at restaurant economics."

---

### 7.2 The "Validation by Analogy" Story

> "When someone tells you an idea is crazy, find someone who made it work in an adjacent domain.
>
> 'AI can't do professional work reliably' was conventional wisdom until CoCounsel proved otherwise. Lawyers—the most risk-averse professionals on earth—now trust AI with document review, legal research, contract analysis. Thomson Reuters validated this with $650 million.
>
> Restaurant operations is the same problem in a different uniform. High stakes (payroll errors mean lawsuits). Complex rules (tip pools, overtime, tax withholding). Time-pressured (decisions made at 2am after long shifts). Previously unsolved by technology.
>
> We're not asking anyone to believe something unproven. We're asking them to see the parallel. CoCounsel cracked the code on AI for professional work. Mise is applying that code to restaurants.
>
> The architecture is validated. The market is ready. The founder runs a restaurant."

---

### 7.3 The "Underserved Professional" Story

> "Lawyers have had Westlaw since 1975. Fifty years of legal research technology. When AI arrived, they got CoCounsel—purpose-built tools for legal workflows.
>
> What do restaurant operators have? Toast for transactions. Spreadsheets for everything else.
>
> Single-unit restaurant owners are the most underserved professionals in America. They work 60+ hour weeks. They do their own payroll at 2am. They track inventory on paper. They calculate tipouts by hand. Not because they want to—because nothing better exists.
>
> Lawyers got CoCounsel. Restaurant operators deserve Mise."

---

### 7.4 The "Exit Path" Story (For Investors)

> "Let me tell you how this ends.
>
> In 2023, Thomson Reuters—the $60 billion information company that owns Westlaw—paid $650 million for Casetext. They didn't build CoCounsel themselves, even though they had unlimited resources and decades of legal domain expertise. Building AI-native from scratch was harder than buying it.
>
> Toast is a $15 billion market cap company. They own restaurant POS. They want to own restaurant operations. But they're a payments company trying to become a platform. Building AI-native operations is outside their core competency.
>
> Gusto processes payroll for millions of small businesses. They want vertical depth in hospitality. But they're a payroll processor, not a domain expert in restaurant operations.
>
> One of them—or someone we haven't thought of yet—will face the same decision Thomson Reuters faced. Build or buy?
>
> Building requires: domain expertise in restaurant operations, AI-native architecture, years of edge case accumulation, operator trust. Buying requires writing a check.
>
> We're building the thing they'll want to buy."

---

## Part 8: Demo Script Framework

### Opening: Establish the Parallel

"Before I show you Mise, let me tell you about CoCounsel.

In 2023, Thomson Reuters paid $650 million for an AI system that does legal work. Not a chatbot—a workflow system where AI handles specific legal tasks, grounds everything in actual documents, and lawyers review before anything goes out.

Mise is that same architecture for restaurants. Let me show you what that means."

### Demo Flow: Mirror CoCounsel's Value Props

**1. Skills/Agents (30 seconds)**
"CoCounsel has skills—document review, legal research, contract analysis. Mise has agents—Payroll Machine, Inventory Agent, Closeout Agent. Each handles a specific workflow."

**2. Voice-First Input (60 seconds)**
"Restaurant operators can't stop to type. So I just talk through my day."

*"Sarah worked a double, left at midnight. Marcus clocked out early at 8. We had that private event—keep those tips separate from the pool."*

**3. Grounding (60 seconds)**
"See how this is pulling actual data from Toast? Hours worked, tip totals, transactions. CoCounsel only responds based on actual documents. Mise only calculates based on actual POS data. No guessing."

**4. Human Approval (30 seconds)**
"Here's the key: nothing happens until I approve it. CoCounsel prepares documents for lawyer review. Mise prepares payroll for my review. I see everything, I approve it, then it exports to Gusto."

**5. Audit Trail (30 seconds)**
"Every decision is logged. If an employee asks why their tips are what they are, I can show them exactly how it was calculated, what data was used, when I approved it."

### Close: The Punchline

"CoCounsel lets lawyers practice law instead of doing document review. Mise lets operators run restaurants instead of doing spreadsheet work.

The architecture is proven. We're just applying it to a market that's been ignored."

---

## Part 9: Audience-Specific Pitch Variations

### For Technical Investors

Lead with architecture:

- Multi-agent system with domain-specific agents
- Transrouter for intelligent task routing
- Grounding in structured data sources
- Evaluation infrastructure as moat
- Token economics at scale

**CoCounsel reference:** "Their moat is evaluation infrastructure. Ours is the same—domain-specific test cases that ensure reliability."

### For Market-Focused Investors

Lead with market:

- 114,000 target restaurants (new/recent single-unit)
- $20-34M ARR at 10% penetration
- Greenfield—no incumbent to displace
- Clear expansion path (multi-unit, adjacent hospitality)
- Exit path validated by CoCounsel acquisition

**CoCounsel reference:** "Thomson Reuters paid $650M for legal AI. Toast, Square, Gusto will face the same build-or-buy decision."

### For Strategic Partners (Toast, Gusto)

Lead with complementarity:

- We make your platform stickier
- We fill the operations gap you can't fill yourself
- We drive usage of your core product
- We've proven the model at Papa Surf

**CoCounsel reference:** "Thomson Reuters didn't build CoCounsel—they partnered, then acquired. We're open to partnership that makes sense for both sides."

### For Restaurant Operators

Lead with pain:

- "You know that 2am spreadsheet session? Gone."
- "You know when tips don't add up and you're too tired to figure it out? Solved."
- "You know the Department of Labor terrifies you? Protected."

**CoCounsel reference:** Use sparingly. Most operators don't know CoCounsel. Instead: "This is what lawyers use for their work—we built it for restaurants."

### For Culinary/Hospitality Press

Lead with operator empowerment:

- Freeing operators to focus on guests and food
- Technology that respects how restaurants actually work
- Voice-first because operators can't stop to type
- Built by an operator who runs a restaurant

**CoCounsel reference:** "The legal profession got AI tools that respect how lawyers work. Restaurants deserve the same."

---

## Part 10: Verified Facts Reference

| Claim | Status | Source |
|-------|--------|--------|
| Thomson Reuters acquired Casetext for $650M cash | Verified | Thomson Reuters press release, August 2023 |
| Acquisition was August 2023 | Verified | Multiple sources |
| CoCounsel is skills-based workflow system | Verified | Jake Heller descriptions |
| "QAnon Shaman" grounding example | Verified | Jake Heller interview |
| Model routing strategy | Verified | Casetext documentation |
| Human-in-the-loop architecture | Verified | Product documentation |
| ~50,000 new restaurants open annually | Verified | Industry data |
| 70% of US restaurants are single-unit | Verified | Multiple sources |
| ~150,000 single-location full-service restaurants | Verified | IBISWorld 2024 |
| 17% first-year failure rate | Verified | UC Berkeley/BLS study |
| ~30% close within 3 years | Verified | Cornell/industry data |

---

## Part 11: What NOT to Say

**Avoid These Claims:**

- "Our market is 10x larger than legal" — False. Establishment counts are comparable.
- "There are 1 million restaurants" — Misleading. Your target is ~150K single-unit full-service.
- "Restaurant industry is $900B" — Outdated. It's $1.5 trillion projected for 2025.
- "We're just like CoCounsel" — Too strong. Say "same architecture" or "same principles."
- "AI will replace restaurant managers" — Wrong framing. Say "AI that makes managers faster."

**Do Say:**

- "CoCounsel proved the architecture. We're applying it to a comparable market."
- "Same principles: grounding, human approval, domain-specific testing."
- "The moat is evaluation infrastructure—same as CoCounsel's."
- "We're filling a vacuum, not displacing an incumbent."
- "Built by an operator who runs a restaurant."

---

## Final Thought

This framework gives you ammunition for any audience, any format, any objection. The CoCounsel parallel is legitimate, defensible, and powerful—if deployed with precision.

---

*Mise: Everything in its place.*
