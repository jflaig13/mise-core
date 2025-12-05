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
