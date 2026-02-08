# MASTER SPEC — Misessessment
Internal Mise Research Output Standard

---

## Definition

A **Misessessment** is the standardized internal document produced after ChatGPT has fully ingested, analyzed, and synthesized a single piece of media for the Mise Research Project.

A Misessessment is:
- Non-authoritative
- Non-canonical
- Designed to improve judgment, not establish law
- Optimized for internal clarity, reuse, and future automation

A Misessessment MUST follow this spec exactly unless explicitly overridden.

---

## Core Principles

1. Plain language only.
   - No AI jargon.
   - No theory flexing.
   - No academic signaling.

2. If the source material uses jargon or theory-heavy language:
   - Call it out explicitly.
   - Explain what it means in simple terms.
   - Explain where the reader is likely to encounter it again in the future
     (investor decks, vendor marketing, engineering docs, media narratives, etc.).

3. The document should read like an internal Mise memo, not a chat response.

4. The goal is not inspiration.
   The goal is orientation, judgment, and decision support.

---

## Output Format (Single Copyable Block)

A Misessessment MUST be delivered as:
- One contiguous Markdown block
- No commentary before or after
- No emojis
- No conversational framing
- Clean headings and deterministic structure

---

## Canonical Structure (Required)

### Title

# Misessessment — [Source Title]

---

### Header

Date: YYYY-MM-DD

Mise State Snapshot:
(Star Wars-style opening crawl; see rules below)

---

### 1. Source Technicality Assessment

Required:
- Rate the technicality as: Low / Medium / High / Very High
- Explain why in plain language
- Focus on assumed knowledge, density, and abstraction level

---

### 2. Plain-Language Summary of the Material

Required:
- In-depth summary of the source
- Plain language only
- No unexplained acronyms
- No imported theory

This section should answer:
- What is the speaker actually arguing?
- What are they asserting is changing?
- What problems are they saying matter most?

#### Jargon & Theory Callouts (Required if applicable)

For each term:
- **Term or Acronym (fully expanded):**
  - Simple explanation of what it means
  - Where the reader is likely to see this term again in the future

All acronyms MUST be expanded and explained before reuse.

---

### 3. What This Means for Mise (Time-Horizon Analysis)

This section translates the material directly into Mise implications.

Required horizons:
- d = 0 (Now)
- d = 30
- d = 90
- d = 180
- d = 360

For each horizon:
- Be concrete
- Tie to product, workflows, data, system behavior, or strategy
- Avoid generic startup or AI advice
- Anchor to Mise's actual constraints and reality

---

### 4. Recommended Courses of Action for Mise

Each recommendation MUST include:
- The recommendation itself
- Why it follows from the material
- What would make this recommendation wrong
- What should be measured next to validate or falsify it

Recommendations should reflect:
- Market trends
- Credible forward-looking commentary
- Realistic Mise execution capacity

---

### 5. Net Effect on Mise's Thinking, Building, or Acting

Required:
- A direct, plain-language answer to:
  "What does this change about how Mise should think, build, or act?"
- No hedging
- No hype
- One short paragraph maximum

---

## Mise State Snapshot — Style Rules (Star Wars Opening Crawl)

The Mise State Snapshot MUST:

- Be written in present tense
- Use short, declarative paragraphs (not bullet points)
- Contain 3-5 paragraphs maximum
- Be factual, not fictional
- Avoid metaphors, hype, or jokes
- Convey momentum, tension, and trajectory

It should answer:
- Where Mise is right now
- What just changed
- Why this moment matters

Example tone reference:
- Star Wars opening crawl
- Internal historical record
- Strategic orientation, not marketing

---

## Relationship to Research Artifacts

A Misessessment MAY result in:
- MEDIA_LOG.md updates
- INVARIANTS_LOG.md entries
- OPEN_QUESTIONS.md entries
- CANDIDATE_FOR_CANON.md staging

A Misessessment:
- Does NOT create canon
- Does NOT update specs
- Does NOT establish institutional law

Escalation beyond this document requires a separate, explicit step.

---

## Default Success Criterion

A Misessessment is successful if:
- A future reader can understand the source material without watching it
- The Mise implications are obvious and grounded
- The document remains useful 6-12 months later
- No part feels like filler, jargon, or performance

---

End of Spec