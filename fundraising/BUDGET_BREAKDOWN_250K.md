# $250,000 Budget — Line-by-Line Breakdown

**Created:** 2026-01-19
**Purpose:** Detailed allocation of seed funding

---

## Summary

| Category | Amount | % of Total |
|----------|--------|------------|
| Senior Engineer | $130,000 | 52% |
| Security/SOC 2 | $35,000 | 14% |
| Infrastructure | $20,000 | 8% |
| QA/Testing | $15,000 | 6% |
| Battlestation + Office | $6,000 | 2.4% |
| Travel/Customers | $8,000 | 3.2% |
| Training/Tools | $4,000 | 1.6% |
| Sales/Onboarding | $12,000 | 4.8% |
| Legal/IP | $10,000 | 4% |
| Contingency | $10,000 | 4% |
| **Total** | **$250,000** | **100%** |

**Note:** Jon is not drawing salary from Mise. Papa Surf salary ($80-120K/year) covers personal expenses. 100% of funding goes to growth.

---

## 1. Senior Engineer — $130,000

This is the biggest line item. Here's exactly where it goes:

| Component | Amount | Details |
|-----------|--------|---------|
| Base salary | $115,000 | ~$9,580/month gross |
| Payroll taxes (employer side) | $8,800 | Social Security (6.2%) + Medicare (1.45%) + FUTA/SUTA (~$500) |
| Health insurance contribution | $4,800 | ~$400/month toward their premium (typical startup contribution) |
| Equipment for them | $1,400 | MacBook Pro or equivalent for their work |
| **Total** | **$130,000** | |

**What $115K base gets you:**
- 5-8 years experience
- Python/FastAPI strong
- Can work autonomously
- Has inherited messy codebases before
- Probably based in a mid-cost-of-living city (Austin, Denver, Raleigh — not SF)

**Payment schedule:**
- Monthly payroll: ~$10,830/month all-in
- 12 months × $10,830 = $129,960

**What they do:**
- Implementation from Jon's specs
- Bug fixes and maintenance
- Test coverage
- Infrastructure/DevOps
- Volume work while Jon focuses on architecture

**What Jon does (15-20 hrs/week):**
- Architecture decisions
- Core workflow logic
- Code review
- Tricky integrations
- Domain-specific features

---

## 2. Security & SOC 2 — $35,000

| Component | Amount | Details |
|-----------|--------|---------|
| Compliance platform (Vanta or Drata) | $12,000 | ~$1,000/month, automates evidence collection |
| SOC 2 Type 1 audit | $15,000 | One-time audit fee from certified CPA firm |
| Penetration testing | $6,000 | Third-party pentest, 1-2 week engagement |
| Security tools/bug bounty | $2,000 | Dependabot, Snyk, or small bug bounty pool |
| **Total** | **$35,000** | |

**Timeline:**
- T1-T2: Set up Vanta, begin evidence collection
- T3-T6: Build compliance habits, fix gaps
- T7-T8: Pentest + SOC 2 Type 1 audit
- T8: Certification in hand

**Why this matters:**
- Enterprise customers require SOC 2
- Shows investors you're serious about security
- Differentiates you from "move fast break things" competitors

---

## 3. Infrastructure & Cloud — $20,000

| Component | Amount | Details |
|-----------|--------|---------|
| Google Cloud Run | $6,000 | ~$500/month, auto-scales, pay-per-request |
| BigQuery | $2,400 | ~$200/month for analytics and data warehouse |
| Cloud Storage | $1,200 | ~$100/month for audio files, backups |
| Whisper API (OpenAI) | $4,800 | ~$400/month for transcription (~3,000 shifties/month at scale) |
| Claude API (Anthropic) | $3,600 | ~$300/month for parsing and agent logic |
| Monitoring (Datadog or GCP native) | $1,200 | ~$100/month for observability |
| Domain, DNS, SSL | $300 | Cloudflare, domain renewals |
| Misc (secrets manager, etc.) | $500 | Google Secret Manager, misc |
| **Total** | **$20,000** | |

**Notes:**
- Costs scale with usage — early months will be cheaper
- At 20 restaurants doing 60 shifties/month each = 1,200 shifties/month
- Buffer for spikes and experimentation

---

## 4. QA & Testing — $15,000

| Component | Amount | Details |
|-----------|--------|---------|
| CI/CD pipeline (GitHub Actions) | $1,200 | ~$100/month for build minutes |
| Testing infrastructure | $1,800 | Test databases, staging environments |
| Contract QA help | $8,000 | Part-time QA contractor, ~$50/hr × 160 hours over the year |
| Test data management | $1,000 | Tools for generating/managing test data |
| Device testing | $1,500 | Physical devices for mobile testing (various phones/tablets) |
| Automated testing tools | $1,500 | Pytest fixtures, Playwright for E2E, coverage tools |
| **Total** | **$15,000** | |

**What you get:**
- Automated test suite running on every PR
- Staging environment that mirrors production
- Part-time QA person to catch what automation misses
- Test coverage from ~40% to ~70%+

---

## 5. Battlestation + Office — $6,000

Jon's workspace. Investment in productivity.

| Component | Amount | Details |
|-----------|--------|---------|
| MacBook Pro M3 (if needed) | $2,500 | Or $0 if current machine is fine |
| Monitor (32" 4K or ultrawide) | $700 | LG, Dell, or Samsung |
| Standing desk | $500 | Uplift, Fully, or similar |
| Ergonomic chair | $400 | Used Herman Miller Aeron or new budget ergo |
| Mechanical keyboard | $150 | If you're into it |
| Headphones | $350 | AirPods Max, Sony XM5, or similar |
| Webcam + lighting | $200 | For investor calls, customer demos |
| Desk accessories | $200 | Cable management, monitor arm, etc. |
| Whiteboard or wall setup | $200 | For architecture diagrams |
| Misc (adapters, cables, etc.) | $100 | The stuff you always need |
| Coworking buffer | $700 | ~2-3 months of day passes if needed |
| **Total** | **$6,000** | |

**Note:** If existing equipment is fine, reallocate unused amount to contingency.

---

## 6. Travel & Customers — $8,000

| Component | Amount | Details |
|-----------|--------|---------|
| Down Island onboarding trip | $800 | Flight/drive, 1-2 nights, meals |
| Customer visit trips (×6) | $3,600 | ~$600 each (regional travel, meals, maybe 1 night) |
| Conference attendance (×1) | $2,000 | Ticket ($500-800) + travel + hotel |
| Customer meals/entertainment | $1,200 | Taking prospects to lunch/dinner (~$100 × 12) |
| Mileage/local travel | $400 | Gas, parking for local customer visits |
| **Total** | **$8,000** | |

**Why this matters:**
- Face-to-face closes deals faster than Zoom
- Onboarding in person builds trust
- You see how they actually use Mise in their environment
- Conference = networking + market intel

---

## 7. Training & Tools — $4,000

| Component | Amount | Details |
|-----------|--------|---------|
| GitHub (Team plan) | $500 | ~$44/month for you + engineer |
| Linear or Notion | $300 | Project management |
| Figma | $150 | Design if needed |
| Claude Pro / ChatGPT Plus | $500 | ~$40/month for AI tools |
| Cursor Pro or similar | $240 | AI-assisted coding |
| Online courses | $800 | System design, advanced Python, security, whatever |
| Books / resources | $200 | Technical books, industry reports |
| Loom or screen recording | $150 | For async communication |
| Misc SaaS tools | $600 | Stuff you'll discover you need |
| One conference/workshop | $560 | Local workshop or online summit |
| **Total** | **$4,000** | |

---

## 8. Sales & Onboarding — $12,000

| Component | Amount | Details |
|-----------|--------|---------|
| CRM (HubSpot free or Pipedrive) | $600 | ~$50/month if you go paid tier |
| Email platform (Customer.io or similar) | $1,200 | ~$100/month for onboarding sequences |
| Support tool (Intercom or Crisp) | $1,200 | ~$100/month for in-app chat/support |
| Demo environment | $500 | Dedicated demo instance with fake data |
| Onboarding materials | $1,000 | Video production, guides, templates |
| Swag / leave-behinds | $1,500 | T-shirts, stickers, printed materials for customers |
| Contract sales help | $4,000 | Part-time sales contractor, ~$25/hr × 160 hours |
| Marketing experiments | $2,000 | Small paid tests, local ads, sponsorships |
| **Total** | **$12,000** | |

**What you get:**
- Professional onboarding experience
- Ability to track leads and pipeline
- Part-time help booking demos and following up
- Leave-behind swag that keeps Mise top of mind

---

## 9. Legal & IP — $10,000

| Component | Amount | Details |
|-----------|--------|---------|
| Trademark registration ("Mise") | $350 | USPTO filing fee |
| Copyright registration | $65 | Copyright.gov for codebase |
| Legal retainer / startup lawyer | $5,000 | General counsel for contracts, questions |
| Terms of Service / Privacy Policy | $1,500 | Lawyer-reviewed (not just templates) |
| Customer contract template | $1,500 | MSA / subscription agreement |
| Contractor agreements | $500 | Templates for any contractors |
| IP assignment cleanup | $500 | Make sure everything is assigned to company |
| Misc legal | $585 | Random stuff that comes up |
| **Total** | **$10,000** | |

**What you get:**
- Protected brand
- Solid contracts that don't scare enterprise customers
- Lawyer on speed dial when weird stuff happens

---

## 10. Contingency — $10,000

| What It's For | Example |
|---------------|---------|
| Unexpected API cost spikes | Whisper/Claude usage higher than projected |
| Emergency contractor help | Need extra hands for a deadline |
| Equipment replacement | Laptop dies |
| Legal surprise | Cease and desist, contract dispute |
| Opportunity fund | Something comes up that's worth grabbing |
| Runway extension | If things take longer than planned |

**Rule:** Don't touch this unless you have to. It's insurance.

---

## Cash Flow Over 12 Months

| Month | Big Expenses | Running Costs | Approx Spend |
|-------|--------------|---------------|--------------|
| T1 | Engineer signing bonus ($2K), legal setup ($3K), equipment ($4K) | Engineer salary, infra | ~$20K |
| T2 | Vanta setup ($3K), trademark filing ($350) | Engineer, infra, tools | ~$15K |
| T3 | Down Island trip ($800), onboarding materials ($1K) | Engineer, infra | ~$14K |
| T4 | Conference ($2K), marketing experiments ($1K) | Engineer, infra | ~$15K |
| T5 | Customer trips ($1.2K), QA contractor starts | Engineer, infra | ~$14K |
| T6 | Customer trips ($1.2K) | Engineer, infra, QA | ~$15K |
| T7 | SOC 2 audit deposit ($7.5K) | Engineer, infra, QA | ~$20K |
| T8 | SOC 2 audit final ($7.5K), pentest ($6K) | Engineer, infra | ~$26K |
| T9 | Sales contractor ramp ($2K) | Engineer, infra | ~$15K |
| T10 | Sales contractor ($2K) | Engineer, infra | ~$15K |
| T11 | Buffer | Engineer, infra | ~$13K |
| T12 | Buffer / runway extension | Engineer, infra | ~$13K |

**Approximate monthly burn (steady state):** $13-15K
**Peak months (T7-T8 with SOC 2):** $20-26K

---

## Key Assumptions

1. **Jon draws $0 salary** — Papa Surf covers personal expenses
2. **Engineer starts T1** — hired during fundraise, starts when money lands
3. **No office lease** — home office + occasional coworking
4. **Regional travel only** — no international trips in year 1
5. **SOC 2 Type 1 only** — Type 2 comes in year 2 with Series A money
6. **Conservative API costs** — actuals may be lower early on

---

## What Success Looks Like at T12

- 15-20 paying restaurants
- $2,200-$3,700 MRR (at $149/month average)
- SOC 2 Type 1 certified
- Inventory workflow live
- Senior engineer retained and productive
- Ready for Series A conversation

---

*This budget is tight but achievable. Every dollar has a job.*
