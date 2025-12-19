import pytest

from inventory_agent.parser import parse_quantity


@pytest.mark.parametrize(
    "text,expected",
    [
        ("half a bottle", 0.5),
        ("quarter bottle", 0.25),
        ("three quarters left", 0.75),
        ("full case", 1.0),
        ("80% of a bottle", 0.8),
        ("10 percent bottle", 0.10),
        ("2 six pack", 12.0),
    ],
)
def test_parse_quantity_fraction_and_percent(text, expected):
    assert parse_quantity(text, {"fraction_words": {}}) == pytest.approx(expected)


def test_parse_quantity_word_number():
    assert parse_quantity("two bottles", {"fraction_words": {}}) == 2.0
