
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("2 tablespoons dried cranberries")
    expected = {
    "comment": "",
    "material": "dried cranberries",
    "original": "2 tablespoons dried cranberries",
    "quantities": [
        [
            2.0,
            "tablespoon"
        ]
    ]
}

    assert actual == expected
