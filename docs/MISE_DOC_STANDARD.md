# Mise Doc Standard

**Canon Document — All CCWs Must Follow**

---

## Definition

A **Mise doc** is any official Mise document that requires branded formatting and archival. When a user says "make this a Mise doc" or "create a Mise doc", the following standard applies.

---

## Output Requirements

Every Mise doc produces **3 files**:

| # | File | Location |
|---|------|----------|
| 1 | Markdown source | `~/mise-core/fundraising/[NAME].md` |
| 2 | Branded PDF | `~/mise-core/fundraising/[NAME].pdf` |
| 3 | Archived PDF | `Google Drive (jonathan@papasurf.com)/Mise/docs/mise_library/[NAME].pdf` |

**Google Drive full path:**
```
/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Mise/docs/mise_library/
```

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
- **File:** `~/mise-core/Branding/Logo Files/Updated Mise Logo Pronunciation.png`
- **Placement:** Top-left with vertical Navy accent line (3px wide)
- **Max width:** 180px

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

## Document Footer

Every Mise doc should end with:

```markdown
---

*Mise: Everything in its place.*
```

---

## Quick Reference for CCWs

When user says "make this a Mise doc":

1. Convert content to clean markdown
2. Save markdown to `~/mise-core/fundraising/[NAME].md`
3. Generate branded PDF using WeasyPrint + above CSS
4. Save PDF to `~/mise-core/fundraising/[NAME].pdf`
5. Copy PDF to Google Drive mise_library folder
6. Confirm all 3 files created

---

## Existing Generator Script

A reusable generator exists at:
```
~/mise-core/fundraising/generate_branded_pdf.py
```

This can be extended to handle new documents by adding them to the `main()` function.

---

*This standard is canon. All Claude Code Windows must follow it.*
