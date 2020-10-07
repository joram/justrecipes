
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("1/4 cup chopped fresh cilantro")
    expected = {
    "comment": "",
    "material": "chopped fresh cilantro",
    "original": "1/4 cup chopped fresh cilantro",
    "quantities": [
        [
            0.25,
            "cup"
        ]
    ]
}

    assert actual == expected
