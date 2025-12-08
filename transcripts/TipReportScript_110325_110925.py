from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
import pandas as pd

# ================== APPROVED DATA (Nov 3–Nov 9, 2025) ==================
SHIFT_COLS = ["MAM","MPM","TAM","TPM","WAM","WPM","ThAM","ThPM","FAM","FPM","SaAM","SaPM","SuAM","SuPM"]

# Per-shift FINAL amounts (after tip-out)
per_shift = {
    "John Neal":     {"MAM":87.59, "TAM":205.47, "WAM":181.49},
    "Austin Kelley": {"MPM":196.86, "TPM":157.55, "ThAM":218.71, "ThPM":206.73, "FAM":185.80, "FPM":448.00},
    "Mark Buryanek": {"MPM":196.86, "FPM":448.00, "SaAM":219.66, "SaPM":319.28},
    "Maddox Porter": {"MPM":44.63,  "TPM":51.41,  "ThAM":35.41,  "ThPM":61.06,  "FAM":38.70,  "FPM":200.00},
    "Janel Baki":    {"TPM":157.55, "FPM":448.00},
    "Heather Martin":{"ThPM":206.73},
    "Kevin Worley":  {"FPM":448.00, "SaAM":219.66, "SaPM":319.28, "SuAM":104.93, "SuPM":264.91},
    "Mike Walton":   {"WPM":91.85,  "SuAM":104.93, "SuPM":42.37},
    "Brooke Neal":   {"WPM":91.85},
    "Coben Cross":   {"MAM":19.35,  "WAM":38.06,  "WPM":31.20,  "SaPM":91.77,  "SuAM":40.74, "SuPM":48.35},
}

# Cook tips (weekly totals page only)
cook_tips = {"Warren Lewis": 13.57}

# Weekly Totals (approved)
weekly_totals = {
    "Austin Kelley": 1887.30,
    "Kevin Worley": 1619.58,
    "John Neal": 474.55,
    "Mark Buryanek": 1539.50,
    "Janel Baki": 762.55,
    "Heather Martin": 206.73,
    "Mike Walton": 239.15,
    "Brooke Neal": 91.85,
    "Maddox Porter": 469.48,
    "Coben Cross": 309.24,
    "Warren Lewis": 13.57,
}

# Detailed Math (Page 3+) — full first+last names in every line
DETAIL_BLOCKS = [
    ("Mon Nov 3 — AM", [
        "John Neal pre-tip $106.94 – Coben Cross $19.35 = John Neal $87.59",
        "Utility: Coben Cross $19.35",
    ]),
    ("Mon Nov 3 — PM (finals)", [
        "Austin Kelley $196.86, Mark Buryanek $196.86, Maddox Porter $44.63",
    ]),
    ("Tue Nov 4 — AM (final)", [
        "John Neal $205.47 (no tip-out)",
    ]),
    ("Tue Nov 4 — PM (finals)", [
        "Austin Kelley $157.55, Janel Baki $157.55, Maddox Porter $51.41",
    ]),
    ("Wed Nov 5 — AM", [
        "John Neal pre-tip $219.55 – Coben Cross $38.06 = John Neal $181.49",
        "Utility: Coben Cross $38.06",
    ]),
    ("Wed Nov 5 — PM (finals)", [
        "Mike Walton $91.85, Brooke Neal $91.85, Coben Cross $31.20",
    ]),
    ("Thu Nov 6 — AM", [
        "Austin Kelley pre-tip $254.12 – Maddox Porter $35.41 = Austin Kelley $218.71",
        "Utility: Maddox Porter $35.41",
    ]),
    ("Thu Nov 6 — PM (finals)", [
        "Austin Kelley $206.73, Heather Martin $206.73, Maddox Porter $61.06",
    ]),
    ("Fri Nov 7 — AM", [
        "Austin Kelley pre-tip $224.50 – Maddox Porter $38.70 = Austin Kelley $185.80",
        "Utility: Maddox Porter $38.70",
    ]),
    ("Fri Nov 7 — PM (finals)", [
        "Austin Kelley $448.00, Kevin Worley $448.00, Janel Baki $448.00, Mark Buryanek $448.00, Maddox Porter $200.00",
    ]),
    ("Sat Nov 8 — AM (finals)", [
        "Kevin Worley $219.66, Mark Buryanek $219.66 (no tip-out)",
    ]),
    ("Sat Nov 8 — PM (finals)", [
        "Kevin Worley $319.28, Mark Buryanek $319.28, Coben Cross $91.77",
    ]),
    ("Sun Nov 9 — AM (finals)", [
        "Kevin Worley $104.93, Mike Walton $104.93, Coben Cross $40.74",
    ]),
    ("Sun Nov 9 — PM (finals)", [
        "Kevin Worley $264.91, Mike Walton $42.37, Coben Cross $48.35",
    ]),
]

# ================== BUILD PDF ==================
pdf_path = "TipReport_110325_110925.pdf"
styles = getSampleStyleSheet()
style_title = styles["Title"]
style_heading = ParagraphStyle("Heading", parent=styles["Heading2"], spaceAfter=10, textColor=colors.darkblue)
style_shift = ParagraphStyle("Shift", parent=styles["Heading3"], spaceAfter=6, textColor=colors.darkred)
style_normal = styles["Normal"]

doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter),
                        leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24)
story = []

# Header
story += [
    Paragraph("Papa Surf Burger Bar — Tip Report", style_title),
    Paragraph("Week of November 3–9, 2025", style_heading),
    Spacer(1, 12)
]

# Page 1 — Weekly Totals
tot_rows = [["Employee", "Weekly Total ($)"]]
for emp, val in sorted(weekly_totals.items(), key=lambda x: (x[0].split()[-1].lower(), x[0].split()[0].lower())):
    tot_rows.append([emp, f"${val:,.2f}"])
tot_tbl = Table(tot_rows, hAlign="LEFT", colWidths=[260, 120])
tot_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("GRID",       (0,0), (-1,-1), 0.25, colors.grey),
    ("FONTNAME",   (0,0), (-1,0),  "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey]),
    ("ALIGN",      (1,1), (-1,-1), "RIGHT"),
]))
story += [Paragraph("Weekly Totals (Alphabetical by Last Name; cooks included)", style_heading), tot_tbl, PageBreak()]

# Page 2 — Shift Matrix
all_emps = sorted(set(per_shift.keys()) | set(cook_tips.keys()),
                  key=lambda s: (s.split()[-1].lower(), s.split()[0].lower()))
matrix = [["Employee"] + SHIFT_COLS]
for emp in all_emps:
    row = [emp]
    for c in SHIFT_COLS:
        v = per_shift.get(emp, {}).get(c, "")
        row.append("" if v=="" else f"${v:,.2f}")
    matrix.append(row)

mt = Table(matrix, hAlign="LEFT", repeatRows=1)
mt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("GRID",       (0,0), (-1,-1), 0.25, colors.grey),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey]),
    ("ALIGN",      (1,1), (-1,-1), "RIGHT"),
]))
story += [Paragraph("Shift Breakdown (MAM → SuPM)", style_heading), mt, PageBreak()]

# Page 3+ — Detailed Math
for title, lines in DETAIL_BLOCKS:
    story.append(Paragraph(title, style_shift))
    for ln in lines:
        story.append(Paragraph(ln, style_normal))
    story.append(Spacer(1, 10))

doc.build(story)

# ================== BUILD EXCEL ==================
weekly_df = pd.DataFrame(sorted(weekly_totals.items(),
                     key=lambda x: (x[0].split()[-1].lower(), x[0].split()[0].lower())),
                     columns=["Employee","Weekly Total ($)"])

rows = []
for emp in all_emps:
    row = {"Employee": emp}
    for c in SHIFT_COLS:
        row[c] = per_shift.get(emp, {}).get(c, "")
    rows.append(row)
matrix_df = pd.DataFrame(rows, columns=["Employee"] + SHIFT_COLS)

with pd.ExcelWriter("TipReport_110325_110925.xlsx", engine="openpyxl") as w:
    weekly_df.to_excel(w, index=False, sheet_name="Weekly Totals")
    matrix_df.to_excel(w, index=False, sheet_name="Shift Breakdown")

print("Generated TipReport_110325_110925.pdf and TipReport_110325_110925.xlsx")
