from mise_inventory.tokenizer import split_line_into_segments


def test_split_line_with_and():
    line = "two bottles of wine and three cases of beer"
    segments = split_line_into_segments(line)
    assert len(segments) == 2
    assert "two bottles" in segments[0]
    assert "three cases" in segments[1]


def test_split_line_without_quantities_keeps_whole():
    line = "this is just narrative text without numbers"
    segments = split_line_into_segments(line)
    assert segments == [line]
