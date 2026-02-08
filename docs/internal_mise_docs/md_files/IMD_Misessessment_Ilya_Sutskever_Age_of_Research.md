# Misessessment — Ilya Sutskever: "We're Moving from the Age of Scaling to the Age of Research"

**Date:** 2026-02-07

**Mise State Snapshot:**

Mise is actively shipping features in the web app and tightening core workflows. Claude Code drives rapid iteration across the entire system.

Payroll and inventory workflows are live and increasingly tested under real restaurant conditions. Papa Surf continues to run Mise every week. This is not a demo environment.

A verbal commitment for $50k in funding has been received. The focus is shifting from building to proving — reliability, defensibility, and readiness for outside scrutiny.

Mise is still early. But it is already operating where it matters: inside a real restaurant, handling real money, under real pressure.

---

## 1. Source Technicality Assessment

**Technicality Level: Medium–High**

The talk is not mathematical, but it assumes familiarity with how modern artificial intelligence systems are built and improved. It contains conceptual language that sounds simple but hides deep technical meaning. Without translation, it's easy to mistake confidence for clarity or miss the practical implications.

---

## 2. Plain-Language Summary of the Material

Ilya Sutskever's core argument is simple but important:

For a long time, artificial intelligence got better by doing more of the same thing. Bigger systems, more data, more computers. That phase worked extremely well, but it is no longer enough on its own.

He calls that earlier phase the "age of scaling."

### What "scaling" means (called out explicitly)

**Scaling** means improving a system by increasing size and volume:

- Bigger models
- More training data
- More computing power

This worked because early systems were still far from understanding language well. Feeding them more examples helped a lot.

### What "pre-training" means (called out explicitly)

**Pre-training** is when an artificial intelligence system is trained by reading massive amounts of general text (books, websites, conversations) without being taught a specific job.

It's like teaching someone to read and understand English before training them to be an accountant or manager.

You will hear "pre-training" again in:

- Model vendor marketing
- Investor discussions about "foundation models"
- Claims that a model is "generally intelligent"

### The key shift Ilya is pointing to

The problem now is not that systems aren't smart enough. The problem is that they are **unreliable in real situations**.

They can:

- Do something perfectly one moment
- Fail badly when the situation changes slightly

This happens because:

- They were trained to look good on tests
- Not trained deeply enough on messy, real-world conditions

Ilya argues we are entering the "age of research," meaning:

- Progress now comes from understanding *why* systems fail
- And designing better ways for them to learn from mistakes

Not just making them bigger.

### Another concept he points out (called out explicitly)

**Evaluation** (often shortened to "evals") — This means the tests people use to decide whether a system is "good."

He warns that systems can become good at passing tests without being good in reality.

You will see this again in:

- AI benchmarks
- Product demos
- Internal metrics that look great but don't match user experience

---

## 3. What This Means for Mise (Time-Horizon Analysis)

### d = 0 (Now)

Mise is already living in the world Ilya describes.

Restaurants are messy. Audio is noisy. People correct themselves. Rules change mid-sentence. There is no clean test environment.

This means:

- Mise cannot rely on "better models" alone.
- The real advantage must come from how Mise handles mistakes, corrections, and edge cases.

### d = 30

Mise should begin treating real failures as first-class product inputs.

That means:

- Capturing when the system is corrected
- Treating those corrections as valuable learning signals
- Tracking *why* something failed, not just that it failed

This is the start of "research" in the Ilya sense.

### d = 90

Mise should have a small but growing internal library of:

- Real transcripts
- Real corrections
- Real edge cases

This becomes Mise's equivalent of "training data," but higher quality than generic data because it reflects real operations.

Competitors without this will look impressive in demos and fall apart in real use.

### d = 180

By this point, Mise should be measurably more reliable in:

- Payroll math
- Inventory counts
- Handling corrections and restatements

Not because it is "smarter," but because it has learned from real mistakes repeatedly.

This is where defensibility begins to form.

### d = 360

If done correctly, Mise's system will generalize better across:

- Different managers
- Different restaurants
- Different speaking styles
- Different operational quirks

This is exactly the problem Ilya identifies as the hardest and most important: reliability across variation.

---

## 4. Recommended Courses of Action for Mise

### 1. Treat reliability as the core product, not intelligence

- **Why:** The talk makes clear that smart-but-unreliable systems stall out.
- **What would make this wrong:** If restaurants suddenly became clean, predictable environments (they won't).
- **What to measure:** Error rates, correction frequency, repeat failures of the same type.

### 2. Design workflows that capture corrections automatically

- **Why:** Corrections are the most valuable learning signal.
- **What would make this wrong:** If corrections are rare or low-signal (they aren't).
- **What to measure:** How often corrections happen and whether the system improves afterward.

### 3. Evaluate Mise using real restaurant conditions only

- **Why:** Tests and demos lie; reality doesn't.
- **What would make this wrong:** If internal tests strongly predict real-world success (unlikely long-term).
- **What to measure:** Performance on real closes, not staged examples.

### 4. Avoid chasing "bigger AI" as a primary strategy

- **Why:** Ilya's argument is that this phase is over as the main lever.
- **What would make this wrong:** A sudden breakthrough that eliminates real-world brittleness (not currently visible).
- **What to measure:** Marginal improvement per model upgrade versus workflow improvements.

---

## 5. Net Effect on Mise's Thinking, Building, or Acting

This should change Mise's mindset from "using advanced AI" to "building a system that gets more dependable every time a real restaurant uses it."

---

*Mise: Everything in its place.*
