
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("¾ cup brown sugar")
    expected = {
    "comment": "",
    "material": "brown sugar",
    "original": "\u00be cup brown sugar",
    "quantities": [
        [
            0.75,
            "cup"
        ]
    ]
}

    assert actual == expected
