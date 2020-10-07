
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("3 tablespoons confectioners' sugar")
    expected = {
    "comment": "",
    "material": "confectioners' sugar",
    "original": "3 tablespoons confectioners' sugar",
    "quantities": [
        [
            3.0,
            "tablespoon"
        ]
    ]
}

    assert actual == expected
