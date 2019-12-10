from collections import defaultdict
from math import gcd
from typing import Iterable, List, NamedTuple


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


Asteroid = Coord


# TODO: document/comment this
def asteroids_in_los(source: Asteroid, asteroids: List[Asteroid]):
    asteroid_distances_by_direction = defaultdict(list)
    for ast in filter(lambda ast: ast != source, asteroids):
        dx, dy = ast - source
        dist = gcd(abs(dx), abs(dy))
        vec = (dx / dist, dy / dist)
        asteroid_distances_by_direction[vec].append((dist, ast))
    return [min(asts)[1] for asts in asteroid_distances_by_direction.values()]


def part_1(asteroids: List[Asteroid]):
    return max(len(asteroids_in_los(ast, asteroids)) for ast in asteroids)


def part_2():
    pass


def parse_input(lines: Iterable[str]) -> List[Asteroid]:
    return [
        Coord(x, y)
        for y, row in enumerate(lines)
        for x, val in enumerate(row)
        if val == "#"
    ]


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    asteroids = parse_input(lines)
    print("Part 1: ", part_1(asteroids))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
