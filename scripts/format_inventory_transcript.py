"""
Heuristically format a raw inventory transcript into one-item-per-line output.

Usage:
    python scripts/format_inventory_transcript.py input.txt output.txt

Approach:
- Split on sentence-ish boundaries (periods, commas, and newlines).
- Start a new line when a segment begins with a quantity pattern (e.g., "two bottles", "14 bottles", "3 cases").
- Preserve order; join the cleaned segments into lines.

This is a lightweight heuristic; it will not be perfect but should make item starts clearer.
"""

import re
import sys
from pathlib import Path

QUANTITY_START = re.compile(
    r"^\s*(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b",
    re.IGNORECASE,
)


def normalize_segments(text: str):
    # Replace newlines with commas to treat them as soft separators
    text = text.replace("\n", ", ")
    # Split on commas and periods
    raw_segments = re.split(r"[.,]", text)
    return [seg.strip() for seg in raw_segments if seg.strip()]


def format_transcript(text: str):
    segments = normalize_segments(text)
    lines = []
    current = []
    for seg in segments:
        if QUANTITY_START.match(seg) and current:
            lines.append(" ".join(current).strip())
            current = [seg]
        else:
            current.append(seg)
    if current:
        lines.append(" ".join(current).strip())
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/format_inventory_transcript.py input.txt [output.txt]")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    text = in_path.read_text(encoding="utf-8")
    formatted = format_transcript(text)

    if out_path:
        out_path.write_text(formatted, encoding="utf-8")
        print(f"Wrote formatted transcript to {out_path}")
    else:
        print(formatted)


if __name__ == "__main__":
    main()
