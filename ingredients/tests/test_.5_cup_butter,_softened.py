
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse(".5 cup butter, softened")
    expected = {
    "comment": "softened",
    "material": ".5  butter",
    "original": ".5 cup butter, softened",
    "quantities": [
        [
            0.5,
            "cup"
        ]
    ]
}

    assert actual == expected
