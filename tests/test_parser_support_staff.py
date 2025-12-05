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
