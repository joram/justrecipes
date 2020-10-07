
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("1 (8 ounce) package cream cheese")
    expected = {
    "comment": "8 ounce",
    "material": "package cream cheese",
    "original": "1 (8 ounce) package cream cheese",
    "quantities": [
        [
            1.0,
            ""
        ]
    ]
}

    assert actual == expected
