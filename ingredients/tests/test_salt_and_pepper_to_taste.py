
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("salt and pepper to taste")
    expected = {
    "comment": "",
    "material": "salt and pepper to taste",
    "original": "salt and pepper to taste",
    "quantities": [
        [
            1,
            ""
        ]
    ]
}

    assert actual == expected
