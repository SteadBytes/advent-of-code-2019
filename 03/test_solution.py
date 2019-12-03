import pytest

from solution import path_coords, Coord


@pytest.mark.parametrize(
    "path_moves,expected",
    [
        (
            ["R8", "U5", "L5", "D3"],
            [
                Coord(x=0, y=0),
                Coord(x=1, y=0),
                Coord(x=2, y=0),
                Coord(x=3, y=0),
                Coord(x=4, y=0),
                Coord(x=5, y=0),
                Coord(x=6, y=0),
                Coord(x=7, y=0),
                Coord(x=8, y=0),
                Coord(x=8, y=1),
                Coord(x=8, y=2),
                Coord(x=8, y=3),
                Coord(x=8, y=4),
                Coord(x=8, y=5),
                Coord(x=7, y=5),
                Coord(x=6, y=5),
                Coord(x=5, y=5),
                Coord(x=4, y=5),
                Coord(x=3, y=5),
                Coord(x=3, y=4),
                Coord(x=3, y=3),
                Coord(x=3, y=2),
            ],
        ),
        (
            ["U7", "R6", "D4", "L4"],
            [
                Coord(x=0, y=0),
                Coord(x=0, y=1),
                Coord(x=0, y=2),
                Coord(x=0, y=3),
                Coord(x=0, y=4),
                Coord(x=0, y=5),
                Coord(x=0, y=6),
                Coord(x=0, y=7),
                Coord(x=1, y=7),
                Coord(x=2, y=7),
                Coord(x=3, y=7),
                Coord(x=4, y=7),
                Coord(x=5, y=7),
                Coord(x=6, y=7),
                Coord(x=6, y=6),
                Coord(x=6, y=5),
                Coord(x=6, y=4),
                Coord(x=6, y=3),
                Coord(x=5, y=3),
                Coord(x=4, y=3),
                Coord(x=3, y=3),
                Coord(x=2, y=3),
            ],
        ),
    ],
)
def test_path_coords(path_moves, expected):
    assert list(path_coords(path_moves)) == expected
