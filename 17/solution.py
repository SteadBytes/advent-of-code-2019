import asyncio
import re
from enum import Enum
from functools import reduce
from itertools import takewhile
from typing import Dict, Iterable, List, NamedTuple, Tuple, TypeVar

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
    Direction.EAST: Coord(1, 0),
    Direction.SOUTH: Coord(0, 1),
    Direction.WEST: Coord(-1, 0),
}


class Turn(Enum):
    LEFT = "L"
    RIGHT = "R"


LEFT_TURN_DIRECTIONS = {
    Direction.NORTH: Direction.WEST,
    Direction.EAST: Direction.NORTH,
    Direction.SOUTH: Direction.EAST,
    Direction.WEST: Direction.SOUTH,
}

RIGHT_TURN_DIRECTIONS = {v: k for k, v in LEFT_TURN_DIRECTIONS.items()}

MOVEMENT_FUNCTION_CHAR_LIMIT = 20  # Not including newline

MOVEMENT_FUNCTION_RE = (
    r"^(?P<A>.{1,20})\1*(?P<B>.{1,20})(?:\1|\2)*(?P<C>.{1,20})(?:\1|\2|\3)*$"
)

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


def pairwise_exclusive(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5.."""
    it = iter(iterable)
    return zip(it, it)


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
    m = build_map(mem)
    return sum_alignment_parameters(m)


def find_robot(m: ScaffoldMap) -> Tuple[Coord, Direction]:
    for loc, val in m.items():
        if val in "^v<>":
            return (loc, Direction(val))


def scaffold_route(start_loc: Coord, start_dir: Direction, m: ScaffoldMap):
    # TODO: PLEASE IMPROVE THIS
    current_loc, current_dir = start_loc, start_dir
    forward_count = 0
    while True:
        # Try move forward
        next_loc = current_loc + MOVE_DIRECTIONS[current_dir]
        if m.get(next_loc) == "#":
            current_loc = next_loc
            forward_count += 1
        else:
            # Try left turn
            next_dir = LEFT_TURN_DIRECTIONS[current_dir]
            next_loc = current_loc + MOVE_DIRECTIONS[next_dir]
            if m.get(next_loc) == "#":
                current_dir = next_dir
                if forward_count:
                    yield forward_count
                    forward_count = 0
                yield Turn.LEFT
            else:
                # Try right turn
                next_dir = RIGHT_TURN_DIRECTIONS[current_dir]
                next_loc = current_loc + MOVE_DIRECTIONS[next_dir]
                if m.get(next_loc) == "#":
                    if forward_count:
                        yield forward_count
                        forward_count = 0
                    current_dir = next_dir
                    yield Turn.RIGHT
                else:
                    if forward_count:
                        yield forward_count
                    return


async def run_movement_program(mem: intcode.Memory, main_routine, movement_funcs):
    mem[0] = 2
    inqueue = asyncio.Queue()
    for c in main_routine + "\n":
        await inqueue.put(ord(c))
    for k, pattern in movement_funcs.items():
        for c in pattern + "\n":
            await inqueue.put(ord(c))
    await inqueue.put(ord("n"))
    await inqueue.put(ord("\n"))

    collector = output_collector()
    await asyncio.create_task(intcode.execute(mem, inqueue.get, collector))
    return collector.output


def part_2(prg: intcode.Program):
    mem = intcode.prg_to_memory(prg)
    m = build_map(mem)
    robot_loc, robot_dir = find_robot(m)
    route = scaffold_route(robot_loc, robot_dir, m)
    route_str = ",".join(
        f"{turn.value},{steps}" for turn, steps in pairwise_exclusive(route)
    )
    m = re.match(MOVEMENT_FUNCTION_RE, route_str + ",")
    if not m:
        raise RuntimeError("No movement functions found for route {route_str}")

    movement_funcs = {
        k: v[:-1]  # Remove ending "," from each pattern
        for k, v in m.groupdict().items()
    }
    main_routine = reduce(
        lambda s, rep: s.replace(rep[1], rep[0]), movement_funcs.items(), route_str
    )
    mem = intcode.prg_to_memory(prg)
    robot_output = asyncio.run(run_movement_program(mem, main_routine, movement_funcs))
    assert robot_output[-3:-1] == [10, 10]  # Robot outputs dust value after 2 newlines
    return robot_output[-1]


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
