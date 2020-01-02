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


