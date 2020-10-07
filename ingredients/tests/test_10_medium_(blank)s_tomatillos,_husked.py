
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("10 medium (blank)s tomatillos, husked")
    expected = {
    "comment": "husked",
    "material": "medium tomatillos",
    "original": "10 medium (blank)s tomatillos, husked",
    "quantities": [
        [
            10.0,
            ""
        ]
    ]
}

    assert actual == expected
