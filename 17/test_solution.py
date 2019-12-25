import pytest

import solution as s
from solution import Coord


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
def example_map(example_grid):
    return s.grid_to_map(example_grid)


class TestPartOne:
    def test_grid_to_map(self, example_grid):
        coords = set()
        for y, row in enumerate(example_grid):
            for x, val in enumerate(row):
                coords.add(s.Coord(x, y))

        m = s.grid_to_map(example_grid)

        # Only expected locations are present
        assert not set(m.keys()) - coords

        # Location values match the original grid
        for c in coords:
            assert m[c] == example_grid[c.y][c.x]

    def test_intersections(self, example_map):
        assert list(s.intersections(example_map)) == [
            Coord(2, 2),
            Coord(2, 4),
            Coord(6, 4),
            Coord(10, 4),
        ]

    def test_sum_alignment_parameters(self, example_map):
        assert s.sum_alignment_parameters(example_map) == 76


@pytest.mark.parametrize(
    "example_grid",
    [
        [
            "#######...#####",
            "#.....#...#...#",
            "#.....#...#...#",
            "......#...#...#",
            "......#...###.#",
            "......#.....#.#",
            "^########...#.#",
            "......#.#...#.#",
            "......#########",
            "........#...#..",
            "....#########..",
            "....#...#......",
            "....#...#......",
            "....#...#......",
            "....#####......",
        ]
    ],
)
class TestPartTwo:
    def test_find_robot(self, example_map):
        robot_loc, robot_dir = s.find_robot(example_map)
        assert robot_loc == Coord(0, 6)
        assert robot_dir == s.Direction.NORTH

    def test_scaffold_route(self, example_map):
        robot_loc, robot_dir = s.find_robot(example_map)
        scaffold_locs = {l for l, v in example_map.items() if v == "#"}

        # Make list for introspection
        route = list(s.scaffold_route(robot_loc, robot_dir, example_map))

        current_loc = robot_loc
        current_dir = robot_dir
        traversed = set()
        for turn, steps in s.pairwise_exclusive(route):
            if turn == s.Turn.LEFT:
                current_dir = s.LEFT_TURN_DIRECTIONS[current_dir]
            elif turn == s.Turn.RIGHT:
                current_dir = s.RIGHT_TURN_DIRECTIONS[current_dir]
            else:
                raise ValueError(f"Unexpected {s.Turn} value {turn}")
            for _ in range(steps):
                current_loc += s.MOVE_DIRECTIONS[current_dir]
                traversed.add(current_loc)

        assert traversed - scaffold_locs == set()
