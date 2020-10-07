
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("3 cloves garlic, chopped")
    expected = {
    "comment": "chopped",
    "material": "cloves garlic",
    "original": "3 cloves garlic, chopped",
    "quantities": [
        [
            3.0,
            ""
        ]
    ]
}

    assert actual == expected
