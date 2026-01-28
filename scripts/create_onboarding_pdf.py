#!/usr/bin/env python3
"""Generate SoWal House onboarding PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from datetime import datetime

# Output file
output_file = "/Users/jonathanflaig/mise-core/docs/onboarding/SoWal_House_Onboarding.pdf"

# Create PDF
doc = SimpleDocTemplate(output_file, pagesize=letter,
                        rightMargin=0.75*inch, leftMargin=0.75*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

# Container for PDF elements
story = []

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1B2A4E'),
    spaceAfter=12,
    alignment=TA_CENTER
)
heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#2D8A4E'),
    spaceAfter=10,
    spaceBefore=15
)
subheading_style = ParagraphStyle(
    'CustomSubHeading',
    parent=styles['Heading3'],
    fontSize=13,
    textColor=colors.HexColor('#1B2A4E'),
    spaceAfter=8,
    spaceBefore=10
)

# ===== PAGE 1: QUICK CHECKLIST =====

story.append(Paragraph("SoWal House Demo", title_style))
story.append(Paragraph("Quick Reference Checklist", styles['Heading2']))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("<b>Timmy (GM) - January 23, 2026, 11:00 AM</b>", styles['Normal']))
story.append(Spacer(1, 0.3*inch))

# Critical Info Section
story.append(Paragraph("CRITICAL INFO TO COLLECT", heading_style))

sections = [
    ("🧑‍💼 People (5 min)", [
        "☐ Server names (full): _______________________________________",
        "☐ Support staff names: _______________________________________",
        "☐ Kitchen staff (if tipped): ___________________________________"
    ]),
    ("⏰ Shifts (3 min)", [
        "☐ AM shift times: _________ to _________",
        "☐ PM shift times: _________ to _________",
        "☐ Days open: _______________________________________"
    ]),
    ("💰 Tip Rules (5 min)", [
        "☐ Pool tips? YES / NO",
        "☐ Utility tipout %: ______%",
        "☐ Tipout based on: Food sales / Total sales"
    ]),
    ("📅 Pay Period (2 min)", [
        "☐ Week starts: _____________ (day)",
        "☐ Week ends: _____________ (day)"
    ]),
    ("🎨 Branding (2 min)", [
        "☐ Logo: Can you email it? YES / NO",
        "☐ Brand colors: _______________________________________"
    ])
]

for section_title, items in sections:
    story.append(Paragraph(section_title, subheading_style))
    for item in items:
        story.append(Paragraph(item, styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
    story.append(Spacer(1, 0.1*inch))

# Demo Flow
story.append(Paragraph("DEMO FLOW", heading_style))
demo_steps = [
    "1. Show login (sowalhouse/mise2026)",
    "2. Record a test shifty (use real SoWal House names if available)",
    "3. Show approval screen with calculations",
    "4. Show weekly totals page",
    "5. <b>Highlight:</b> Time saved, accuracy, transparency"
]
for step in demo_steps:
    story.append(Paragraph(step, styles['Normal']))
    story.append(Spacer(1, 0.05*inch))

story.append(Spacer(1, 0.2*inch))

# Questions to Ask
story.append(Paragraph("QUESTIONS TO ASK", heading_style))
questions = [
    ('<b>Opening:</b> "How do you currently handle payroll each week?"<br/>→ Listen for pain points', styles['Normal']),
    ('<b>During demo:</b> "Does this match how you calculate tips?"<br/>→ Adjust if needed', styles['Normal']),
    ('<b>Closing:</b> "What would make you confident to start using this?"<br/>→ Address concerns', styles['Normal'])
]
for q in questions:
    story.append(Paragraph(q[0], q[1]))
    story.append(Spacer(1, 0.1*inch))

# Key Selling Points
story.append(Paragraph("KEY SELLING POINTS", heading_style))
selling_points = [
    "✅ <b>Saves time:</b> Payroll in minutes, not hours",
    "✅ <b>Accurate:</b> No math errors",
    "✅ <b>Transparent:</b> Staff can see calculations",
    "✅ <b>Flexible:</b> Handles your specific rules",
    "✅ <b>Easy:</b> Just speak into your phone"
]
for point in selling_points:
    story.append(Paragraph(point, styles['Normal']))
    story.append(Spacer(1, 0.05*inch))

# ===== PAGE 2: COMPREHENSIVE QUESTIONNAIRE =====

story.append(PageBreak())

story.append(Paragraph("SoWal House Onboarding", title_style))
story.append(Paragraph("Comprehensive Questionnaire", styles['Heading2']))
story.append(Spacer(1, 0.2*inch))

comprehensive_sections = [
    ("1. Employee Roster", [
        "<b>Servers:</b>",
        "☐ Who are your current servers? (Full names)",
        "☐ Any common nicknames or shortened names?",
        "",
        "<b>Support Staff:</b>",
        "☐ Who typically works utility/busser/expo roles?",
        "☐ Do they rotate or are roles dedicated?",
        "",
        "<b>Kitchen:</b>",
        "☐ Any cooks who receive tip-outs?",
        "☐ If yes, what names and what percentage/amount?"
    ]),
    ("2. Shift Configuration", [
        "<b>AM Shifts:</b>",
        "☐ What time does AM shift start and end?",
        "☐ Is it the same every day or different on weekends?",
        "",
        "<b>PM Shifts:</b>",
        "☐ What time does PM shift start and end?",
        "☐ Does it vary by day of week?",
        "☐ Daylight Saving Time or Standard Time currently?",
        "",
        "<b>Days Open:</b>",
        "☐ What days of the week are you open?",
        "☐ Any days you don't run certain shifts?"
    ]),
    ("3. Tip Pooling & Business Rules", [
        "<b>Tip Pool Policy:</b>",
        "☐ Do servers pool tips when multiple work the same shift?",
        "☐ Or does each server keep their own tips?",
        "",
        "<b>Tipout Structure:</b>",
        "☐ What percentage goes to utility staff?",
        "☐ Do you use expo + busser separately, or just 'utility'?",
        "☐ Is tipout based on food sales or total sales?",
        "",
        "<b>Special Cases:</b>",
        "☐ How do you handle when support staff leaves early?",
        "☐ Do you prorate their tipout based on hours worked?"
    ]),
    ("4. Payroll Workflow", [
        "<b>Current Process:</b>",
        "☐ How do you currently track daily payroll?",
        "☐ Who is responsible for recording tips each shift?",
        "",
        "<b>Pain Points:</b>",
        "☐ What's the most time-consuming part of payroll?",
        "☐ What errors or issues come up most often?",
        "☐ How long does it typically take to process a week?",
        "",
        "<b>Pay Period:</b>",
        "☐ What day does your pay week start?",
        "☐ What day does it end?",
        "☐ When do you typically finalize/approve payroll?"
    ]),
    ("5. Demo Preferences", [
        "<b>What to Focus On:</b>",
        "☐ What feature would be most impressive to see?",
        "☐ Time savings? Accuracy? Ease of use?",
        "",
        "<b>Concerns:</b>",
        "☐ Any concerns or hesitations about using this system?",
        "☐ What would make you confident to use it?",
        "",
        "<b>Decision Timeline:</b>",
        "☐ Looking to start using this immediately?",
        "☐ Or more of an evaluation period?"
    ])
]

for section_title, items in comprehensive_sections:
    story.append(Paragraph(section_title, heading_style))
    for item in items:
        if item == "":
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph(item, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
    story.append(Spacer(1, 0.15*inch))

# Post-Demo Action Items
story.append(PageBreak())
story.append(Paragraph("Post-Demo Action Items", heading_style))

action_items = [
    "☐ Get employee roster (full names)",
    "☐ Get logo file",
    "☐ Get brand colors (hex codes if possible)",
    "☐ Confirm shift times for AM/PM",
    "☐ Confirm tip pool policy",
    "☐ Confirm tipout percentages",
    "☐ Set up Timmy's contact info for support",
    "☐ Schedule follow-up training if needed"
]

for item in action_items:
    story.append(Paragraph(item, styles['Normal']))
    story.append(Spacer(1, 0.08*inch))

story.append(Spacer(1, 0.3*inch))

# Notes Section
story.append(Paragraph("Notes", heading_style))
story.append(Spacer(1, 0.1*inch))
for i in range(10):
    story.append(Paragraph("_" * 80, styles['Normal']))
    story.append(Spacer(1, 0.15*inch))

# Build PDF
doc.build(story)

print(f"✓ PDF created: {output_file}")
