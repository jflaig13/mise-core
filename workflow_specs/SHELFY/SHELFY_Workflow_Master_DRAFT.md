# Shelfy Workflow Master Spec — DRAFT

**Status:** DRAFT - First pass, to be refined
**Owner:** ccw6 (Backend), ccw2 (Frontend)
**Last Updated:** 2026-01-18

---

## 1. What is Shelfy?

Shelfy is Mise's voice-first inventory recording system. It's the first product Mise will bring to market.

**Core concept:** Manager walks through restaurant, records inventory counts by area, Mise transcribes and structures the data into deliverable spreadsheets.

| Term | Definition |
|------|------------|
| **Shelfy** (singular) | One voice recording for one inventory area |
| **Shelfies** (plural) | Multiple inventory recordings |
| **Area** | Physical section being counted (Walk-in, Back Bar, etc.) |
| **Period** | Inventory period, identified by last day of month (e.g., `2026-01-31`) |

---

## 2. Areas by Category

### Kitchen (Food Inventory)
- Dry Goods
- Kitchen/Line
- Walk-in
- Dish Pit/Chest Freezers
- Inside Bar
- Back Bar
- Misc

### Bar (Alcohol Inventory)
- The Office
- Inside Bar
- Back Bar
- Walk-in
- Offsite Storage Unit
- Misc

---

## 3. User Flow

1. User opens /inventory → "Record a Shelfy" button
2. Select Category → Kitchen or Bar
3. Select Area → Walk-in, Back Bar, etc.
4. Record → Speak inventory count
5. Processing → Transcribed via Whisper
6. Approve → Review and confirm
7. Deliverable → (Future: email spreadsheet)

---

## 4. Current Implementation (Lite)

**Files:**
- `mise_app/shelfy_storage.py` — Storage, date normalization, areas
- `mise_app/routes/inventory.py` — API + HTML routes

**Endpoints:**
- POST /inventory/record_shelfy
- POST /inventory/approve_shelfy
- GET /inventory/totals/{period_id}
- GET /inventory/shelfy/{shelfy_id}
- GET /inventory/areas
- GET /inventory/periods

---

## 5. Known Limitations

1. OpenAI Whisper 25MB limit (~4-5 min audio)
2. 60-second timeout too short for long recordings
3. No product parsing (raw transcript only)

**Planned solution:** Async processing + email delivery

---

## 6. TODO for Full Version

- [ ] Async email delivery for long recordings
- [ ] Audio compression before upload
- [ ] Inventory AI agent for parsing items/quantities
- [ ] Product catalog matching
- [ ] Previous inventory context
- [ ] MarginEdge integration

---

*This is a first draft. To be refined tomorrow.*
