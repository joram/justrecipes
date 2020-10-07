
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("2 onions")
    expected = {
    "comment": "",
    "material": "",
    "original": "2 onions",
    "quantities": [
        [
            2.0,
            "onions"
        ]
    ]
}

    assert actual == expected
