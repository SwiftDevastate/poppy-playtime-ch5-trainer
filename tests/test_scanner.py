from memory.scanner import find_pattern


def test_find_pattern_with_wildcards():
    buf = b"\xAA\xBB\x48\x8B\x0D\x11\x22\x33\x44\xF3"
    hits = find_pattern(buf, b"\x48\x8B\x0D\x00\x00\x00\x00")
    assert hits == [2]


def test_find_pattern_no_match():
    assert find_pattern(b"\x00" * 32, b"\xDE\xAD\xBE\xEF") == []