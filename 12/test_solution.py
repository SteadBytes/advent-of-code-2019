from solution import parse_input, Coord3d


def test_parse_input():
    lines = [
        "<x=6, y=10, z=10>",
        "<x=-9, y=3, z=17>",
        "<x=9, y=-4, z=14>",
        "<x=4, y=14, z=4>",
    ]

    assert parse_input(lines) == [
        Coord3d(6, 10, 10),
        Coord3d(-9, 3, 17),
        Coord3d(9, -4, 14),
        Coord3d(4, 14, 4),
    ]
