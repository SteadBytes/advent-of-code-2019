from typing import NamedTuple, Iterable


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


Wire = Iterable[Coord]

CENTRAL_PORT = Coord(0, 0)


directions = {
    "R": lambda x: Coord(x, 0),
    "L": lambda x: Coord(-x, 0),
    "U": lambda y: Coord(0, y),
    "D": lambda y: Coord(0, -y),
}


def path_coords(path_moves: Iterable[str]) -> Wire:
    pos = CENTRAL_PORT
    for direction, magnitude in ((p[0], p[1:]) for p in path_moves):
        for _ in range(1, int(magnitude) + 1):
            pos += directions[direction](1)
            yield pos


def manhattan(c1: float, c2: float) -> float:
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)


def part_1(w1: Wire, w2: Wire) -> float:
    return min(manhattan(c, CENTRAL_PORT) for c in set(w1) & set(w2))


def part_2(w1: Wire, w2: Wire) -> float:
    wire1_steps = {p: i for i, p in enumerate(w1)}
    return min(i + wire1_steps[p] for i, p in enumerate(w2) if p in wire1_steps)


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    wire1, wire2 = [list(path_coords(l.split(","))) for l in lines]
    print("Part 1: ", part_1(wire1, wire2))
    print("Part 2: ", part_2(wire1, wire2))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
