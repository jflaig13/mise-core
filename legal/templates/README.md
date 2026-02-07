# Legal Document Templates

## Standard: Clean Legal PDFs

All legal documents use **clean, professional formatting**:
- White background
- Black text
- Times New Roman font
- No branding, no colors
- 1-inch margins

**Do NOT use IMD branding for legal documents.**

---

## Generating Legal PDFs

```bash
cd ~/mise-core/legal/templates
python3 generate_legal_pdf.py <template>.md
```

Example:
```bash
python3 generate_legal_pdf.py Initial_Board_Resolutions_TEMPLATE.md
```

Output goes to same directory as `.pdf`.

---

## DocuSign Integration

Templates include anchor tags for DocuSign auto-detection:

| Anchor Format | Field Type |
|---------------|------------|
| `/SignName/` | Signature field |
| `/DateName/` | Date field |
| `/TextFieldName/` | Text input field |
| `/InitialsName/` | Initials field |

When uploading to DocuSign, use "Auto-Place" to detect these anchors.

---

## Templates

| Template | Purpose |
|----------|---------|
| `Initial_Board_Resolutions_TEMPLATE.md` | Founding board resolutions (shares, officers, bylaws) |
| `Founder_IP_Assignment_TEMPLATE.md` | Transfer founder IP to company |
| `Terms_of_Service_TEMPLATE.md` | User agreement for Mise platform |
| `Privacy_Policy_TEMPLATE.md` | CCPA-compliant privacy policy |
| `Written_Consent_TEMPLATE.md` | Template for future board actions |

---

## Workflow

1. Edit the `.md` template
2. Run `python3 generate_legal_pdf.py <template>.md`
3. Upload PDF to DocuSign
4. Use Auto-Place to detect fields
5. Assign signers and send

---

## Storage

- **Source files:** `~/mise-core/legal/templates/`
- **Executed documents:** Google Drive `/Docs/Legal/`
- **Board consents:** Google Drive `/Docs/Legal/Board Consents/`
