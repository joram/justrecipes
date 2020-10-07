
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("2 cups boiling water")
    expected = {
    "comment": "",
    "material": "boiling water",
    "original": "2 cups boiling water",
    "quantities": [
        [
            2.0,
            "cup"
        ]
    ]
}

    assert actual == expected
