#!/usr/bin/env python3
"""
Generate branded PDFs for Mise fundraising documents.
Uses Inter font, Mise brand colors, and includes logo.
"""

import markdown
import base64
from pathlib import Path
from weasyprint import HTML, CSS

# Mise brand colors
NAVY = "#1B2A4E"
RED = "#B5402F"
CREAM = "#F9F6F1"

# Paths
SCRIPT_DIR = Path(__file__).parent
LOGO_PATH = Path.home() / "mise-core/Branding/Logo Files/Updated Mise Logo Pronunciation.png"
ICON_PATH = Path.home() / "mise-core/Branding/Logo Files/Icon No Background.png"
OUTPUT_DIR = Path.home() / "mise-core/fundraising"

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
    # Bullet point style - use audiowave icon if available
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
            top: 2px;
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
            background-color: white;
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
            border-bottom: none;
            padding-bottom: 0;
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

        p {{
            margin-bottom: 12px;
        }}

        strong {{
            font-weight: 600;
            color: {NAVY};
        }}

        em {{
            font-style: italic;
            color: {RED};
        }}

        ul, ol {{
            margin-bottom: 12px;
            padding-left: 24px;
        }}

        li {{
            margin-bottom: 6px;
        }}

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

        tr:nth-child(even) {{
            background-color: {CREAM};
        }}

        tr:hover {{
            background-color: #f0ebe3;
        }}

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

        a {{
            color: {RED};
            text-decoration: none;
        }}

        .contact-section {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid {RED};
            text-align: center;
        }}

        /* ========== CALLOUT BOXES ========== */
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
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .callout.note {{
            background-color: #E8EBF0;
            border-left-color: {NAVY};
        }}
        .callout.note .callout-title {{
            color: {NAVY};
        }}

        .callout.tip {{
            background-color: #E6F4EA;
            border-left-color: #2E7D32;
        }}
        .callout.tip .callout-title {{
            color: #2E7D32;
        }}

        .callout.warning {{
            background-color: #FFF3E0;
            border-left-color: #E65100;
        }}
        .callout.warning .callout-title {{
            color: #E65100;
        }}

        .callout.important {{
            background-color: #FDEAEA;
            border-left-color: {RED};
        }}
        .callout.important .callout-title {{
            color: {RED};
        }}

        /* ========== PULL QUOTES ========== */
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
            line-height: 1.4;
            page-break-inside: avoid;
        }}

        .pull-quote .attribution {{
            font-size: 11pt;
            font-weight: 400;
            font-style: normal;
            color: {RED};
            margin-top: 12px;
        }}

        /* ========== KEY STATS / METRICS ========== */
        .stat-box {{
            display: inline-block;
            text-align: center;
            padding: 20px 30px;
            margin: 10px;
            background-color: {CREAM};
            border-radius: 8px;
            page-break-inside: avoid;
        }}

        .stat-box .number {{
            font-size: 32pt;
            font-weight: 700;
            color: {RED};
            line-height: 1;
        }}

        .stat-box .label {{
            font-size: 10pt;
            font-weight: 500;
            color: {NAVY};
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .stats-row {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            margin: 24px 0;
        }}

        /* ========== DIAGRAMS / FIGURES ========== */
        figure {{
            margin: 24px 0;
            text-align: center;
            page-break-inside: avoid;
        }}

        figure img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}

        figcaption {{
            font-size: 10pt;
            font-style: italic;
            color: #666;
            margin-top: 8px;
        }}

        /* ASCII diagram styling */
        .diagram {{
            font-family: 'SF Mono', Menlo, Monaco, monospace;
            font-size: 9pt;
            background-color: {CREAM};
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
            white-space: pre;
            line-height: 1.3;
            margin: 20px 0;
            page-break-inside: avoid;
        }}

        /* ========== ICON HELPERS ========== */
        .icon {{
            display: inline-block;
            width: 20px;
            text-align: center;
        }}

        .check {{ color: #2E7D32; }}
        .cross {{ color: {RED}; }}
        .arrow {{ color: {NAVY}; }}
        .star {{ color: #F9A825; }}

        /* ========== COMPARISON TABLE ========== */
        .comparison td:first-child {{
            font-weight: 600;
            background-color: {CREAM};
        }}

        .comparison .yes {{
            color: #2E7D32;
            font-weight: 600;
        }}

        .comparison .no {{
            color: {RED};
            font-weight: 600;
        }}

        /* ========== TIMELINE ========== */
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
            border: 2px solid white;
        }}

        .timeline-item .date {{
            font-weight: 600;
            color: {RED};
            font-size: 10pt;
        }}

        .timeline-item .event {{
            color: {NAVY};
        }}

        /* Page break hints */
        h2 {{
            page-break-after: avoid;
        }}

        table, figure, .callout, .pull-quote, .stat-box, .diagram {{
            page-break-inside: avoid;
        }}

        {bullet_style}
    """)

def markdown_to_html(md_content, title, include_logo=True):
    """Convert markdown to styled HTML."""
    # Convert markdown to HTML (md_in_html allows HTML blocks with markdown inside)
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc', 'md_in_html']
    )

    # Build logo header
    logo_html = ""
    if include_logo:
        logo_base64 = get_logo_base64()
        if logo_base64:
            logo_html = f'''
            <div class="logo-header">
                <div class="accent-line"></div>
                <img src="{logo_base64}" alt="Mise Logo">
            </div>
            '''

    # Full HTML document
    full_html = f"""
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

    return full_html

def generate_pdf(md_file, output_name, title):
    """Generate a PDF from a markdown file."""
    md_path = SCRIPT_DIR / md_file

    if not md_path.exists():
        print(f"Error: {md_path} not found")
        return False

    print(f"Reading {md_file}...")
    with open(md_path, 'r') as f:
        md_content = f.read()

    print("Converting to HTML...")
    html_content = markdown_to_html(md_content, title)

    print("Generating PDF...")
    output_path = OUTPUT_DIR / output_name

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Get audiowave icon for bullet points
    icon_base64 = get_icon_base64()

    # Generate PDF
    HTML(string=html_content).write_pdf(
        output_path,
        stylesheets=[get_css(icon_base64)]
    )

    print(f"Saved to: {output_path}")
    return True

def main():
    """Generate all fundraising PDFs."""
    print("=" * 50)
    print("Generating Mise Fundraising PDFs")
    print("=" * 50)
    print()

    # Check logo exists
    if LOGO_PATH.exists():
        print(f"Logo found: {LOGO_PATH}")
    else:
        print(f"Warning: Logo not found at {LOGO_PATH}")
    print()

    # Generate Executive Summary PDF
    print("-" * 50)
    generate_pdf(
        "EXECUTIVE_SUMMARY.md",
        "Mise_Executive_Summary.pdf",
        "Mise - Executive Summary"
    )
    print()

    # Generate Tuesday Meeting Prep PDF
    print("-" * 50)
    generate_pdf(
        "TUESDAY_MEETING_PREP.md",
        "Tuesday_Meeting_Prep.pdf",
        "Tuesday Meeting Prep"
    )
    print()

    # Generate NDA PDF
    print("-" * 50)
    generate_pdf(
        "Mise_NDA.md",
        "Mise_NDA.pdf",
        "Mise - Non-Disclosure Agreement"
    )
    print()

    # Generate CoCounsel Improvements Guide PDF
    print("-" * 50)
    generate_pdf(
        "CoCounsel_Improvements_Guide.md",
        "CoCounsel_Improvements_Guide.pdf",
        "CoCounsel-Inspired Improvements to Mise"
    )
    print()

    # Generate Trillion Dollar AI Buildout PDF
    print("-" * 50)
    generate_pdf(
        "TRILLION_DOLLAR_AI_BUILDOUT.md",
        "Trillion_Dollar_AI_Buildout.pdf",
        "Inside the Trillion-Dollar AI Buildout"
    )
    print()

    print("=" * 50)
    print("Done!")
    print("=" * 50)

if __name__ == "__main__":
    main()
