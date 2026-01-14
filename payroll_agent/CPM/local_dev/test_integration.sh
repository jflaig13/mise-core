#!/bin/bash
# Integration test script for CPM local testing
# Tests all fixtures against the local payroll engine

set -e  # Exit on error

BASE_URL="${BASE_URL:-http://localhost:8080}"
FIXTURES_DIR="$(dirname "$0")/fixtures"

echo "========================================="
echo "CPM Integration Tests"
echo "========================================="
echo "Base URL: $BASE_URL"
echo "Fixtures: $FIXTURES_DIR"
echo ""

# Check if engine is running
if ! curl -s -f "$BASE_URL/ping" > /dev/null; then
    echo "❌ Payroll engine not responding at $BASE_URL"
    echo "   Start with: make up"
    exit 1
fi

echo "✓ Payroll engine is running"
echo ""

# Test each fixture
PASSED=0
FAILED=0

for fixture_file in "$FIXTURES_DIR"/*.json; do
    fixture_name=$(basename "$fixture_file" .json)
    echo "Testing: $fixture_name"

    # Read expected row count
    expected_rows=$(jq -r '.expected_rows' "$fixture_file")
    transcript=$(jq -r '.transcript' "$fixture_file")

    # Create temp WAV file (mock transcriber will match by filename)
    temp_wav="/tmp/${fixture_name}.wav"
    touch "$temp_wav"

    # Call /parse_only endpoint
    response=$(curl -s -X POST "$BASE_URL/parse_only" \
        -F "audio=@${temp_wav}" \
        -F "shift=AM")

    # Parse response
    actual_rows=$(echo "$response" | jq -r '.rows | length')

    if [ "$actual_rows" = "$expected_rows" ]; then
        echo "  ✓ Expected $expected_rows rows, got $actual_rows"
        ((PASSED++))
    else
        echo "  ❌ Expected $expected_rows rows, got $actual_rows"
        echo "  Response: $response"
        ((FAILED++))
    fi

    # Cleanup
    rm -f "$temp_wav"
    echo ""
done

# Summary
echo "========================================="
echo "Results: $PASSED passed, $FAILED failed"
echo "========================================="

if [ $FAILED -gt 0 ]; then
    exit 1
fi

exit 0
