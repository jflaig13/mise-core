# Research Learning Pipeline

*Mandatory analysis structure for all research work in this project.*

This file defines how research must be conducted. Every research task follows these stages in order. Skipping stages produces shallow work. The pipeline exists to ensure that raw input is transformed into something Mise can actually use.

This file does not create law. It sets quality standards.

---

## Stage 1: Transcription / Ingest

**Purpose:** Capture the raw source material in a stable, reviewable form.

**Process:**
- [ ] Identify the source (article, talk, podcast, paper, conversation, dataset)
- [ ] Record the source metadata (author, date, URL/location, format)
- [ ] If audio/video: transcribe to text
- [ ] If long-form text: extract key passages with page/section references
- [ ] Store the raw ingest in the research file with clear attribution

**Output:** Verbatim or near-verbatim source material, properly cited.

---

## Stage 2: Comprehension

**Purpose:** Understand what is actually being said — not what you assume is being said.

**Process:**
- [ ] Summarize the source's core argument or thesis in 2-3 sentences
- [ ] Identify the author's context (who are they, what is their perspective, what are they selling)
- [ ] Note any assumptions the source makes that may not hold for Mise
- [ ] Flag anything ambiguous or contradictory within the source itself

**Output:** A plain-language summary that someone unfamiliar with the source could read and understand the main point.

---

## Stage 3: Invariant Extraction

**Purpose:** Identify durable principles — things that are likely true regardless of context.

**Process:**
- [ ] Separate opinions from observations
- [ ] Separate time-bound claims from structural claims
- [ ] Ask: "Would this still be true in 5 years? In a different industry? At a different scale?"
- [ ] Extract 1-5 candidate invariants (if any exist — not every source produces invariants)
- [ ] Assign a confidence level to each (low / medium / high)

**Output:** A short list of candidate invariants with confidence ratings. These may later be logged in `INVARIANTS_LOG.md`.

---

## Stage 4: System-Level Synthesis

**Purpose:** Understand how this insight fits into the broader system — not just the narrow topic.

**Process:**
- [ ] What system does this insight belong to? (product, GTM, hiring, operations, AI, legal, culture)
- [ ] What other systems does it touch or interact with?
- [ ] Are there second-order effects? (If we act on this, what else changes?)
- [ ] Does this reinforce, contradict, or extend anything we already believe?

**Output:** A paragraph or short section explaining where this insight sits in the larger picture.

---

## Stage 5: Mise-Specific Translation

**Purpose:** Convert general insight into Mise-relevant terms.

**Process:**
- [ ] Does this apply to Mise's current stage? (pre-seed, single client, two founders)
- [ ] Does this apply to Mise's market? (independent restaurants, voice-first ops)
- [ ] Does this apply to Mise's architecture? (multi-agent, audio-first, FastAPI)
- [ ] If the insight is general, what is the Mise-specific version of it?
- [ ] If the insight does not apply to Mise, say so explicitly and stop here

**Output:** The insight restated in Mise-specific language, or an explicit statement that it does not apply.

---

## Stage 6: Actionable Directives

**Purpose:** If this insight suggests action, state the action clearly.

**Process:**
- [ ] Does this insight recommend a product change? State what.
- [ ] Does this insight recommend a strategy shift? State what.
- [ ] Does this insight recommend further research? State the question.
- [ ] Does this insight recommend a conversation with a specific person? State who and why.
- [ ] If no action is recommended, say: "Informational only. No action recommended at this time."

**Output:** A numbered list of concrete recommendations, or an explicit "no action" statement.

---

## Stage 7: The Final Question

**Purpose:** Force a direct answer to the question that justifies doing this research at all.

**The question:**

> "What does this change about how Mise should think, build, or act?"

**Process:**
- [ ] Answer in 1-3 sentences
- [ ] If the answer is "nothing," that is a valid and useful answer — it means the research confirmed existing direction or found nothing actionable
- [ ] If the answer is something, it should connect directly to Stage 6 recommendations

**Output:** A direct, honest answer. No hedging. No "it depends." If you cannot answer this question, the research is not finished.
