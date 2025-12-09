# Local Inventory Machine (LIM)

Purpose / Scope
- Converts long-form restaurant inventory audio into structured, verifiable data and a MarginEdge-ready CSV export.
- Second major Mise workflow (alongside the Local Payroll Machine) and a key piece of Wedge v2 demos/early deployment.
- Performs SKU normalization, fuzzy matching, unit conversions, fractional bottles, pack sizing, and aggregation across zones (Truck, Walk-In, Inside Bar, Back Bar, Upstairs).
- Interpreter-assisted parsing today (ChatGPT resolves ambiguities, normalizes distortions); future plan is a deterministic internal model.

Repo Location
- data/Inventory/
  - <DATE>_Inventory.txt — Whisper transcript
  - inventory_catalog.json — enterprise catalog
- mise_inventory/
  - parser.py — main inventory parser (tokenize, fuzzy match, normalize, aggregate)
  - normalizer.py — SKU normalization (handles phonetic variants, consolidations)
  - tokenizer.py — transcript segmentation
  - validator.py — schema/quantity checks
  - catalog_loader.py — load/expand roster/catalog
  - generate_inventory_file.py — produce ME-ready CSV/XLSX
  - inventory_schema.json — output schema
- scripts/
  - convert_m4a_to_wav.sh — optional audio preprocessor
  - grow_catalog.py — catalog expansion utility

Main Entry Points / Scripts
1) mise_inventory/parser.py
   - Reads Whisper transcript, tokenizes, fuzzy-matches SKUs, normalizes, extracts quantities, aggregates zones, validates against inventory_schema.json.
2) mise_inventory/generate_inventory_file.py
   - Given structured JSON inventory, produces `MMDDYY_Inventory_MEExport.csv` (MarginEdge import file).
3) mise_inventory/normalizer.py
   - Canonicalizes distorted/variant expressions (e.g., aperol variants → Aperol; Mom Water → Linda; High Noon flavors consolidated) and Whisper quirks.
4) mise_inventory/tokenizer.py
   - Breaks long-form transcripts into parseable segments.
5) mise_inventory/validator.py
   - Enforces schema, flags missing/mis-categorized/invalid quantities.

Key Inputs
- Whisper transcript: `MMDDYY_Inventory.txt`
- `inventory_catalog.json` (SKU definitions, fuzzy rules, synonyms, pack sizes)
- Internal roster via catalog_loader

Key Outputs
- Structured JSON inventory
- MarginEdge-ready CSV via generate_inventory_file.py
- Both saved locally under the Mise directory structure.

Environment Variables
- Typically none required.
- Optional: INVENTORY_TRANSCRIPT_DIR, INVENTORY_OUTPUT_DIR (if overriding defaults).

Execution Flow
1) Record full inventory audio.
2) Whisper creates `MMDDYY_Inventory.txt`.
3) Run parser:
   `python -m mise_inventory.parser data/Inventory/MMDDYY_Inventory.txt data/inventory_catalog.json output/MMDDYY_Inventory.json`
4) Generate MarginEdge CSV:
   `python -m mise_inventory.generate_inventory_file output/MMDDYY_Inventory.json output/MMDDYY_Inventory_MEExport.csv`
   (The JSON from step 3 is the input to the runner that builds the CSV.)

Interpreter Note
- LIM (and Local Payroll Machine) currently rely on ChatGPT as interpreter to bridge messy speech → structured data. Post-funding, this will be codified into a deterministic internal model.
