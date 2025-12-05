import importlib
from unittest import mock


def test_support_staff_are_recognized_and_categorized():
    """
    Ensure support staff names are normalized and tagged with support category.
    """

    with mock.patch("google.cloud.bigquery.Client") as client_mock:
        client_mock.return_value = mock.Mock()
        engine = importlib.reload(importlib.import_module("engine.payroll_engine"))

    payload = engine.TranscriptIn(
        filename="010125_AM.wav",
        transcript="Ryan Alexander 123 45",
    )

    rows = engine.parse_transcript_to_rows(payload)

    assert engine.SUPPORT_STAFF == {"Ryan Alexander", "Coben Cross", "Maddox Porter"}
    assert len(rows) == 1
    row = rows[0]
    assert row.employee == "Ryan Alexander"
    assert row.category == "support"
    assert abs(row.amount_final - 123.45) < 1e-6


def test_full_phrase_amounts_are_not_truncated():
    with mock.patch("google.cloud.bigquery.Client") as client_mock:
        client_mock.return_value = mock.Mock()
        engine = importlib.reload(importlib.import_module("engine.payroll_engine"))

    payload = engine.TranscriptIn(
        filename="113025_AM.wav",
        transcript="Sunday, November 30th 2025 AM shift Kevin 111 dollars and 12 cents Mike 111 dollars and 12 cents Ryan 34 dollars and 72 cents",
    )

    rows = engine.parse_transcript_to_rows(payload)

    amounts = {r.employee: (r.amount_final, r.role, r.category) for r in rows}
    assert amounts["Kevin Worley"][0] == 111.12
    assert amounts["Kevin Worley"][1] == "FOH"
    assert amounts["Mike Walton"][0] == 111.12
    assert amounts["Ryan Alexander"][0] == 34.72
    assert amounts["Ryan Alexander"][1] == "utility"
    assert amounts["Ryan Alexander"][2] == "support"


def test_dollar_tokens_with_punctuation_are_parsed():
    with mock.patch("google.cloud.bigquery.Client") as client_mock:
        client_mock.return_value = mock.Mock()
        engine = importlib.reload(importlib.import_module("engine.payroll_engine"))

    payload = engine.TranscriptIn(
        filename="113025_PM.wav",
        transcript="Kevin $16.80 mic $16.86. Ryan $7.35.",
    )

    rows = engine.parse_transcript_to_rows(payload)
    amounts = {r.employee: r.amount_final for r in rows}
    assert amounts["Kevin Worley"] == 16.80
    assert amounts["Mike Walton"] == 16.86
    assert amounts["Ryan Alexander"] == 7.35


def test_full_phrase_amounts_with_dollars_and_cents_are_kept():
    with mock.patch("google.cloud.bigquery.Client") as client_mock:
        client_mock.return_value = mock.Mock()
        engine = importlib.reload(importlib.import_module("engine.payroll_engine"))

    payload = engine.TranscriptIn(
        filename="113025_AM.wav",
        transcript="Sunday, November 30th 2025 AM shift Kevin 111 dollars and 12 cents Mike 111 dollars and 12 cents Ryan 34 dollars and 72 cents",
    )

    rows = engine.parse_transcript_to_rows(payload)
    amounts = {r.employee: r.amount_final for r in rows}
    assert amounts["Kevin Worley"] == 111.12
    assert amounts["Mike Walton"] == 111.12
    assert amounts["Ryan Alexander"] == 34.72


def test_plain_dollar_amounts_with_trailing_dot_parse_to_whole_dollars():
    with mock.patch("google.cloud.bigquery.Client") as client_mock:
        client_mock.return_value = mock.Mock()
        engine = importlib.reload(importlib.import_module("engine.payroll_engine"))

    payload = engine.TranscriptIn(
        filename="120425_PM.wav",
        transcript="December 4th 2025, PM shift, Austin $120.",
    )

    rows = engine.parse_transcript_to_rows(payload)
    amounts = {r.employee: r.amount_final for r in rows}
    assert amounts["Austin Kelley"] == 120.00


def test_fiona_dodson_normalization_and_support_category():
    with mock.patch("google.cloud.bigquery.Client") as client_mock:
        client_mock.return_value = mock.Mock()
        engine = importlib.reload(importlib.import_module("engine.payroll_engine"))

    payload = engine.TranscriptIn(
        filename="120425_PM.wav",
        transcript="Fiona 75 04",
    )

    rows = engine.parse_transcript_to_rows(payload)
    assert any(r.employee == "Fiona Dodson" for r in rows)
    fiona_row = next(r for r in rows if r.employee == "Fiona Dodson")
    assert fiona_row.category == "support"
    assert abs(fiona_row.amount_final - 75.04) < 1e-6


def test_lost_him_variants_map_to_austin_kelley():
    with mock.patch("google.cloud.bigquery.Client") as client_mock:
        client_mock.return_value = mock.Mock()
        engine = importlib.reload(importlib.import_module("engine.payroll_engine"))

    payload = engine.TranscriptIn(
        filename="112825_AM.wav",
        transcript="November 28 2025 AM shift Kevin $364.30 lost him $364.30 Ryan $130.94",
    )

    rows = engine.parse_transcript_to_rows(payload)
    amounts = {r.employee: r.amount_final for r in rows}
    assert amounts["Kevin Worley"] == 364.30
    assert amounts["Austin Kelley"] == 364.30
    assert amounts["Ryan Alexander"] == 130.94
