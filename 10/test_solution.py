import pytest

from solution import asteroids_in_los, parse_input, part_1


def test_parse_input():
    lines = [".#..#", ".....", "#####", "....#", "...##"]
    assert parse_input(lines) == [
        (1, 0),
        (4, 0),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (4, 3),
        (3, 4),
        (4, 4),
    ]


@pytest.mark.parametrize(
    "source_asteroid,expected",
    [((1, 0), {(4, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (4, 4)})],
)
def test_asteroids_in_los(source_asteroid, expected):
    lines = [".#..#", ".....", "#####", "....#", "...##"]
    asteroids = parse_input(lines)
    assert set(asteroids_in_los(source_asteroid, asteroids)) == expected


def test_part_1():
    lines = [".#..#", ".....", "#####", "....#", "...##"]
    asteroids = parse_input(lines)
    assert part_1(asteroids) == 8
