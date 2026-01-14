"""
Pytest test suite for CPM payroll parsing logic.

Tests name normalization, amount parsing, and database integration.
"""

import pytest
import requests
from pathlib import Path


BASE_URL = "http://localhost:8080"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures():
    """Load all test fixtures."""
    import json
    fixtures_data = {}
    for fixture_file in FIXTURES_DIR.glob("*.json"):
        with open(fixture_file) as f:
            fixtures_data[fixture_file.stem] = json.load(f)
    return fixtures_data


class TestHealthChecks:
    """Test service health endpoints."""

    def test_payroll_engine_ping(self):
        """Test payroll engine is running."""
        response = requests.get(f"{BASE_URL}/ping")
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert "database" in data

    def test_mock_transcriber_health(self):
        """Test mock transcriber is running."""
        response = requests.get("http://localhost:8081/health")
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert data["service"] == "mock_transcriber"


class TestNameNormalization:
    """Test employee name normalization from Whisper errors."""

    def test_whisper_hallucinations(self, fixtures):
        """Test normalization of common Whisper errors."""
        fixture = fixtures["whisper_hallucinations"]

        # Create temp file
        temp_wav = Path("/tmp/hallucinations.wav")
        temp_wav.touch()

        try:
            # Call parse endpoint
            with open(temp_wav, "rb") as f:
                response = requests.post(
                    f"{BASE_URL}/parse_only",
                    files={"audio": f},
                    data={"shift": "AM"},
                )

            assert response.status_code == 200
            data = response.json()
            rows = data.get("rows", [])

            # Check expected normalizations
            employees = [row["employee"] for row in rows]
            assert "Austin Kelley" in employees  # "lost him" → Austin
            assert "Coben Cross" in employees    # "covid" → Coben
            assert "Brooke Neal" in employees    # "broke Neil" → Brooke
            assert "Ryan Alexander" in employees  # "run" → Ryan

        finally:
            temp_wav.unlink()


class TestAmountParsing:
    """Test amount parsing edge cases."""

    def test_edge_case_amounts(self, fixtures):
        """Test parsing of various amount formats."""
        fixture = fixtures["edge_case_amounts"]

        temp_wav = Path("/tmp/amounts.wav")
        temp_wav.touch()

        try:
            with open(temp_wav, "rb") as f:
                response = requests.post(
                    f"{BASE_URL}/parse_only",
                    files={"audio": f},
                    data={"shift": "AM"},
                )

            assert response.status_code == 200
            data = response.json()
            rows = data.get("rows", [])

            # Verify amounts were parsed
            assert len(rows) == fixture["expected_rows"]
            for row in rows:
                assert "amount_final" in row
                assert row["amount_final"] > 0

        finally:
            temp_wav.unlink()


class TestDatabaseIntegration:
    """Test database operations."""

    def test_parse_only_does_not_commit(self, fixtures):
        """Verify parse_only doesn't write to database."""
        fixture = fixtures["monday_am_simple"]

        temp_wav = Path("/tmp/monday_am_120925.wav")
        temp_wav.touch()

        try:
            # Get initial ping (includes row count)
            ping_before = requests.get(f"{BASE_URL}/ping").json()

            # Parse without committing
            with open(temp_wav, "rb") as f:
                response = requests.post(
                    f"{BASE_URL}/parse_only",
                    files={"audio": f},
                    data={"shift": "AM"},
                )

            assert response.status_code == 200

            # Row count should be unchanged
            ping_after = requests.get(f"{BASE_URL}/ping").json()
            assert ping_before["database"]["row_count"] == ping_after["database"]["row_count"]

        finally:
            temp_wav.unlink()


class TestComplexRoles:
    """Test parsing of complex shifts with multiple roles."""

    def test_complex_roles_fixture(self, fixtures):
        """Test shift with servers, expo, busser, utility."""
        fixture = fixtures["complex_roles"]

        temp_wav = Path("/tmp/complex_121125.wav")
        temp_wav.touch()

        try:
            with open(temp_wav, "rb") as f:
                response = requests.post(
                    f"{BASE_URL}/parse_only",
                    files={"audio": f},
                    data={"shift": "PM"},
                )

            assert response.status_code == 200
            data = response.json()
            rows = data.get("rows", [])

            assert len(rows) == fixture["expected_rows"]

            # Check role variety
            roles = [row["role"] for row in rows]
            assert "server" in roles
            assert "expo" in roles
            assert "busser" in roles
            assert "utility" in roles

        finally:
            temp_wav.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
