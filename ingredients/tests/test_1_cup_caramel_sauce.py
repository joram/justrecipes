
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("1 cup caramel sauce")
    expected = {
    "comment": "",
    "material": "caramel sauce",
    "original": "1 cup caramel sauce",
    "quantities": [
        [
            1.0,
            "cup"
        ]
    ]
}

    assert actual == expected
