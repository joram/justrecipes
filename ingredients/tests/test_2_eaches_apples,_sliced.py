
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("2 eaches apples, sliced")
    expected = {
    "comment": "sliced",
    "material": "eaches apples",
    "original": "2 eaches apples, sliced",
    "quantities": [
        [
            2.0,
            ""
        ]
    ]
}

    assert actual == expected
