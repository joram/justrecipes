
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("2 pounds white mushrooms")
    expected = {
    "comment": "",
    "material": "pounds white mushrooms",
    "original": "2 pounds white mushrooms",
    "quantities": [
        [
            2.0,
            "pound"
        ]
    ]
}

    assert actual == expected
