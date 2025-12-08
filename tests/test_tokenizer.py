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


def test_split_line_with_repeated_quantity_phrases():
    line = "one can of watermelon high noon one can of michelob ultra one can of coors light"
    segments = split_line_into_segments(line)
    assert len(segments) == 3
    assert "watermelon high noon" in segments[0].lower()
    assert "michelob ultra" in segments[1].lower()
    assert "coors light" in segments[2].lower()


def test_split_line_drops_preamble_and_connectors():
    line = "and on top we have one can of cola and one can of ginger ale on the shelf"
    segments = split_line_into_segments(line)
    assert segments[0] == "one can of cola"
    assert segments[1].startswith("one can of ginger ale")


def test_split_line_with_hyphenated_pack_sizes():
    line = "we have five 24-packs of yingling seven 12-packs of coors"
    segments = split_line_into_segments(line)
    assert len(segments) == 2
    assert segments[0].startswith("five 24-packs of yingling")
    assert segments[1].startswith("seven 12-packs of coors")
