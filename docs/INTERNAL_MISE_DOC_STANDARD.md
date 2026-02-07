# IMD Standard (Internal Mise Document)

**Canon Document — All CCWs Must Follow**

---

## Definition

An **IMD (Internal Mise Document)** is any official internal Mise document that requires branded formatting and archival. These are documents created by the Mise team for internal purposes: pitch decks, investment proposals, onboarding plans, strategy docs, meeting prep, etc.

When a user says "IMD [something]" or "create an IMD", the following standard applies.

**Important distinction:** An IMD is not the same as a **Mise Report** — the user-facing deliverable that the Mise product generates for restaurant managers (e.g., weekly payroll summaries, inventory reports, tip reports). IMDs are internal company documents. Mise Reports are product output for customers.

---

## Output Requirements

Every IMD produces **4 files**:

| # | File | Location | Lifespan |
|---|------|----------|----------|
| 1 | Markdown source | `~/mise-core/docs/internal_mise_docs/md_files/[NAME].md` | Permanent |
| 2 | Local PDF | `~/mise-core/docs/internal_mise_docs/[Category]/[NAME].pdf` | Permanent |
| 3 | "What's New" PDF | `mise_library/extra! extra!/[NAME].pdf` | 30 days, then deleted |
| 4 | Category PDF | `mise_library/[Category]/[NAME].pdf` | Permanent |

**Local base path:**
```
~/mise-core/docs/internal_mise_docs/
```

**Google Drive base path:**
```
/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/.shortcut-targets-by-id/125d9N_f2Jry6B1rLFicq8fmXsTvkShwb/Mise/Docs/mise_library/
```

**Category folders (same structure in both local and Google Drive):**

| Local Folder | Google Drive Folder | Contents |
|--------------|---------------------|----------|
| `investor_materials/` | `Investor Materials/` | Pitch decks, moat memos, investment asks |
| `investor_reading/` | `Investor Reading/` | Curated content for investors (research, articles, context) |
| `mise_restricted_section/` | `Mise Restricted Section/` | Investor-only long-form content: education, company culture, deep dives |
| `strategy_and_playbooks/` | `Strategy & Playbooks/` | AGI playbook, YC guide, operating frameworks |
| `onboarding/` | `Onboarding/` | Team and customer onboarding docs |
| `research/` | `Research/` | Market context, external research |
| `hiring/` | `Hiring/` | Job postings, contractor docs |
| `legal/` | `Legal/` | NDAs, contracts, agreements |
| `parked/` | `Parked/` | Ideas on hold until triggered

---

## Branding Standards

### Colors
| Name | Hex | Usage |
|------|-----|-------|
| Navy | `#1B2A4E` | Body text, h1, h3, accent line, table headers |
| Red | `#B5402F` | h2 headers, blockquote borders, links |
| Cream | `#F9F6F1` | Table alternating rows, horizontal rules, subtle backgrounds |

### Typography
- **Font:** Inter (with system fallbacks: -apple-system, BlinkMacSystemFont, sans-serif)
- **Body:** 11pt, line-height 1.6
- **H1:** 24pt, bold, Navy
- **H2:** 16pt, semibold, Red, with Cream bottom border
- **H3:** 13pt, semibold, Navy

### Logo
- **File:** `~/mise-core/Branding/Logo Files/Mise Logo No BG.png`
- **Placement:** Top-left with vertical Navy accent line (3px wide)
- **Max width:** 180px

### Bullet Points
- **Icon:** Mise audiowave (`~/mise-core/Branding/Logo Files/Icon No Background.png`)
- **Size:** 16px
- **Applied to:** All unordered lists (`<ul>`) automatically

### Page Setup
- **Size:** Letter (8.5" x 11")
- **Margins:** 0.75" all sides
- **Page numbers:** Bottom center, 10pt, Navy

---

## PDF Generation

Use WeasyPrint with the following CSS template:

```python
NAVY = '#1B2A4E'
RED = '#B5402F'
CREAM = '#F9F6F1'

css = f'''
@page {{
    size: letter;
    margin: 0.75in;
    @bottom-center {{
        content: counter(page);
        font-family: Inter, sans-serif;
        font-size: 10pt;
        color: {NAVY};
    }}
}}
body {{
    font-family: Inter, -apple-system, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: {NAVY};
}}
.logo-header {{
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
    padding-bottom: 15px;
}}
.logo-header .accent-line {{
    width: 3px;
    background-color: {NAVY};
    margin-right: 15px;
    min-height: 80px;
    align-self: stretch;
}}
.logo-header img {{
    max-width: 180px;
    height: auto;
}}
h1 {{ font-weight: 700; font-size: 24pt; color: {NAVY}; margin-top: 0; }}
h2 {{ font-weight: 600; font-size: 16pt; color: {RED}; margin-top: 24px; border-bottom: 1px solid {CREAM}; padding-bottom: 6px; }}
h3 {{ font-weight: 600; font-size: 13pt; color: {NAVY}; margin-top: 18px; }}
p {{ margin-bottom: 12px; }}
ul, ol {{ margin-bottom: 12px; padding-left: 24px; }}
li {{ margin-bottom: 6px; }}
hr {{ border: none; border-top: 2px solid {CREAM}; margin: 24px 0; }}
strong {{ font-weight: 600; color: {NAVY}; }}
em {{ font-style: italic; }}
blockquote {{ border-left: 4px solid {RED}; margin: 16px 0; padding: 12px 20px; background-color: {CREAM}; font-style: italic; }}
table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 10pt; }}
th {{ background-color: {NAVY}; color: white; font-weight: 600; text-align: left; padding: 10px 12px; border: 1px solid {NAVY}; }}
td {{ padding: 8px 12px; border: 1px solid #ddd; vertical-align: top; }}
tr:nth-child(even) {{ background-color: {CREAM}; }}
'''
```

### HTML Structure

```html
<div class="logo-header">
    <div class="accent-line"></div>
    <img src="[base64-encoded-logo]" alt="Mise Logo">
</div>
[markdown-converted-to-html]
```

---

## Visual Aids

IMDs support rich visual elements. Use HTML blocks in markdown to access these styles.

### Callout Boxes

Four types available: `note`, `tip`, `warning`, `important`

```html
<div class="callout note" markdown="1">
<div class="callout-title">📝 Note</div>
This is additional context or background information.
</div>

<div class="callout tip" markdown="1">
<div class="callout-title">💡 Tip</div>
A helpful suggestion or best practice.
</div>

<div class="callout warning" markdown="1">
<div class="callout-title">⚠️ Warning</div>
Something to watch out for.
</div>

<div class="callout important" markdown="1">
<div class="callout-title">🔴 Important</div>
Critical information that must not be missed.
</div>
```

### Pull Quotes

Large, centered quotes for emphasis:

```html
<div class="pull-quote">
"The quote text goes here — make it impactful."
<div class="attribution">— Attribution</div>
</div>
```

### Stat Boxes

Display key metrics prominently:

```html
<div class="stats-row">
<div class="stat-box">
<div class="number">97%</div>
<div class="label">Time Saved</div>
</div>
<div class="stat-box">
<div class="number">$4.2M</div>
<div class="label">Payroll Processed</div>
</div>
</div>
```

### Icons & Symbols

Use Unicode symbols directly in text:

| Icon | Code | Usage |
|------|------|-------|
| ✓ | `✓` | Success, included, yes |
| ✗ | `✗` | Failure, excluded, no |
| → | `→` | Flow, next step, leads to |
| ★ | `★` | Highlight, important |
| 📝 | `📝` | Note |
| 💡 | `💡` | Tip, idea |
| ⚠️ | `⚠️` | Warning |
| 🔴 | `🔴` | Critical, important |
| 📌 | `📌` | Pinned, key point |

### Diagrams

ASCII diagrams with monospace styling:

```html
<div class="diagram">
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   MANAGER    │ ──→ │  TRANSROUTER │ ──→ │    AGENT     │
│   (Voice)    │     │   (Parse)    │     │   (Execute)  │
└──────────────┘     └──────────────┘     └──────────────┘
</div>
```

For images/charts, use standard figure markup:

```html
<figure>
<img src="path/to/image.png" alt="Description">
<figcaption>Figure 1: Caption text here</figcaption>
</figure>
```

### Timeline

Show progression of events:

```html
<div class="timeline">
<div class="timeline-item">
<div class="date">Q3 2025</div>
<div class="event">Launched at Papa Surf</div>
</div>
<div class="timeline-item">
<div class="date">Q1 2026</div>
<div class="event">Seed round closed</div>
</div>
</div>
```

### Comparison Tables

For yes/no feature comparisons:

```html
<table class="comparison">
<tr><th>Feature</th><th>Mise</th><th>Competitor</th></tr>
<tr><td>Voice-first</td><td class="yes">✓ Yes</td><td class="no">✗ No</td></tr>
</table>
```

---

## Versioning

IMDs can be revised. When an IMD is edited, a new version is created and placed in "extra! extra!" for 30 days.

### Version Numbering

| Version | When to Use |
|---------|-------------|
| `_v2.0` | Major revision — significant content changes, new sections, structural rewrites |
| `_v2.1` | Minor revision — small fixes, clarifications, typo corrections to v2 |
| `_v2.2` | Another minor fix to v2 |
| `_v3.0` | Next major revision |
| `_v3.1` | Minor revision to v3 |

**Rule:** If the change affects the document's meaning or conclusions, it's a major version. If it's just a fix or clarification, it's a minor version.

### Filename Convention

```
[NAME]_v[VERSION].pdf

Examples:
- Mise_Moat_Memo_v2.0.pdf
- Austin_Onboarding_Plan_v2.1.pdf
- Executive_Summary_v3.0.pdf
```

### Revision History Block

Every revised IMD must include a **Revision History** section immediately after the title. This explains what changed and why.

```markdown
# Document Title

**Revision History**

| Version | Date | Changes |
|---------|------|---------|
| v2.0 | Feb 10, 2026 | Added section on competitive moats; removed outdated pricing |
| v1.0 | Feb 5, 2026 | Original document |

---

[Rest of document...]
```

### Workflow for Revisions

1. Edit the markdown source file
2. Add/update the Revision History table at the top
3. Regenerate the PDF with the new version suffix
4. Copy the new PDF to `mise_library/extra! extra!/`
5. Old version stays in its category folder (or extra! extra! if still <31 days old)

### What Happens to Old Versions

- Old versions are **kept** — they're not deleted
- When a new version goes to "extra! extra!", the old version stays where it was
- After 31 days, the new version moves to its category folder alongside the old version
- This creates a complete revision history in each category folder

---

## Document Footer

Every IMD should end with:

```markdown
---

*Mise: Everything in its place.*
```

---

## Quick Reference for CCWs

When user says "IMD [something]" or "create an IMD":

1. Convert content to clean markdown
2. Save markdown to `~/mise-core/docs/internal_mise_docs/md_files/[NAME].md`
3. Generate branded PDF using WeasyPrint + above CSS
4. Save PDF to `~/mise-core/docs/internal_mise_docs/[Category]/[NAME].pdf`
5. Copy PDF to Google Drive `mise_library/extra! extra!/[NAME].pdf`
6. Copy PDF to Google Drive `mise_library/[Category]/[NAME].pdf`
7. Confirm all 4 files created

---

## Existing Generator Script

A reusable generator exists at:
```
~/mise-core/docs/internal_mise_docs/generate_imd.py
```

Usage:
```bash
python generate_imd.py <markdown_file> <category>
```

Example:
```bash
python generate_imd.py md_files/IMD_Founder_Listening_Curriculum.md strategy_and_playbooks
```

---

*This standard is canon. All Claude Code Windows must follow it when generating IMDs.*
