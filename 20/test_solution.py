import pytest

import solution as s


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


def test_parse_grid_returns_finds_portals(example_grid):
    m, portals = s.parse_grid(example_grid)

    assert portals == {
        "AA": [s.Portal("AA", s.Coord(9, 2), True)],
        "BC": [
            s.Portal("BC", s.Coord(9, 6), False),
            s.Portal("BC", s.Coord(2, 8), True),
        ],
        "DE": [
            s.Portal("DE", s.Coord(6, 10), False),
            s.Portal("DE", s.Coord(2, 13), True),
        ],
        "FG": [
            s.Portal(label="FG", location=s.Coord(x=11, y=12), outer=False),
            s.Portal(label="FG", location=s.Coord(x=2, y=15), outer=True),
        ],
        "ZZ": [s.Portal(label="ZZ", location=s.Coord(x=13, y=16), outer=True)],
    }
