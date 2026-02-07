#!/usr/bin/env python3
"""
Generate branded PDF for the Mise Onboarding Form.
"""

import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_branded_pdf import generate_pdf, LOGO_PATH

GDRIVE_LIBRARY = Path.home() / "Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Mise/docs/mise_library"

def main():
    print("=" * 50)
    print("Generating: Mise Onboarding Form")
    print("=" * 50)
    print()

    if LOGO_PATH.exists():
        print(f"Logo found: {LOGO_PATH}")
    else:
        print(f"Warning: Logo not found at {LOGO_PATH}")
    print()

    success = generate_pdf(
        "ONBOARDING_FORM_020426.md",
        "Onboarding_Form_020426.pdf",
        "Mise - New Restaurant Onboarding Form"
    )

    if success:
        pdf_path = Path(__file__).parent / "Onboarding_Form_020426.pdf"
        if GDRIVE_LIBRARY.exists():
            dest = GDRIVE_LIBRARY / "Onboarding_Form_020426.pdf"
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
