# Legal Action Plan

**February 2026 — Closing Mise's Legal Gaps**

---

## The Situation

Mise has been operating since November 2025 with only 2 executed documents: a Certificate of Incorporation and a Shareholder Agreement. The Lipton Standard assessment scored Mise **5 out of 33** on corporate legal hygiene.

Five documents have been drafted and are ready for attorney review and execution. This plan tells you exactly what to do, in what order, and why.

<div class="stats-row">
<div class="stat-box">
<div class="number">5/33</div>
<div class="label">Lipton Score (Current)</div>
</div>
<div class="stat-box">
<div class="number">5</div>
<div class="label">Docs Ready</div>
</div>
<div class="stat-box">
<div class="number">~$5-8K</div>
<div class="label">Legal Budget</div>
</div>
</div>

---

## Step 1: Find the Right Attorney

You need a **startup-fluent corporate attorney** who knows Delaware law and won't flinch at AI. You don't need a local attorney — 90% of startup legal work happens over email, DocuSign, and Zoom.

### What to Look For

- 20-30+ Delaware C-Corp formations under their belt
- Has closed priced equity rounds (Series Seed or Series A)
- Understands IP assignment for software companies
- Ideally has represented at least one AI or voice-tech company
- Knows what SAFE notes are without you explaining it

### Where to Look

**Ask Mercury and Carta.** Both maintain referral networks of startup attorneys. Email Mercury support: *"Can you recommend startup attorneys who work with early-stage Delaware C-Corps?"*

**YC Startup School network.** Post in the YC forum asking for attorney referrals. Attorneys who regularly work with YC companies understand your stage and your budget.

**Florida startup ecosystem.** Tampa and Miami have growing startup scenes. Look at Tampa Bay Wave and Embarc Collective for mentor/advisor networks that include attorneys.

**Clerky's attorney network.** Clerky is the gold standard for startup legal paperwork. Their website lists partner attorneys by region.

**Direct search.** Don't Google "business attorney near me." Search for: *"Delaware C-Corp" attorney startup AI* on LinkedIn.

### The 5-Minute Vet — 3 Questions to Ask

<div class="callout important" markdown="1">
<div class="callout-title">Question 1</div>
"We're a Delaware C-Corp with two founders, 70/30 split, fully vested. Our core product uses OpenAI Whisper for transcription and Anthropic Claude for data extraction. What's the biggest IP risk you see?"

**Right answer:** Proper IP assignment from founders, making sure API terms allow commercial use of outputs, confirming you own the outputs. If they say "what's Whisper?" — hang up.
</div>

<div class="callout important" markdown="1">
<div class="callout-title">Question 2</div>
"We have a one-sentence IP clause in our Shareholder Agreement that says 'work-for-hire principles.' Is that sufficient?"

**Right answer:** Immediate no. Work-for-hire under 17 U.S.C. §101 doesn't apply to software written by founders who aren't employees. You need a proper assignment.
</div>

<div class="callout important" markdown="1">
<div class="callout-title">Question 3</div>
"We're raising $250K on a SAFE at $3M pre-money. What do we need to clean up before we can close?"

**Right answer:** Board resolutions, IP assignments, stock ledger, cap table on Carta, possibly 83(b) elections, and they should ask about your Certificate of Incorporation's authorized share count.
</div>

### Budget Reality

With $5-8K, you can afford a solo practitioner or small firm to review all 5 documents, provide redlines, and handle execution. You cannot afford Big Law at this stage. That's fine — you need a sharp startup specialist who charges $300-500/hour and can review everything in 10-15 hours.

---

## Step 2: Execute the Documents

<div class="timeline">
<div class="timeline-item">
<div class="date">DOCUMENT 1 — FIRST</div>
<div class="event"><strong>Initial Board Resolutions</strong></div>
</div>
<div class="timeline-item">
<div class="date">DOCUMENT 2 — SAME DAY</div>
<div class="event"><strong>IP Assignment — Jonathan Flaig</strong></div>
</div>
<div class="timeline-item">
<div class="date">DOCUMENT 3 — SAME DAY</div>
<div class="event"><strong>IP Assignment — Austin Miett</strong></div>
</div>
<div class="timeline-item">
<div class="date">DOCUMENT 4 — BEFORE NEXT CLIENT</div>
<div class="event"><strong>Terms of Service</strong></div>
</div>
<div class="timeline-item">
<div class="date">DOCUMENT 5 — SAME DAY AS TOS</div>
<div class="event"><strong>Privacy Policy</strong></div>
</div>
</div>

---

## Document 1: Initial Board Resolutions

<div class="callout note" markdown="1">
<div class="callout-title">Priority: Do This First</div>
This is the foundation document. Without it, nothing else is formally authorized.
</div>

### Why It Matters

Every corporate action Mise has taken — opening Mercury, signing NDAs, deploying on GCP — was done without formal board authorization. The Board Resolutions retroactively cure all of that and establish the authority chain going forward.

It also formally kills the old 60/40 bylaws from November 2025. You don't want two conflicting bylaws when investors do due diligence.

### Who Signs

| Signer | Role | Why |
|--------|------|-----|
| Jonathan Flaig | Director | Board action requires all directors |
| Austin Miett | Director | Board action requires all directors |

Both sign **as Directors** (not officers). This is a board action by unanimous written consent under DGCL §141(f).

### How to Execute

1. Send PDF to attorney for review
2. After attorney approval, upload to DocuSign
3. Fill in the Effective Date field
4. Both directors sign and date
5. Attach the January 22, 2026 Bylaws as Exhibit A
6. Save executed PDF to Google Drive: `Docs/Legal/Board Consents/`

---

## Document 2: IP Assignment — Jonathan Flaig

<div class="callout warning" markdown="1">
<div class="callout-title">This is the most important document for Mise's valuation</div>
Without it, the company does not provably own its core technology. Every investor will ask "does the company own its IP?" — this is how you answer yes.
</div>

### Why It Matters

Jon wrote the entire platform — LPM, CPM, LIM, Transrouter, Mise App — partly before the company was incorporated on November 19, 2025. Under copyright law, that pre-incorporation code belongs to **Jon personally**, not to Mise, Inc.

The one-sentence "work-for-hire" clause in the Shareholder Agreement doesn't fix this because work-for-hire under 17 U.S.C. §101 requires an employer-employee relationship that didn't exist before incorporation.

This document irrevocably assigns all 10 itemized IP assets from Jonathan Flaig to Mise, Inc.

### Who Signs

| Signer | Role | Why |
|--------|------|-----|
| Jonathan Flaig | Assignor | Giving the IP |
| Austin Miett | Company Representative | Secretary/Treasurer signs for the Company |

Austin signs on behalf of the Company — this avoids the same-person-both-sides problem.

### How to Execute

1. Attorney reviews and redlines
2. Upload to DocuSign
3. Fill in Effective Date and Jon's personal address
4. Jon signs as Assignor and initials the Exhibit A page
5. Austin signs as Company representative
6. Save to Google Drive: `Docs/Legal/`

---

## Document 3: IP Assignment — Austin Miett

### Why It Matters

Same principle as Jon's, but for Austin's contributions: business plans, corporate formation materials, and investor materials. Investors want to see that **all** founders assigned IP, not just the technical one. It also closes any future dispute about who contributed what.

### Who Signs

| Signer | Role | Why |
|--------|------|-----|
| Austin Miett | Assignor | Giving the IP |
| Jonathan Flaig | Company Representative | President/CEO signs for the Company |

Mirror image of Jon's. Jon signs on behalf of the Company for Austin's assignment.

### How to Execute

1. Attorney reviews
2. Upload to DocuSign
3. Fill in Effective Date and Austin's personal address
4. Austin signs as Assignor and initials Exhibit A
5. Jon signs as Company representative
6. Save to Google Drive: `Docs/Legal/`

<div class="callout tip" markdown="1">
<div class="callout-title">Pro Tip</div>
Sign all three documents (Board Resolutions + both IP Assignments) in one DocuSign envelope on the same day. The Board Resolutions authorize the IP Assignments (Resolution §6), so the resolutions should be dated first or on the same date.
</div>

---

## Document 4: Terms of Service

<div class="callout note" markdown="1">
<div class="callout-title">Priority: Before Down Island or Any New Client</div>
Nobody signs this. It's a published document users agree to by using the Service.
</div>

### Why It Matters

Right now, anyone using app.getmise.io has no contractual agreement with Mise. That means: no liability cap, no arbitration clause, no IP protection, no disclaimer on AI accuracy.

If a client has a payroll calculation error and relies on it without reviewing, Mise has zero legal protection. The Terms of Service establishes: the user is responsible for verifying AI output, Mise is not an employer of record, liability is capped, disputes go to arbitration, and class actions are waived.

### Who Signs

Nobody. Published at `getmise.io/terms`.

### How to Execute

1. Attorney reviews and redlines (this doc gets the most changes — attorneys have strong opinions about liability caps and arbitration)
2. Publish final version at `getmise.io/terms`
3. Add a "By using this service, you agree to our Terms of Service and Privacy Policy" to the app
4. Fill in the effective date as the date you publish

---

## Document 5: Privacy Policy

### Why It Matters

You're processing voice recordings, employee names, hours, tips, and inventory data. Multiple state privacy laws apply — CCPA/CPRA (California), Florida Digital Bill of Rights, and potentially BIPA-adjacent claims (Illinois).

Without a published privacy policy, you're in technical violation of California law if any California resident ever has their data in a recording. The policy also discloses your AI sub-processors (OpenAI, Anthropic), which users need to know about.

### Who Signs

Nobody. Published at `getmise.io/privacy`.

### How to Execute

1. Attorney reviews (pay attention to the biometric data section — confirm your transcription workflow genuinely doesn't create voiceprints)
2. Publish at `getmise.io/privacy`
3. Publish same day as Terms of Service (the ToS references the Privacy Policy URL)
4. Fill in the effective date

---

## Execution Checklist

| # | Document | Signs | Priority | Status |
|---|----------|-------|----------|--------|
| 1 | Board Resolutions | Jon + Austin (Directors) | Immediate | Drafted, needs attorney review |
| 2 | IP Assignment — Jon | Jon (Assignor) + Austin (Company) | Immediate | Drafted, needs attorney review |
| 3 | IP Assignment — Austin | Austin (Assignor) + Jon (Company) | Immediate | Drafted, needs attorney review |
| 4 | Terms of Service | Nobody (published) | Before next client | Drafted, needs attorney review |
| 5 | Privacy Policy | Nobody (published) | Before next client | Drafted, needs attorney review |

<div class="callout important" markdown="1">
<div class="callout-title">The One Action Item Right Now</div>
Find the attorney. Everything else flows from that. Send the 5 PDFs to the attorney for review, get redlines back, execute Documents 1-3 via DocuSign, publish Documents 4-5 on the website. That sequence closes your biggest legal gaps and makes you investor-ready.
</div>

---

## All Documents Are Here

All markdown source files and PDFs are located at:

`mise-core/legal/documents/`

- `Initial_Board_Resolutions_Mise.md` + `.pdf`
- `IP_Assignment_Jonathan_Flaig.md` + `.pdf`
- `IP_Assignment_Austin_Miett.md` + `.pdf`
- `Terms_of_Service_Mise.md` + `.pdf`
- `Privacy_Policy_Mise.md` + `.pdf`

---

*Mise: Everything in its place.*
