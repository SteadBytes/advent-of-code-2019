import pytest

from solution import Coord, intersections, sum_alignment_parameters, grid_to_map


@pytest.fixture
def example_grid():
    return [
        "..#..........",
        "..#..........",
        "#######...###",
        "#.#...#...#.#",
        "#############",
        "..#...#...#..",
        "..#####...^..",
    ]


@pytest.fixture
def example_map():
    return {
        Coord(0, 0): ".",
        Coord(1, 0): ".",
        Coord(2, 0): "#",
        Coord(3, 0): ".",
        Coord(4, 0): ".",
        Coord(5, 0): ".",
        Coord(6, 0): ".",
        Coord(7, 0): ".",
        Coord(8, 0): ".",
        Coord(9, 0): ".",
        Coord(10, 0): ".",
        Coord(11, 0): ".",
        Coord(12, 0): ".",
        Coord(0, 1): ".",
        Coord(1, 1): ".",
        Coord(2, 1): "#",
        Coord(3, 1): ".",
        Coord(4, 1): ".",
        Coord(5, 1): ".",
        Coord(6, 1): ".",
        Coord(7, 1): ".",
        Coord(8, 1): ".",
        Coord(9, 1): ".",
        Coord(10, 1): ".",
        Coord(11, 1): ".",
        Coord(12, 1): ".",
        Coord(0, 2): "#",
        Coord(1, 2): "#",
        Coord(2, 2): "#",
        Coord(3, 2): "#",
        Coord(4, 2): "#",
        Coord(5, 2): "#",
        Coord(6, 2): "#",
        Coord(7, 2): ".",
        Coord(8, 2): ".",
        Coord(9, 2): ".",
        Coord(10, 2): "#",
        Coord(11, 2): "#",
        Coord(12, 2): "#",
        Coord(0, 3): "#",
        Coord(1, 3): ".",
        Coord(2, 3): "#",
        Coord(3, 3): ".",
        Coord(4, 3): ".",
        Coord(5, 3): ".",
        Coord(6, 3): "#",
        Coord(7, 3): ".",
        Coord(8, 3): ".",
        Coord(9, 3): ".",
        Coord(10, 3): "#",
        Coord(11, 3): ".",
        Coord(12, 3): "#",
        Coord(0, 4): "#",
        Coord(1, 4): "#",
        Coord(2, 4): "#",
        Coord(3, 4): "#",
        Coord(4, 4): "#",
        Coord(5, 4): "#",
        Coord(6, 4): "#",
        Coord(7, 4): "#",
        Coord(8, 4): "#",
        Coord(9, 4): "#",
        Coord(10, 4): "#",
        Coord(11, 4): "#",
        Coord(12, 4): "#",
        Coord(0, 5): ".",
        Coord(1, 5): ".",
        Coord(2, 5): "#",
        Coord(3, 5): ".",
        Coord(4, 5): ".",
        Coord(5, 5): ".",
        Coord(6, 5): "#",
        Coord(7, 5): ".",
        Coord(8, 5): ".",
        Coord(9, 5): ".",
        Coord(10, 5): "#",
        Coord(11, 5): ".",
        Coord(12, 5): ".",
        Coord(0, 6): ".",
        Coord(1, 6): ".",
        Coord(2, 6): "#",
        Coord(3, 6): "#",
        Coord(4, 6): "#",
        Coord(5, 6): "#",
        Coord(6, 6): "#",
        Coord(7, 6): ".",
        Coord(8, 6): ".",
        Coord(9, 6): ".",
        Coord(10, 6): "^",
        Coord(11, 6): ".",
        Coord(12, 6): ".",
    }


def test_grid_to_map(example_grid, example_map):
    assert grid_to_map(example_grid) == example_map


def test_intersections(example_map):
    assert list(intersections(example_map)) == [
        Coord(2, 2),
        Coord(2, 4),
        Coord(6, 4),
        Coord(10, 4),
    ]


def test_sum_alignement_parameters(example_map):
    assert sum_alignment_parameters(example_map) == 76
