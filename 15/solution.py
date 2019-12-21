import asyncio
from collections import deque
from enum import IntEnum
from typing import Iterable, List, NamedTuple, Set, Tuple, Deque, Optional

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


class MoveCmd(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class DroidStatus(IntEnum):
    WALL = 0
    MOVED = 1
    MOVED_FOUND_SYSTEM = 2


class LocationType(IntEnum):
    EMPTY = 0
    WALL = 1
    OXYGEN_SYSTEM = 2


MOVE_DIRECTIONS = {
    MoveCmd.NORTH: Coord(0, -1),
    MoveCmd.SOUTH: Coord(0, 1),
    MoveCmd.WEST: Coord(-1, 0),
    MoveCmd.EAST: Coord(1, 0),
}

DROID_START_LOCATION = Coord(0, 0)


def moves_from(loc: Coord) -> Iterable[Tuple[Coord, MoveCmd]]:
    return ((loc + diff, move_cmd) for move_cmd, diff in MOVE_DIRECTIONS.items())


def find_path(
    start: Coord, target: Coord, traversable_locations: Set[Coord]
) -> List[Tuple[Coord, MoveCmd]]:
    SearchNode = Tuple[Coord, List[Tuple[Coord, MoveCmd]]]
    if start == target:
        return []
    seen: Set[Coord] = set()
    q: Deque[SearchNode] = deque([(start, [])])
    while True:
        loc, path = q.popleft()
        for next_loc, move_cmd in moves_from(loc):
            next_path = path + [(next_loc, move_cmd)]
            if next_loc == target:
                return next_path
            if next_loc in seen or next_loc not in traversable_locations:
                continue
            q.append((next_loc, next_path))
            seen.add(next_loc)


async def explore_ship(mem: intcode.Memory) -> Tuple[Set[Coord], Coord]:
    seen: Set[Coord] = set()
    traversable_locations: Set[Coord] = set()
    oxygen_system_pos: Optional[Coord] = None
    droid_loc = DROID_START_LOCATION
    to_visit = {droid_loc}
    inq: asyncio.Queue = asyncio.Queue()
    outq: asyncio.Queue = asyncio.Queue()

    pc = asyncio.create_task(intcode.execute(mem, inq.get, outq.put))

    while to_visit:
        target = to_visit.pop()
        seen.add(target)
        path = find_path(droid_loc, target, traversable_locations)
        if path:
            for next_loc, move_cmd in path:
                await inq.put(move_cmd)
                status = await outq.get()
                if status == DroidStatus.WALL:
                    break
                droid_loc = next_loc
                if status == DroidStatus.MOVED_FOUND_SYSTEM:
                    oxygen_system_pos = droid_loc
        else:
            status = DroidStatus.MOVED

        if status != DroidStatus.WALL:
            traversable_locations.add(droid_loc)

        possible_next_loctions = (l for l, _ in moves_from(droid_loc))
        to_visit.update(filter(lambda l: l not in seen, possible_next_loctions))

    pc.cancel()
    assert oxygen_system_pos is not None
    return traversable_locations, oxygen_system_pos


def part_1(prg: intcode.Program) -> int:
    mem = intcode.prg_to_memory(prg)
    traversable_locations, oxygen_system_pos = asyncio.run(explore_ship(mem))
    return len(
        find_path(DROID_START_LOCATION, oxygen_system_pos, traversable_locations)
    )


def part_2(prg: intcode.Program) -> int:
    mem = intcode.prg_to_memory(prg)
    traversable_locations, oxygen_system_pos = asyncio.run(explore_ship(mem))
    # Filling with oxygen is equivalent to the longest path from any empty location
    # in the ship
    return max(
        len(find_path(oxygen_system_pos, loc, traversable_locations))
        for loc in traversable_locations
    )


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
