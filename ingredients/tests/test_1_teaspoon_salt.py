
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("1 teaspoon salt")
    expected = {
    "comment": "",
    "material": "salt",
    "original": "1 teaspoon salt",
    "quantities": [
        [
            1.0,
            "teaspoon"
        ]
    ]
}

    assert actual == expected
