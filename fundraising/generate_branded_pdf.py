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
OUTPUT_DIR = Path.home() / "mise-core/fundraising"

def get_logo_base64():
    """Read logo and convert to base64 for embedding in HTML."""
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{logo_data}"
    return None

def get_css():
    """Return the CSS styling for the PDF."""
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

        /* Page break hints */
        h2 {{
            page-break-after: avoid;
        }}

        table, figure {{
            page-break-inside: avoid;
        }}
    """)

def markdown_to_html(md_content, title, include_logo=True):
    """Convert markdown to styled HTML."""
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc']
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

    # Generate PDF
    HTML(string=html_content).write_pdf(
        output_path,
        stylesheets=[get_css()]
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

    print("=" * 50)
    print("Done!")
    print("=" * 50)

if __name__ == "__main__":
    main()
