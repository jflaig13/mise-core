#!/usr/bin/env python3
"""
Generate clean, professional legal PDFs.
White background, black text, no branding - just professional legal formatting.

Usage:
    python generate_legal_pdf.py <markdown_file> [--output <path>]

Example:
    python generate_legal_pdf.py Initial_Board_Resolutions_TEMPLATE.md
"""

import argparse
import markdown
from pathlib import Path

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Error: WeasyPrint not installed. Run: pip install weasyprint markdown")
    exit(1)

SCRIPT_DIR = Path(__file__).parent

def get_legal_css():
    """Clean, professional legal document styling."""
    return CSS(string="""
        @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');

        @page {
            size: letter;
            margin: 1in;
            @bottom-center {
                content: counter(page);
                font-family: 'Times New Roman', Times, Georgia, serif;
                font-size: 10pt;
                color: #000;
            }
        }

        body {
            font-family: 'Times New Roman', Times, Georgia, serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #000;
            background-color: #fff;
        }

        h1 {
            font-size: 16pt;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
            margin-top: 0;
            margin-bottom: 24px;
            color: #000;
        }

        h2 {
            font-size: 12pt;
            font-weight: bold;
            text-transform: uppercase;
            margin-top: 24px;
            margin-bottom: 12px;
            color: #000;
        }

        h3 {
            font-size: 11pt;
            font-weight: bold;
            margin-top: 18px;
            margin-bottom: 8px;
            color: #000;
        }

        p {
            margin-bottom: 12px;
            text-align: justify;
        }

        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        ul, ol {
            margin-bottom: 12px;
            padding-left: 36px;
        }

        li {
            margin-bottom: 6px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 10pt;
        }

        th {
            background-color: #f5f5f5;
            font-weight: bold;
            text-align: left;
            padding: 8px 12px;
            border: 1px solid #000;
        }

        td {
            padding: 8px 12px;
            border: 1px solid #000;
            vertical-align: top;
        }

        blockquote {
            margin: 16px 0;
            padding-left: 24px;
            border-left: none;
            font-style: normal;
        }

        hr {
            border: none;
            border-top: 1px solid #000;
            margin: 24px 0;
        }

        code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 10pt;
        }

        a {
            color: #000;
            text-decoration: underline;
        }

        /* Signature blocks */
        .signature-block {
            margin-top: 36px;
            page-break-inside: avoid;
        }

        /* Document header styling */
        .doc-header {
            text-align: center;
            margin-bottom: 24px;
        }

        /* Party blocks */
        .party-block {
            margin: 16px 0;
            padding-left: 24px;
        }

        /* Address blocks */
        .address-block {
            margin: 12px 0;
            padding-left: 24px;
        }

        /* Contact blocks */
        .contact-block {
            margin: 16px 0;
        }

        /* Footer notice */
        .footer-notice {
            margin-top: 36px;
            text-align: center;
            font-style: italic;
            font-size: 10pt;
        }

        /* Info categories for privacy policy */
        .info-category {
            margin: 12px 0;
        }

        /* Highlight boxes - make them subtle */
        .highlight-box {
            margin: 16px 0;
            padding: 12px;
            border: 1px solid #ccc;
            background-color: #fafafa;
        }

        /* Page breaks */
        h1, h2 {
            page-break-after: avoid;
        }

        table, .signature-block {
            page-break-inside: avoid;
        }
    """)


def markdown_to_html(md_content, title):
    """Convert markdown to clean HTML."""
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'md_in_html']
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """


def generate_legal_pdf(md_file: Path, output_path: Path = None):
    """Generate a clean legal PDF from markdown."""
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False

    # Read markdown
    print(f"Reading {md_file.name}...")
    md_content = md_file.read_text()

    # Derive title from first H1
    title = md_file.stem.replace('_', ' ')
    for line in md_content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break

    # Default output path
    if output_path is None:
        output_path = md_file.with_suffix('.pdf')

    print(f"Title: {title}")
    print(f"Output: {output_path}")

    # Convert to HTML
    html_content = markdown_to_html(md_content, title)

    # Generate PDF
    print("Generating PDF...")
    HTML(string=html_content).write_pdf(
        output_path,
        stylesheets=[get_legal_css()]
    )

    print(f"✓ Created: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate clean, professional legal PDFs"
    )
    parser.add_argument("markdown_file", help="Path to markdown file")
    parser.add_argument("--output", "-o", help="Output PDF path")

    args = parser.parse_args()

    md_file = Path(args.markdown_file)
    if not md_file.is_absolute():
        md_file = SCRIPT_DIR / md_file

    output_path = Path(args.output) if args.output else None

    generate_legal_pdf(md_file, output_path)


if __name__ == "__main__":
    main()
