
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("2 quarts water")
    expected = {
    "comment": "",
    "material": "water",
    "original": "2 quarts water",
    "quantities": [
        [
            2.0,
            "quart"
        ]
    ]
}

    assert actual == expected
