import pytest

from solution import parse_layers, build_image_matrix


@pytest.mark.parametrize(
    "image_data,width,height,expected_layers",
    [
        (
            "123456789012",
            3,
            2,
            [("1", "2", "3", "4", "5", "6"), ("7", "8", "9", "0", "1", "2")],
        ),
        (
            "0222112222120000",
            2,
            2,
            [
                ("0", "2", "2", "2"),
                ("1", "1", "2", "2"),
                ("2", "2", "1", "2"),
                ("0", "0", "0", "0"),
            ],
        ),
    ],
)
def test_parse_layers(image_data, width, height, expected_layers):
    assert list(parse_layers(image_data, width, height)) == expected_layers


def test_build_image_matrix():
    layers = [
        ("0", "2", "2", "2"),
        ("1", "1", "2", "2"),
        ("2", "2", "1", "2"),
        ("0", "0", "0", "0"),
    ]
    assert build_image_matrix(layers, 2) == [["0", "1"], ["1", "0"]]
