#!/usr/bin/env python3
"""
Generate branded PDFs for Internal Mise Documents (IMDs).
Uses Inter font, Mise brand colors, and includes logo.

Usage:
    python generate_imd.py <markdown_file> <category> [--title "Custom Title"]

Example:
    python generate_imd.py md_files/IMD_Founder_Listening_Curriculum.md strategy_and_playbooks

Categories:
    investor_materials, investor_reading, mise_restricted_section,
    strategy_and_playbooks, onboarding, research, hiring, legal, parked
"""

import argparse
import markdown
import base64
import shutil
from pathlib import Path
from datetime import datetime

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Error: WeasyPrint not installed. Run: pip install weasyprint markdown")
    exit(1)

# Mise brand colors
NAVY = "#1B2A4E"
RED = "#B5402F"
CREAM = "#F9F6F1"

# Paths
SCRIPT_DIR = Path(__file__).parent
LOCAL_BASE = Path.home() / "mise-core/docs/internal_mise_docs"
GDRIVE_BASE = Path.home() / "Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/.shortcut-targets-by-id/125d9N_f2Jry6B1rLFicq8fmXsTvkShwb/Mise/Docs/mise_library"
LOGO_PATH = Path.home() / "mise-core/Branding/Logo Files/Mise Logo No BG.png"
ICON_PATH = Path.home() / "mise-core/Branding/Logo Files/Icon No Background.png"

# Category mapping (local folder name -> Google Drive folder name)
CATEGORY_MAP = {
    "investor_materials": "Investor Materials",
    "investor_reading": "Investor Reading",
    "mise_restricted_section": "Mise Restricted Section",
    "strategy_and_playbooks": "Strategy & Playbooks",
    "onboarding": "Onboarding",
    "research": "Research",
    "hiring": "Hiring",
    "legal": "Legal",
    "parked": "Parked",
}

def get_logo_base64():
    """Read logo and convert to base64 for embedding in HTML."""
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{logo_data}"
    return None

def get_icon_base64():
    """Read audiowave icon and convert to base64 for bullet points."""
    if ICON_PATH.exists():
        with open(ICON_PATH, "rb") as f:
            icon_data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{icon_data}"
    return None

def get_css(icon_base64=None):
    """Return the CSS styling for the PDF."""
    bullet_style = ""
    if icon_base64:
        bullet_style = f"""
        ul {{
            list-style: none;
            padding-left: 28px;
        }}
        ul li {{
            position: relative;
            padding-left: 4px;
        }}
        ul li::before {{
            content: '';
            position: absolute;
            left: -24px;
            top: 5px;
            width: 16px;
            height: 16px;
            background-image: url('{icon_base64}');
            background-size: contain;
            background-repeat: no-repeat;
        }}
        """

    return CSS(string=f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        @page {{
            size: letter;
            margin: 0.75in 0.75in 0.75in 0.75in;
            @bottom-center {{
                content: counter(page);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 10pt;
                color: {NAVY};
            }}
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: {NAVY};
            background-color: {CREAM};
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

        h1 {{
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 24pt;
            color: {NAVY};
            margin-top: 0;
            margin-bottom: 8px;
        }}

        h2 {{
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 16pt;
            color: {RED};
            margin-top: 24px;
            margin-bottom: 12px;
            border-bottom: 1px solid {CREAM};
            padding-bottom: 6px;
        }}

        h3 {{
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 13pt;
            color: {NAVY};
            margin-top: 18px;
            margin-bottom: 8px;
        }}

        p {{ margin-bottom: 12px; }}
        strong {{ font-weight: 600; color: {NAVY}; }}
        em {{ font-style: italic; color: {RED}; }}
        ul, ol {{ margin-bottom: 12px; padding-left: 24px; }}
        li {{ margin-bottom: 6px; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 10pt;
        }}

        th {{
            background-color: {NAVY};
            color: white;
            font-weight: 600;
            text-align: left;
            padding: 10px 12px;
            border: 1px solid {NAVY};
        }}

        td {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            vertical-align: top;
        }}

        tr:nth-child(even) {{ background-color: {CREAM}; }}

        blockquote {{
            border-left: 4px solid {RED};
            margin: 16px 0;
            padding: 12px 20px;
            background-color: {CREAM};
            font-style: italic;
        }}

        code {{
            font-family: 'SF Mono', Menlo, Monaco, monospace;
            font-size: 9pt;
            background-color: {CREAM};
            padding: 2px 6px;
            border-radius: 3px;
        }}

        hr {{
            border: none;
            border-top: 2px solid {CREAM};
            margin: 24px 0;
        }}

        a {{ color: {RED}; text-decoration: none; }}

        /* Callout boxes */
        .callout {{
            margin: 20px 0;
            padding: 16px 20px;
            border-radius: 6px;
            border-left: 4px solid;
            page-break-inside: avoid;
        }}
        .callout-title {{
            font-weight: 600;
            font-size: 11pt;
            margin-bottom: 8px;
        }}
        .callout.note {{ background-color: #E8EBF0; border-left-color: {NAVY}; }}
        .callout.tip {{ background-color: #E6F4EA; border-left-color: #2E7D32; }}
        .callout.warning {{ background-color: #FFF3E0; border-left-color: #E65100; }}
        .callout.important {{ background-color: #FDEAEA; border-left-color: {RED}; }}

        /* Pull quotes */
        .pull-quote {{
            font-size: 18pt;
            font-weight: 500;
            font-style: italic;
            color: {NAVY};
            text-align: center;
            margin: 32px 40px;
            padding: 24px 0;
            border-top: 3px solid {RED};
            border-bottom: 3px solid {RED};
        }}
        .pull-quote .attribution {{
            font-size: 11pt;
            font-weight: 400;
            font-style: normal;
            color: {RED};
            margin-top: 12px;
        }}

        /* Stat boxes */
        .stat-box {{
            display: inline-block;
            text-align: center;
            padding: 20px 30px;
            margin: 10px;
            background-color: {CREAM};
            border-radius: 8px;
        }}
        .stat-box .number {{
            font-size: 32pt;
            font-weight: 700;
            color: {RED};
        }}
        .stat-box .label {{
            font-size: 10pt;
            font-weight: 500;
            color: {NAVY};
            margin-top: 8px;
            text-transform: uppercase;
        }}
        .stats-row {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            margin: 24px 0;
        }}

        /* Timeline */
        .timeline {{
            margin: 24px 0;
            padding-left: 30px;
            border-left: 3px solid {NAVY};
        }}
        .timeline-item {{
            position: relative;
            margin-bottom: 20px;
            padding-left: 20px;
        }}
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -36px;
            top: 4px;
            width: 12px;
            height: 12px;
            background-color: {RED};
            border-radius: 50%;
        }}
        .timeline-item .date {{
            font-weight: 600;
            color: {RED};
            font-size: 10pt;
        }}

        /* Page breaks */
        h2, h3 {{ page-break-after: avoid; }}
        table, figure, .callout, .pull-quote {{ page-break-inside: avoid; }}

        {bullet_style}
    """)

def markdown_to_html(md_content, title):
    """Convert markdown to styled HTML."""
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc', 'md_in_html']
    )

    logo_html = ""
    logo_base64 = get_logo_base64()
    if logo_base64:
        logo_html = f'''
        <div class="logo-header">
            <div class="accent-line"></div>
            <img src="{logo_base64}" alt="Mise Logo">
        </div>
        '''

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
        {logo_html}
        {html_content}
    </body>
    </html>
    """

def generate_imd(md_file: Path, category: str, title: str = None):
    """
    Generate an IMD from a markdown file.

    Creates 4 files:
    1. .md in md_files/ (already exists)
    2. .pdf in local category folder
    3. .pdf in Google Drive extra! extra!/
    4. .pdf in Google Drive category folder
    """
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False

    if category not in CATEGORY_MAP:
        print(f"Error: Unknown category '{category}'")
        print(f"Valid categories: {', '.join(CATEGORY_MAP.keys())}")
        return False

    # Read markdown
    print(f"Reading {md_file.name}...")
    md_content = md_file.read_text()

    # Derive title from first H1 if not provided
    if not title:
        for line in md_content.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                break
        if not title:
            title = md_file.stem.replace('_', ' ')

    # Generate PDF filename
    pdf_name = md_file.stem.replace('IMD_', '') + '.pdf'

    print(f"Title: {title}")
    print(f"Category: {category} -> {CATEGORY_MAP[category]}")
    print()

    # Convert to HTML
    print("Converting to HTML...")
    html_content = markdown_to_html(md_content, title)
    icon_base64 = get_icon_base64()

    # Define output paths
    local_category_dir = LOCAL_BASE / category
    gdrive_extra_dir = GDRIVE_BASE / "extra! extra!"
    gdrive_category_dir = GDRIVE_BASE / CATEGORY_MAP[category]

    # Ensure directories exist
    local_category_dir.mkdir(parents=True, exist_ok=True)

    # Generate PDF
    print("Generating PDF...")
    local_pdf_path = local_category_dir / pdf_name

    HTML(string=html_content).write_pdf(
        local_pdf_path,
        stylesheets=[get_css(icon_base64)]
    )
    print(f"  ✓ Local PDF: {local_pdf_path}")

    # Copy to Google Drive locations
    files_created = [str(local_pdf_path)]

    if gdrive_extra_dir.exists():
        gdrive_extra_path = gdrive_extra_dir / pdf_name
        shutil.copy(local_pdf_path, gdrive_extra_path)
        print(f"  ✓ Google Drive (extra! extra!): {gdrive_extra_path}")
        files_created.append(str(gdrive_extra_path))
    else:
        print(f"  ⚠ Google Drive extra! extra! not found: {gdrive_extra_dir}")

    if gdrive_category_dir.exists():
        gdrive_category_path = gdrive_category_dir / pdf_name
        shutil.copy(local_pdf_path, gdrive_category_path)
        print(f"  ✓ Google Drive ({CATEGORY_MAP[category]}): {gdrive_category_path}")
        files_created.append(str(gdrive_category_path))
    else:
        print(f"  ⚠ Google Drive category folder not found: {gdrive_category_dir}")

    print()
    print(f"Created {len(files_created)} files:")
    for f in files_created:
        print(f"  - {f}")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Generate branded PDFs for Internal Mise Documents (IMDs)"
    )
    parser.add_argument("markdown_file", help="Path to markdown file")
    parser.add_argument("category", choices=CATEGORY_MAP.keys(),
                        help="Document category")
    parser.add_argument("--title", "-t", help="Custom document title")

    args = parser.parse_args()

    md_file = Path(args.markdown_file)
    if not md_file.is_absolute():
        md_file = SCRIPT_DIR / md_file

    print("=" * 60)
    print("Generating Internal Mise Document (IMD)")
    print("=" * 60)
    print()

    success = generate_imd(md_file, args.category, args.title)

    print()
    if success:
        print("Done!")
    else:
        print("Failed.")
        exit(1)

if __name__ == "__main__":
    main()
