#!/usr/bin/env python3
"""
Read Word documents and extract Performer/Artist signature sections
"""
from docx import Document
import sys

files = [
    "/Users/jonathanflaig/Library/CloudStorage/OneDrive-Personal/Papa Surf/Live Music/Contracts/2026/Entertainment_Agreement_Alex_Napier_Band_2026.docx",
    "/Users/jonathanflaig/Library/CloudStorage/OneDrive-Personal/Papa Surf/Live Music/Contracts/2026/Entertainment_Agreement_Boukou_Groove_2026.docx",
    "/Users/jonathanflaig/Library/CloudStorage/OneDrive-Personal/Papa Surf/Live Music/Contracts/2026/Entertainment_Agreement_Killer_Robot_Army_2026_1.docx"
]

labels = [
    "Alex Napier Band (individual performer)",
    "Boukou Groove (entity: Sound Production Inc.)",
    "Killer Robot Army (entity: Scott Rockwood, LLC)"
]

for file_path, label in zip(files, labels):
    print("=" * 80)
    print(f"FILE: {label}")
    print(f"Path: {file_path}")
    print("=" * 80)

    try:
        doc = Document(file_path)

        # Find the start of the Performer/Artist signature section
        in_performer_section = False
        performer_paragraphs = []

        for para in doc.paragraphs:
            text = para.text.strip()

            # Start capturing when we find "Artist/Performer Signature:"
            if "Artist/Performer Signature:" in text or "Performer Signature:" in text or "Artist Signature:" in text:
                in_performer_section = True
                performer_paragraphs.append(para)
                continue

            # Stop when we hit "Organizer Signature:"
            if in_performer_section and "Organizer Signature:" in text:
                break

            # Capture paragraphs in the performer section
            if in_performer_section:
                performer_paragraphs.append(para)

        if performer_paragraphs:
            print("\nPERFORMER/ARTIST SIGNATURE SECTION:")
            print("-" * 80)
            for para in performer_paragraphs:
                # Show the text with visual indication of runs if needed
                print(f"{para.text}")
            print("-" * 80)
        else:
            print("\nNO PERFORMER SIGNATURE SECTION FOUND")

    except Exception as e:
        print(f"\nERROR reading file: {e}")

    print("\n")
