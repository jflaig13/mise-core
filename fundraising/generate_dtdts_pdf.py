#!/usr/bin/env python3
"""
Generate branded PDF for 'Do Things That Don't Scale' IMD.
Uses the standard IMD branding from generate_branded_pdf.py.
"""

import sys
from pathlib import Path

# Import from the shared generator
sys.path.insert(0, str(Path(__file__).parent))
from generate_branded_pdf import generate_pdf, LOGO_PATH

GDRIVE_LIBRARY = Path.home() / "Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Mise/docs/mise_library"

def main():
    print("=" * 50)
    print("Generating: Do Things That Don't Scale - IMD")
    print("=" * 50)
    print()

    if LOGO_PATH.exists():
        print(f"Logo found: {LOGO_PATH}")
    else:
        print(f"Warning: Logo not found at {LOGO_PATH}")
    print()

    success = generate_pdf(
        "DO_THINGS_THAT_DONT_SCALE.md",
        "Do_Things_That_Dont_Scale.pdf",
        "Do Things That Don't Scale - Applied to Mise"
    )

    if success:
        # Copy to Google Drive mise_library
        pdf_path = Path(__file__).parent / "Do_Things_That_Dont_Scale.pdf"
        if GDRIVE_LIBRARY.exists():
            import shutil
            dest = GDRIVE_LIBRARY / "Do_Things_That_Dont_Scale.pdf"
            shutil.copy2(pdf_path, dest)
            print(f"Copied to Google Drive: {dest}")
        else:
            print(f"Google Drive path not found: {GDRIVE_LIBRARY}")
            print("PDF saved locally only.")

    print()
    print("=" * 50)
    print("Done!")
    print("=" * 50)

if __name__ == "__main__":
    main()
