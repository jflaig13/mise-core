import json, sys, os
from pathlib import Path
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
DEFAULT_BASE = ROOT_DIR / "Transcripts"
FALLBACK_BASE = Path("/Users/jonathanflaig/Transcripts")

def resolve_base_dir() -> Path:
    env_base = os.environ.get("LPM_TRANSCRIPTS_BASE")
    if env_base:
        return Path(env_base)
    if DEFAULT_BASE.exists():
        return DEFAULT_BASE
    if FALLBACK_BASE.exists():
        return FALLBACK_BASE
    return DEFAULT_BASE

def main(p):
    with open(p, 'r') as f:
        cfg = json.load(f)

    out_base   = cfg["out_base"]                         # e.g. "TipReport_110325_110925"
    per_shift  = cfg["per_shift"]                        # { "Employee": {"MAM": 123.45, ...}, ... }
    cook_tips  = cfg.get("cook_tips", {})                # { "Cook Name": 12.34 }
    weekly     = cfg["weekly_totals"]                    # { "Employee": total }
    detail     = cfg.get("detail_blocks", [])            # [ [title, [lines...]], ... ]
    shift_cols = cfg.get("shift_cols", ["MAM","MPM","TAM","TPM","WAM","WPM","ThAM","ThPM","FAM","FPM","SaAM","SaPM","SuAM","SuPM"])
    header     = cfg.get("header", "Tip Report")

    # ----- PDF -----
    base_dir = resolve_base_dir()

    base = out_base.replace("TipReport_", "")
    report_dir = base_dir / "Tip_Reports" / base
    os.makedirs(report_dir, exist_ok=True)
    pdf_path = os.path.join(report_dir, f"{out_base}.pdf")
    styles = getSampleStyleSheet()
    style_title  = styles["Title"]
    style_heading= ParagraphStyle("Heading", parent=styles["Heading2"], spaceAfter=10, textColor=colors.darkblue)
    style_shift  = ParagraphStyle("Shift",   parent=styles["Heading3"], spaceAfter=6,  textColor=colors.darkred)
    style_norm   = styles["Normal"]

    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter),
                            leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24)
    story = []
    story += [Paragraph("Papa Surf Burger Bar — Tip Report", style_title),
              Paragraph(header, style_heading), Spacer(1, 12)]

    # Page 1: Weekly Totals (alpha by last name)
    tot_rows = [["Employee","Weekly Total ($)"]]
    for emp, val in sorted(weekly.items(), key=lambda x: (x[0].split()[-1].lower(), x[0].split()[0].lower())):
        tot_rows.append([emp, f"${val:,.2f}"])
    t = Table(tot_rows, hAlign="LEFT", colWidths=[260,120])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.25,colors.grey),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.whitesmoke, colors.lightgrey]),
        ("ALIGN",(1,1),(-1,-1),"RIGHT"),
    ]))
    story += [Paragraph("Weekly Totals (Alphabetical by Last Name; cooks included)", style_heading), t, PageBreak()]

    # Page 2: Shift Matrix (columns = shift labels)
    all_emps = sorted(set(per_shift.keys()) | set(cook_tips.keys()),
                      key=lambda s: (s.split()[-1].lower(), s.split()[0].lower()))
    matrix = [["Employee"] + shift_cols]
    for emp in all_emps:
        row = [emp] + [ ("" if per_shift.get(emp,{}).get(c,"")=="" else f"${per_shift[emp][c]:,.2f}") for c in shift_cols ]
        matrix.append(row)
    tm = Table(matrix, hAlign="LEFT", repeatRows=1)
    tm.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.25,colors.grey),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.whitesmoke, colors.lightgrey]),
        ("ALIGN",(1,1),(-1,-1),"RIGHT"),
    ]))
    story += [Paragraph("Shift Breakdown (MAM → SuPM)", style_heading), tm, PageBreak()]

    # Page 3+: Detailed math (full names already in cfg)
    for title, lines in detail:
        story.append(Paragraph(title, style_shift))
        for ln in lines:
            story.append(Paragraph(ln, style_norm))
        story.append(Spacer(1, 10))

    doc.build(story)
    os.system(f"open '{pdf_path}'")

    # ----- Excel -----
    weekly_df = pd.DataFrame(sorted(weekly.items(),
                         key=lambda x: (x[0].split()[-1].lower(), x[0].split()[0].lower())),
                         columns=["Employee","Weekly Total ($)"])
    rows = []
    for emp in all_emps:
        row = {"Employee": emp}
        for c in shift_cols:
            row[c] = per_shift.get(emp, {}).get(c, "")
        rows.append(row)
    matrix_df = pd.DataFrame(rows, columns=["Employee"]+shift_cols)
    with pd.ExcelWriter(os.path.join(report_dir, f"{out_base}.xlsx"), engine="openpyxl") as w:
        weekly_df.to_excel(w, index=False, sheet_name="Weekly Totals")
        matrix_df.to_excel(w, index=False, sheet_name="Shift Breakdown")

    csv_path = os.path.join(report_dir, f"{out_base}.csv")
    weekly_df.to_csv(csv_path, index=False)
    print(f"Built {out_base}.csv")
    # Remove legacy CSV to keep only PayrollExport CSV
    try:
        os.remove(csv_path)
        print(f"Removed legacy CSV: {csv_path}")
    except FileNotFoundError:
        pass

    # ----- PayrollExport CSV (Employee ID | Tips Owed | Employee Name) -----
    roster_path = base_dir / "PayrollExportTemplate.csv"
    if roster_path.exists():
        roster = pd.read_csv(roster_path)
        roster_map = {}
        for _, r in roster.iterrows():
            full = f"{r['First Name']} {r['Last Name']}"
            roster_map[full] = int(r["Employee ID"])
        start, end = base.split("_")
        payroll_rows = []
        for full_name, total in weekly.items():
            emp_id = roster_map.get(full_name, None)
            payroll_rows.append({
                "Employee ID": emp_id,
                "Tips Owed": total,
                "Employee Name": full_name
            })
        payroll_df = pd.DataFrame(payroll_rows)
        payroll_export_path = os.path.join(report_dir, f"{start}_{end}_PayrollExport.csv")
        payroll_df.to_csv(payroll_export_path, index=False)
        print(f"Built {start}_{end}_PayrollExport.csv")

    print(f"Built {out_base}.pdf and {out_base}.xlsx")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: build_from_json.py path/to/approve_xxxxxx_xxxxxx.approve.json"); sys.exit(2)
    main(sys.argv[1])
