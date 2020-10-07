
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("1 (8 ounce) package toffee baking bits (such as SKOR®)")
    expected = {
    "comment": "8 ounce) package toffee baking bits (such as SKOR\u00ae",
    "material": "",
    "original": "1 (8 ounce) package toffee baking bits (such as SKOR\u00ae)",
    "quantities": [
        [
            1.0,
            ""
        ]
    ]
}

    assert actual == expected
