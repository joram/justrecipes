
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("1 small onion, chopped")
    expected = {
    "comment": "chopped",
    "material": "small onion",
    "original": "1 small onion, chopped",
    "quantities": [
        [
            1.0,
            ""
        ]
    ]
}

    assert actual == expected
