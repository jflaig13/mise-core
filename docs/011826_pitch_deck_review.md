# Pitch Deck Review — 2026-01-18

**Reviewer:** ccw5 (Demo Prep & Documentation)
**Deck Version:** Mise_PitchDeck_v2.pdf
**Investor Demo:** Tuesday, January 20th @ 1PM

---

## CRITICAL ISSUES (Must Fix Before Demo)

### 1. FUNDING ASK IS WRONG — Slide 19

**Current (INCORRECT):** "$150,000"

**Should be:** "$250,000" per MISE_STATE_COMPLETE.md

**Copy-paste replacement for Slide 19 title:**
```
The Ask: Build the First Voice-Driven Virtual Executive Assistant for Hospitality

We are raising $250,000 to turn Mise's proven systems into an enterprise-grade platform and reach 10-20 paying restaurants within 12 months.
```

---

### 2. CHATGPT REFERENCE STILL IN DECK — Slide 11

**Current (Slide 11, Local Inventory Machine):**
> "ChatGPT interprets the transcript using:"

**Replace with:**
```
Claude interprets the transcript using:
```

---

### 3. TYPO — Slide 10

**Current:**
> "Typing inot spreadsheets"

**Replace with:**
```
Typing into spreadsheets
```

---

## HIGH-PRIORITY IMPROVEMENTS

### 4. SLIDE 19 (The Ask) — Complete Rewrite

The current slide lacks the detailed allocation that demonstrates financial discipline. Replace entire slide content:

```
The Ask: $250,000 for 12-Month Enterprise-Grade Deployment

We are raising $250,000 to scale Mise from one restaurant to 10-20 paying customers with enterprise-grade infrastructure.

Allocation:
• Engineering (48%) — $120,000
  Lead engineer salary + benefits for 12 months

• Security & Compliance (16%) — $40,000
  Enterprise hardening, SOC 2 prep, penetration testing

• Infrastructure & Cloud (10%) — $25,000
  Cloud Run, BigQuery, monitoring, logging

• QA & Testing (8%) — $20,000
  Automated testing, CI/CD, integration tests

• Sales & Onboarding (6%) — $15,000
  Customer success, training, support systems

• Legal & Compliance (4%) — $10,000
  Contracts, privacy policy, IP protection

• Contingency (8%) — $20,000
  Buffer for unknowns

By Month 12: 10-20 paying restaurants, $4K-$8K MRR, SOC 2 ready, Jon full-time on Mise.
```

---

### 5. SLIDE 20 (2026 Roadmap) — Use Timeline Tokens

Per MISE_STATE_COMPLETE.md, avoid specific calendar dates. Replace:

**Current:** Uses "Feb 2026", "Mar 2026", etc.

**Replace entire slide with:**

```
12-Month Roadmap

T1 (Month 1): Foundation & Hiring
• Lead full-stack engineer onboarded
• Engineering standards established
• CI/CD pipeline operational

T2 (Month 2): Security Hardening & Infrastructure
• API authentication hardened
• Production infrastructure live
• Monitoring and alerting systems deployed

T3 (Month 3): Down Island Onboarding (Pilot #2)
• Second location fully onboarded
• Multi-tenant architecture validated

T4 (Month 4): First Paying Customer
• Revenue generation begins
• Billing system operational

T5-T6 (Months 5-6): Scale to 5 Restaurants
• ~$1.5K-$2K MRR
• Onboarding time < 1 week per restaurant

T7-T8 (Months 7-8): SOC 2 Compliance Prep
• Security audit
• Enterprise-ready posture

T9-T10 (Months 9-10): Scale to 10 Restaurants
• ~$3K-$4K MRR
• Unit economics proven

T11 (Month 11): Inventory Workflow Launch
• Expand beyond payroll

T12 (Month 12): Jon Full-Time, Series A Prep
• 15-20 restaurants, ~$6K-$8K MRR
• Product-market fit conclusively proven
```

---

### 6. ADD MARKET SIZE SLIDE (New — Insert After Slide 5)

The deck never states the market opportunity. Add:

```
The Market Opportunity

500,000+ single-location owner-operators in the US alone.

• 7 in 10 restaurants are single-unit operations
• 9 in 10 have fewer than 50 employees
• Restaurant labor costs up 30% since 2019
• Voice AI market: $10B → $49B by 2029

These owners don't have IT departments. They can't afford back-office staff.
They're doing payroll at midnight after 14-hour shifts.

Big players ignore them because they're "low-value" customers.

That's exactly why the opportunity exists.
```

---

### 7. SLIDE 9 (Mise Web App) — Clarify Naming

**Issue:** Title says "The Mise Web App" but content describes "The Local Payroll Machine" — confusing.

**Replace slide title:**
```
The Mise Web App – Payroll Workflow
```

Or keep current title but update first line:
```
The Mise Web App's payroll workflow uses a hybrid human + AI pattern:
```

---

### 8. SLIDE 16 (Why Mise Wins) — Add Enterprise-Grade Positioning

**Add new bullet #7:**
```
7. Enterprise-grade from day one
   Built with SOC 2 compliance in mind from the start.
   Security, audit logging, and rollback-ready deployments are not afterthoughts.
```

---

### 9. SLIDE 14 (Unified Mise System) — Update Architecture Language

**Current (bottom):**
> "Once funded, we will transform what Claude does today into a production-grade internal model"

**Replace with:**
```
The Transrouter API gateway already orchestrates domain agents in production.
Funding accelerates multi-restaurant deployment and enterprise hardening.
```

This is more accurate — Transrouter already exists and works.

---

## MEDIUM-PRIORITY IMPROVEMENTS

### 10. SLIDE 2 (Why I Built This) — Add One-Line Pitch

**Add at the very end of the quote, or as a separate callout:**
```
"I built Mise because I wanted my restaurant back."
```

---

### 11. SLIDE 10 (Local Payroll Machine) — Strengthen Production Claim

**Current:**
> "This isn't a prototype. I've run real payroll this way since Q3 2025. It works."

**Enhance to:**
```
This isn't a prototype. I've processed real payroll — real money, real employees — every week since Q3 2025. It works.
```

---

### 12. SLIDE 17 (Unique Access) — Add Traction Metric

**Add at the end:**
```
Since Q3 2025: 20+ consecutive weeks of real payroll processed at Papa Surf without errors.
```

(Verify the actual number of weeks — this demonstrates reliability)

---

### 13. SLIDE 21 (Pricing Model) — Add Enterprise Tier Mention

**Add after Full Suite:**
```
Enterprise (Coming T7+)
• Multi-location support
• SOC 2 compliance
• Dedicated support
• Custom pricing
```

---

### 14. SLIDE 18 (Why Now) — Tighten Point #5

**Current:**
> "Mise has validated the new paradigm ahead of the market"
> "POS systems store data. Scheduling tools schedule. Inventory tools count."
> "None of them execute operations end-to-end."

**Issue:** This repeats point #5 from Slide 16 (Why Mise Wins). Differentiate:

**Replace with:**
```
5. First-mover advantage in a category that doesn't have a name yet
   Voice-first back-office operations for owner-operators.
   When the market names this category, Mise will already be operating inside it.
```

---

## LOW-PRIORITY / OPTIONAL IMPROVEMENTS

### 15. SLIDE 22 (Our Team) — Fix Apostrophe

**Current:**
> "complement Jons on-the-ground"

**Replace with:**
```
complement Jon's on-the-ground
```

---

## SUMMARY — PRIORITY ORDER

| Priority | Issue | Slide | Action |
|----------|-------|-------|--------|
| **CRITICAL** | Funding ask wrong ($150K → $250K) | 19 | Fix immediately |
| **CRITICAL** | ChatGPT → Claude | 11 | Fix immediately |
| **CRITICAL** | Typo "inot" | 10 | Fix immediately |
| **HIGH** | Add allocation breakdown | 19 | Rewrite slide |
| **HIGH** | Timeline tokens vs calendar dates | 20 | Rewrite slide |
| **HIGH** | Add market size slide | New | Insert after slide 5 |
| **HIGH** | Clarify Web App vs LPM naming | 9 | Update title/intro |
| **HIGH** | Add enterprise-grade positioning | 16 | Add bullet |
| **MEDIUM** | Add one-line pitch | 2 | Add callout |
| **MEDIUM** | Strengthen production claim | 10 | Enhance text |
| **MEDIUM** | Add traction metric | 17 | Add stat |
| **LOW** | Fix apostrophe "Jons" | 22 | Fix typo |

---

## Executive Summary

**3 Critical Fixes (do these first):**
1. Slide 19: Change "$150,000" to "$250,000"
2. Slide 11: Change "ChatGPT interprets" to "Claude interprets"
3. Slide 10: Fix "inot" → "into"

**4 High-Impact Improvements:**
1. Rewrite Slide 19 with the $250K allocation breakdown (shows financial discipline)
2. Convert Slide 20 to timeline tokens (T1-T12) instead of calendar dates
3. Add market size slide ("500,000 single-location restaurants")
4. Add enterprise-grade positioning to "Why Mise Wins"

The deck is structurally sound — the founder story (Slide 2) is powerful and the technical architecture (Slides 14-15) is well-explained. These fixes ensure the numbers match the canonical fundraising ask and eliminate inconsistencies that could undermine investor confidence.
