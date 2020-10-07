
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse(".5 cup boiling water")
    expected = {
    "comment": "",
    "material": ".5  boiling water",
    "original": ".5 cup boiling water",
    "quantities": [
        [
            0.5,
            "cup"
        ]
    ]
}

    assert actual == expected
