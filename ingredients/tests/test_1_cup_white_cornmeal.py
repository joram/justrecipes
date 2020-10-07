
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("1 cup white cornmeal")
    expected = {
    "comment": "",
    "material": "white cornmeal",
    "original": "1 cup white cornmeal",
    "quantities": [
        [
            1.0,
            "cup"
        ]
    ]
}

    assert actual == expected
