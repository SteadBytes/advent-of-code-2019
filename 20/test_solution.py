import pytest

from solution import Coord, Portal, parse_grid, Tile


@pytest.fixture
def example_grid():
    return [
        "         A           ",
        "         A           ",
        "  #######.#########  ",
        "  #######.........#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #####  B    ###.#  ",
        "BC...##  C    ###.#  ",
        "  ##.##       ###.#  ",
        "  ##...DE  F  ###.#  ",
        "  #####    G  ###.#  ",
        "  #########.#####.#  ",
        "DE..#######...###.#  ",
        "  #.#########.###.#  ",
        "FG..#########.....#  ",
        "  ###########.#####  ",
        "             Z       ",
        "             Z       ",
    ]


def test_parse_grid(example_grid):
    m = parse_grid(example_grid)

    assert m.start == Coord(9, 2)
    assert m.end == Coord(13, 16)

    assert m.portals == {
        Coord(9, 6): (
            Portal(label="BC", location=Coord(9, 6), outer=False),
            Portal(label="BC", location=Coord(2, 8), outer=True),
        ),
        Coord(2, 8): (
            Portal(label="BC", location=Coord(2, 8), outer=True),
            Portal(label="BC", location=Coord(9, 6), outer=False),
        ),
        Coord(6, 10): (
            Portal(label="DE", location=Coord(6, 10), outer=False),
            Portal(label="DE", location=Coord(2, 13), outer=True),
        ),
        Coord(2, 13): (
            Portal(label="DE", location=Coord(2, 13), outer=True),
            Portal(label="DE", location=Coord(6, 10), outer=False),
        ),
        Coord(11, 12): (
            Portal(label="FG", location=Coord(11, 12), outer=False),
            Portal(label="FG", location=Coord(2, 15), outer=True),
        ),
        Coord(2, 15): (
            Portal(label="FG", location=Coord(2, 15), outer=True),
            Portal(label="FG", location=Coord(11, 12), outer=False),
        ),
    }

    for y, row in enumerate(example_grid):
        for x, val in enumerate(row):
            loc = Coord(x, y)
            t = m.tiles[loc]
            if val == "#":
                assert t == Tile.WALL
            elif val == ".":
                assert t == Tile.OPEN
            elif val == " ":
                assert t == Tile.EMPTY
            elif val.isupper():
                assert t == Tile.EMPTY
            else:
                # defaultdict default value
                assert t == Tile.EMPTY
