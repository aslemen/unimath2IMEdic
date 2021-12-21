import pytest

import unimath2imedic.roman2kana as r2k

items_MSIME: tuple[tuple[str, str], ...] = (
    ("doubleplus", "どうｂぇｐぅｓ"),
    ("minusdot", "みぬｓどｔ"),
)

@pytest.mark.parametrize(
    "input, output",
    items_MSIME,
)
def test_roman2kana_msime(input: str, output: str):
    assert r2k.roman2kana_msime(input) == output