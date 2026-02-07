#!/usr/bin/env python3
"""
Clean up old IMDs from 'extra! extra!' after 31 days.

Run manually or set up as a cron job:
    crontab -e
    0 9 * * * /usr/bin/python3 ~/mise-core/scripts/archive_imds.py

This script:
1. Checks each file in 'extra! extra!' folder
2. If file is 31+ days old, DELETES it (category folder already has permanent copy)
3. Handles versioned files (_v2, _v2.1, _v3, etc.)

NOTE: When IMDs are created, they're saved to BOTH 'extra! extra!' (temporary)
AND the appropriate category folder (permanent). This script only cleans up
the temporary copies after 30 days.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
MISE_LIBRARY = Path.home() / "Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Mise/docs/mise_library"
EXTRA_FOLDER = MISE_LIBRARY / "extra! extra!"
AGE_THRESHOLD_DAYS = 31

# Category mapping: filename pattern -> category folder
# Add new IMDs here as they're created
CATEGORY_MAP = {
    # Investor Materials
    "Mise_Pitch_Deck": "Investor Materials",
    "Family_Investment_Ask": "Investor Materials",
    "Mise_Moat_Memo": "Investor Materials",
    "Mise_AGI_Defensibility": "Investor Materials",
    "Executive_Summary": "Investor Materials",

    # Strategy & Playbooks
    "AGI_Playbook": "Strategy & Playbooks",
    "YC_Startup_School": "Strategy & Playbooks",
    "Do_Things_That_Dont_Scale": "Strategy & Playbooks",
    "CoCounsel": "Strategy & Playbooks",

    # Onboarding
    "Austin_Onboarding": "Onboarding",
    "Onboarding_Form": "Onboarding",

    # Research
    "Trillion_Dollar": "Research",

    # Investor Reading (curated content for investors)
    "Reading": "Investor Reading",

    # Hiring
    "Senior_Engineer": "Hiring",
    "Job_Posting": "Hiring",
    "Contractor": "Hiring",

    # Parked (ideas on hold)
    "Human_Fund": "Parked",

    # Legal
    "NDA": "Legal",
    "Mise_NDA": "Legal",
}

# Default category for unmapped files
DEFAULT_CATEGORY = "Strategy & Playbooks"

# Regex pattern to match version suffixes (_v2, _v2.1, _v3.2, etc.)
VERSION_PATTERN = re.compile(r'_v\d+(\.\d+)?(?=\.pdf$)', re.IGNORECASE)


def strip_version_suffix(filename: str) -> str:
    """Remove version suffix from filename for category matching."""
    return VERSION_PATTERN.sub('', filename)


def get_version(filename: str) -> str:
    """Extract version from filename, or return empty string if none."""
    match = VERSION_PATTERN.search(filename)
    return match.group(0) if match else ""


def get_file_age_days(filepath: Path) -> int:
    """Get the age of a file in days based on modification time."""
    mtime = filepath.stat().st_mtime
    file_date = datetime.fromtimestamp(mtime)
    age = datetime.now() - file_date
    return age.days


def get_category(filename: str) -> str:
    """Determine category based on filename patterns (ignoring version suffix)."""
    # Strip version suffix before matching
    base_filename = strip_version_suffix(filename)
    for pattern, category in CATEGORY_MAP.items():
        if pattern.lower() in base_filename.lower():
            return category
    return DEFAULT_CATEGORY


def cleanup_old_imds(dry_run: bool = False):
    """Delete IMDs older than threshold from extra! extra! (category folder has permanent copy)."""
    if not EXTRA_FOLDER.exists():
        print(f"Error: {EXTRA_FOLDER} does not exist")
        return

    deleted_count = 0
    skipped_count = 0

    for filepath in EXTRA_FOLDER.glob("*.pdf"):
        age_days = get_file_age_days(filepath)

        if age_days >= AGE_THRESHOLD_DAYS:
            category = get_category(filepath.name)

            if dry_run:
                print(f"[DRY RUN] Would delete: {filepath.name}")
                print(f"           Age: {age_days} days")
                print(f"           Permanent copy in: {category}/")
                print()
            else:
                # Delete the file (permanent copy exists in category folder)
                filepath.unlink()
                print(f"Deleted: {filepath.name} (permanent copy in {category}/)")

            deleted_count += 1
        else:
            skipped_count += 1
            if dry_run:
                print(f"[SKIP] {filepath.name} ({age_days} days old, threshold: {AGE_THRESHOLD_DAYS})")

    print()
    print(f"Summary: {deleted_count} deleted, {skipped_count} kept (< {AGE_THRESHOLD_DAYS} days)")


def list_current_status():
    """Show current state of all IMDs with their ages and categories."""
    print("=" * 60)
    print("IMD Library Status")
    print("=" * 60)
    print()

    # Show extra! extra! contents
    print(f"📰 extra! extra! (docs ≤30 days)")
    print("-" * 40)
    if EXTRA_FOLDER.exists():
        for filepath in sorted(EXTRA_FOLDER.glob("*.pdf")):
            age_days = get_file_age_days(filepath)
            category = get_category(filepath.name)
            version = get_version(filepath.name)
            version_str = f" [{version}]" if version else ""
            status = "🔴 READY TO ARCHIVE" if age_days >= AGE_THRESHOLD_DAYS else f"⏳ {AGE_THRESHOLD_DAYS - age_days} days left"
            print(f"  {filepath.name}{version_str}")
            print(f"    Age: {age_days} days | Category: {category} | {status}")
    print()

    # Show category folders
    for category in ["Investor Materials", "Investor Reading", "Strategy & Playbooks", "Onboarding", "Research", "Hiring", "Legal", "Parked"]:
        folder = MISE_LIBRARY / category
        if folder.exists():
            files = list(folder.glob("*.pdf"))
            if files:
                print(f"📁 {category}")
                print("-" * 40)
                for filepath in sorted(files):
                    age_days = get_file_age_days(filepath)
                    version = get_version(filepath.name)
                    version_str = f" [{version}]" if version else ""
                    print(f"  {filepath.name}{version_str} ({age_days} days old)")
                print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--dry-run":
            print("DRY RUN MODE - No files will be deleted")
            print("=" * 50)
            cleanup_old_imds(dry_run=True)
        elif sys.argv[1] == "--status":
            list_current_status()
        elif sys.argv[1] == "--help":
            print("Usage: python archive_imds.py [--dry-run|--status|--help]")
            print()
            print("  --dry-run  Show what would be deleted without deleting")
            print("  --status   Show current state of all IMDs")
            print("  --help     Show this help message")
            print()
            print("Run without arguments to delete files older than 31 days from extra! extra!")
            print("(Permanent copies exist in category folders)")
    else:
        cleanup_old_imds(dry_run=False)
