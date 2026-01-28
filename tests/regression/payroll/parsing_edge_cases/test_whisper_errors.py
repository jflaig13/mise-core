"""
Regression Test: Whisper Errors / ASR Mistakes

CATEGORY: Parsing Edge Cases / Robustness
PRIORITY: High - Real-world voice input is messy

PURPOSE:
Test that Mise handles speech recognition errors gracefully.

COMMON WHISPER ERRORS:
- Name mishearings: "Austin" → "Lost him", "Allston", "Awesome"
- Number mishearings: "Seventeen" → "70", "$50" → "Fifty"
- Punctuation errors: "Austin $16.80 mic $16.86" (mic = Mike)
- Filler words: "um", "uh", "so", "okay"
- Background noise: partial words, cutoffs
- Accent/pronunciation: regional variants, fast speech

EXPECTED BEHAVIOR:
- Normalize common mishearings (use roster mapping)
- Parse amounts despite punctuation errors
- Ignore filler words gracefully
- Request clarification for ambiguous errors
"""

import pytest


def test_austin_to_lost_him_variant():
    """
    Test Whisper misheard "Austin" as "lost him" → maps to Austin Kelley.

    ACTUAL PRODUCTION ERROR (from test_parser_support_staff.py:122):
    Transcript: "Kevin $364.30 lost him $364.30 Ryan $130.94"
    Expected: "lost him" → "Austin Kelley"
    """
    transcript = "November 28 2025 AM shift Kevin $364.30 lost him $364.30 Ryan $130.94"

    # result = parse_transcript(transcript)

    # assert "Austin Kelley" in result["employees"]
    # assert result["employees"]["Austin Kelley"]["amount"] == 364.30
    # assert result["employees"]["Austin Kelley"]["name_source"] == "roster_variant: lost him"

    pytest.skip("Name variant mapping pending")


def test_austin_to_allston_variant():
    """
    Test Whisper misheard "Austin" as "Allston" (from test_parser_support_staff.py:154).

    Transcript: "Allston $49.33, Fiona $10.04."
    Expected: "Allston" → "Austin Kelley"
    """
    transcript = "December 5th 2025 PM shift, Allston $49.33, Fiona $10.04."

    # result = parse_transcript(transcript)

    # assert "Austin Kelley" in result["employees"]
    # assert result["employees"]["Austin Kelley"]["amount"] == 49.33

    pytest.skip("Name variant mapping pending")


def test_punctuation_in_dollar_amounts():
    """
    Test parsing dollar amounts with punctuation errors.

    ACTUAL PRODUCTION ERROR (from test_parser_support_staff.py:56):
    Transcript: "Kevin $16.80 mic $16.86. Ryan $7.35."
    "mic" should be "Mike" (Mike Walton)
    """
    transcript = "Kevin $16.80 mic $16.86. Ryan $7.35."

    # result = parse_transcript(transcript)

    # Should handle:
    # 1. "mic" → "Mike Walton" (name variant)
    # 2. Trailing periods after amounts
    # assert "Kevin Worley" in result["employees"]
    # assert result["employees"]["Kevin Worley"]["amount"] == 16.80
    # assert "Mike Walton" in result["employees"]
    # assert result["employees"]["Mike Walton"]["amount"] == 16.86
    # assert "Ryan Alexander" in result["employees"]
    # assert result["employees"]["Ryan Alexander"]["amount"] == 7.35

    pytest.skip("Punctuation handling pending")


def test_full_phrase_amounts():
    """
    Test parsing amounts spoken as full phrases.

    ACTUAL PRODUCTION ERROR (from test_parser_support_staff.py:73):
    Transcript: "Kevin 111 dollars and 12 cents"
    Expected: 111.12 (not 111.00 or truncated)
    """
    transcript = "Sunday, November 30th 2025 AM shift Kevin 111 dollars and 12 cents Mike 111 dollars and 12 cents Ryan 34 dollars and 72 cents"

    # result = parse_transcript(transcript)

    # Must NOT truncate "and 12 cents" part
    # assert result["employees"]["Kevin Worley"]["amount"] == 111.12
    # assert result["employees"]["Mike Walton"]["amount"] == 111.12
    # assert result["employees"]["Ryan Alexander"]["amount"] == 34.72

    pytest.skip("Full phrase amount parsing pending")


def test_trailing_dot_whole_dollars():
    """
    Test that trailing dots parse as whole dollars, not errors.

    ACTUAL PRODUCTION ERROR (from test_parser_support_staff.py:90):
    Transcript: "Austin $120."
    Expected: 120.00 (not 120.0 or error)
    """
    transcript = "December 4th 2025, PM shift, Austin $120."

    # result = parse_transcript(transcript)

    # assert result["employees"]["Austin Kelley"]["amount"] == 120.00

    pytest.skip("Trailing dot handling pending")


def test_filler_words_ignored():
    """
    Test that filler words don't break parsing.

    Transcript with filler: "Okay so um Austin like $150 and uh Brooke $140"
    Expected: Parse amounts correctly, ignore fillers
    """
    transcript = "Monday AM okay so um Austin like $150 and uh Brooke $140 alright"

    # result = parse_transcript(transcript)

    # Filler words should be ignored
    # assert result["employees"]["Austin Kelley"]["amount"] == 150.00
    # assert result["employees"]["Brooke Neal"]["amount"] == 140.00

    pytest.skip("Filler word filtering pending")


def test_background_noise_partial_words():
    """
    Test handling of partial words / cutoffs from background noise.

    Transcript: "Austin [inaudible] $150 Bro- Brooke $140"
    Expected: Handle partial "Bro-" → "Brooke"
    """
    transcript = "Austin mmm $150 Bro- Brooke $140"

    # result = parse_transcript(transcript)

    # Should recognize "Brooke" despite partial start
    # assert "Brooke Neal" in result["employees"]
    # assert result["employees"]["Brooke Neal"]["amount"] == 140.00

    pytest.skip("Partial word handling pending")


def test_number_spacing_variants():
    """
    Test different ways numbers might be spaced/separated.

    Examples:
    - "12345" (no space) → $123.45
    - "123 45" (space) → $123.45
    - "123.45" (decimal) → $123.45
    - "123 point 45" (spoken) → $123.45
    """
    transcripts = [
        "Austin 12345",       # No space
        "Austin 123 45",      # Space
        "Austin 123.45",      # Decimal
        "Austin 123 point 45" # Spoken
    ]

    # for transcript in transcripts:
    #     result = parse_transcript(transcript)
    #     assert result["employees"]["Austin Kelley"]["amount"] == 123.45

    pytest.skip("Number format normalization pending")


def test_name_pronunciation_variants():
    """
    Test common pronunciation variants for employee names.

    ACTUAL PRODUCTION ERRORS:
    - "Atticus usseglo" → "Atticus Usseglio" (test_parser_support_staff.py:139)
    - "Fiona" spoken clearly (common enough)
    """
    transcripts = {
        "Atticus usseglo 85 25": ("Atticus Usseglio", 85.25),
        "Fiona 75 04": ("Fiona Dodson", 75.04),
    }

    # for transcript, (expected_name, expected_amount) in transcripts.items():
    #     result = parse_transcript(transcript)
    #     assert expected_name in result["employees"]
    #     assert result["employees"][expected_name]["amount"] == expected_amount

    pytest.skip("Name pronunciation mapping pending")


def test_manager_self_correction():
    """
    Test handling manager correcting themselves mid-sentence.

    Transcript: "Austin $150 no wait make that $160"
    Expected: Final amount is $160, not $150
    """
    transcript = "Monday AM Austin $150 no wait make that $160 Brooke $140"

    # result = parse_transcript(transcript)

    # Should use corrected amount
    # assert result["employees"]["Austin Kelley"]["amount"] == 160.00
    # Should flag correction for review
    # assert result["employees"]["Austin Kelley"]["has_correction"] == True

    pytest.skip("Self-correction handling pending")


def test_ambiguous_error_requests_clarification():
    """
    Test that truly ambiguous errors request clarification.

    Transcript: "Austin [garbled] Brooke $140"
    If amount is unintelligible, ask rather than guess.
    """
    transcript = "Austin inaudible Brooke $140"

    # result = parse_transcript(transcript)

    # Should request clarification for Austin's amount
    # assert "Austin Kelley" in result["needs_clarification"]
    # assert result["needs_clarification"]["Austin Kelley"] == "amount_missing"

    pytest.skip("Ambiguous error clarification pending")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
