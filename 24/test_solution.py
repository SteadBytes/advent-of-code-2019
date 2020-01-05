"""
Some functions in solution.py include doctests, include with pytest option:

    $ pytest --doctest-modules
"""
import pytest

import solution as s
from solution import GType


def example_input_lines():
    return ["....#", "#..#.", "#..##", "..#..", "#...."]


@pytest.mark.parametrize(
    "lines,bin_grid",
    [
        (["....#", "#..#.", "#..##", "..#..", "#...."], "0000100100110010100110000"),
        (["##.#.", "##.#.", "##.##", ".####", ".#..."], "0001011110110110101101011"),
    ],
)
def test_parse_input(lines, bin_grid):
    assert s.parse_input(lines) == int(bin_grid, 2)


@pytest.mark.parametrize(
    "loc,coords",
    [
        # Outer corners
        (
            (0, 0),
            [
                (GType.CURRENT, 1, 0),
                (GType.CURRENT, 0, 1),
                (GType.OUTER, 1, 2),
                (GType.OUTER, 2, 1),
            ],
        ),
        (
            (0, 4),
            [
                (GType.CURRENT, 0, 3),
                (GType.CURRENT, 1, 4),
                (GType.OUTER, 2, 3),
                (GType.OUTER, 1, 2),
            ],
        ),
        (
            (4, 4),
            [
                (GType.CURRENT, 4, 3),
                (GType.CURRENT, 3, 4),
                (GType.OUTER, 3, 2),
                (GType.OUTER, 2, 3),
            ],
        ),
        (
            (4, 0),
            [
                (GType.CURRENT, 3, 0),
                (GType.CURRENT, 4, 1),
                (GType.OUTER, 2, 1),
                (GType.OUTER, 3, 2),
            ],
        ),
        # Inner corners
        (
            (1, 1),
            [
                (GType.CURRENT, 1, 0),
                (GType.CURRENT, 1, 2),
                (GType.CURRENT, 0, 1),
                (GType.CURRENT, 2, 1),
            ],
        ),
    ],
)
def test_adjacent_coords(loc, coords):
    x, y = loc
    assert sorted(list(s.adjacent_coords(x, y))) == sorted(coords)
