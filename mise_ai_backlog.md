# Mise AI Backlog / Session Notes

## State (Cycle 3)
- Parser layers: catalog loader (merges papa_surf_roster.csv), normalizer, tokenizer, validator, quantity parsing (fractions/percent/pack multipliers), JSON writer.
- Tokenizer now splits repeated quantity phrases and simple and/comma cases.
- Normalization is OFF by default; fuzzy is opt-in with --normalize.
- Validation checks items against catalog and reports errors; unmatched lines are printed for catalog growth.
- Tests: quantity parsing, tokenizer; payroll tests skipped for now.

## Known Issues / Gaps
- Many narrative/multi-item lines remain unmatched (see latest parser run output).
- Normalization thresholds not tuned; risk of over/under replacement if enabled.
- Catalog needs growth from unmatched lines; grow_catalog.py not yet used this cycle.
- No structured guidance for adding new aliases/case sizes from unmatched lines.

## Next Actions (suggested)
1) Improve multi-item sentence splitting: add rule-based splitter for sequences like "one can X one can Y" and narrative intros (ignore non-quantity preamble).
2) Add normalization guardrails: higher fuzzy threshold, limit replacement span, maybe disable fuzzy on long sentences.
3) Run scripts/grow_catalog.py on unmatched lines to add aliases/case_size for common misses.
4) Add tests for multi-item narratives and catalog validation errors.

## Heuristics / Lessons
- Keep fuzzy normalization opt-in to avoid garbling; prefer explicit catalog growth.
- Split only when quantity tokens repeat; avoid over-splitting narrative text without quantities.
- Always validate against catalog and surface unmatched lines for human review.

## Parking Lot
- Re-enable payroll-engine tests once inventory changes are stable.
- Consider property-based tests for tokenizer/quantity parsing.
- Add optional per-category parsing rules (e.g., canned vs bottle case sizing).
