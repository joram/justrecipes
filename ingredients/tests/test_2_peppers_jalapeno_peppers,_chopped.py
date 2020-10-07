
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("2 peppers jalapeno peppers, chopped")
    expected = {
    "comment": "chopped",
    "material": "peppers jalapeno peppers",
    "original": "2 peppers jalapeno peppers, chopped",
    "quantities": [
        [
            2.0,
            ""
        ]
    ]
}

    assert actual == expected
