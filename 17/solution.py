import asyncio
from enum import Enum
from itertools import takewhile
from typing import Dict, Iterable, List, NamedTuple, TypeVar

import intcode


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


class Direction(Enum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"


MOVE_DIRECTIONS = {
    Direction.NORTH: Coord(0, -1),
    Direction.EAST: Coord(0, 1),
    Direction.SOUTH: Coord(-1, 0),
    Direction.WEST: Coord(1, 0),
}

T = TypeVar("T")
Grid = Iterable[List[str]]
ScaffoldMap = Dict[Coord, str]


class output_collector:
    def __init__(self):
        self.output: List[int] = []

    async def __call__(self, value: int):
        self.output.append(value)


def split_iter(iterable: Iterable[T], sep: T) -> Iterable[List[T]]:
    it = iter(iterable)
    while True:
        split = list(takewhile(lambda x: x != sep, it))
        if not split:
            break
        yield split


def grid_to_map(grid: Grid) -> ScaffoldMap:
    return {Coord(x, y): v for y, row in enumerate(grid) for x, v in enumerate(row)}


def build_map(mem: intcode.Memory) -> ScaffoldMap:
    collector = output_collector()
    asyncio.run(intcode.execute(mem, intcode.no_input, collector))
    grid = split_iter(map(chr, collector.output[:-1]), "\n")
    return grid_to_map(grid)


def neighbours(loc: Coord) -> Iterable[Coord]:
    return (loc + diff for diff in MOVE_DIRECTIONS.values())


def is_intersection(loc: Coord, m: ScaffoldMap) -> bool:
    if m[loc] != "#":
        return False
    neighbour_scaffold = [l for l in neighbours(loc) if l in m and m[l] == "#"]
    return len(neighbour_scaffold) == 4


def intersections(m: ScaffoldMap) -> Iterable[Coord]:
    return (l for l in m if is_intersection(l, m))


def sum_alignment_parameters(m: ScaffoldMap) -> int:
    return sum(l.x * l.y for l in intersections(m))


def part_1(prg: intcode.Program):
    mem = intcode.prg_to_memory(prg)
    map = build_map(mem)
    return sum_alignment_parameters(map)


def part_2(prg: intcode.Program):

    pass


def main(puzzle_input_f):
    line = puzzle_input_f.read().strip()
    prg = [int(x) for x in line.split(",")]
    print("Part 1: ", part_1(prg[:]))
    print("Part 2: ", part_2(prg))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
