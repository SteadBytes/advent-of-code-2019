import heapq
from collections import defaultdict
from enum import Enum
from typing import (DefaultDict, Dict, Iterable, List, NamedTuple, Optional,
                    Tuple)


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


class Portal(NamedTuple):
    label: str
    location: Coord


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Tile(Enum):
    OPEN = "."
    WALL = "#"
    EMPTY = " "


MOVE_DIRECTIONS = {
    Direction.NORTH: Coord(0, -1),
    Direction.EAST: Coord(1, 0),
    Direction.SOUTH: Coord(0, 1),
    Direction.WEST: Coord(-1, 0),
}

Grid = List[str]
Map = DefaultDict[Coord, Tile]
Portals = DefaultDict[str, List[Portal]]
PortalMap = Dict[Coord, Coord]


def neighbours(loc: Coord) -> Iterable[Coord]:
    return (loc + diff for diff in MOVE_DIRECTIONS.values())


def parse_grid(grid: Grid) -> Tuple[Map, Portals]:
    m: Map = defaultdict(lambda: Tile.EMPTY)
    portals: Portals = defaultdict(list)
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            # TODO: Tidy this up
            loc = Coord(x, y)
            if val.isupper():  # Portal
                # Interior LHS inner label or exterior RHS inner label
                if loc.x > 0 and row[loc.x - 1] == ".":
                    p = Portal(val + row[loc.x + 1], loc + Coord(-1, 0))
                # Interior RHS inner label or exterior LHS inner label
                elif loc.x + 1 < len(row) and row[loc.x + 1] == ".":
                    p = Portal(row[loc.x - 1] + val, loc + Coord(1, 0))
                # Interior top inner label or exterior bottom innter label
                elif loc.y > 0 and grid[loc.y - 1][loc.x] == ".":
                    p = Portal(val + grid[loc.y + 1][loc.x], loc + Coord(0, -1))
                # Interor bottom inner label or exterior top inner label
                elif loc.y + 1 < len(grid) and grid[loc.y + 1][loc.x] == ".":
                    p = Portal(grid[loc.y - 1][loc.x] + val, loc + Coord(0, 1))
                else:
                    # Ignore outer labels as they're processed as part of inner label
                    continue
                portals[p.label].append(p)
            else:
                tile = Tile(val)
                m[loc] = tile
    return m, portals


def find_shortest_path_length(src: Coord, dest: Coord, m: Map, pm: PortalMap) -> int:
    seen = set()
    q = [(0, src)]
    while q:
        dist, loc = heapq.heappop(q)
        seen.add(loc)
        if loc == dest:
            return dist
        if loc in pm and pm[loc] not in seen:
            heapq.heappush(q, (dist + 1, pm[loc]))
        for next_loc in neighbours(loc):
            if next_loc in seen or m[next_loc] != Tile.OPEN:
                continue
            heapq.heappush(q, (dist + 1, next_loc))
    raise RuntimeError(f"No path found from {src} -> {dest}")


def part_1(grid: Grid) -> int:
    m, portals = parse_grid(grid)
    assert len(portals["AA"]) == 1
    assert len(portals["ZZ"]) == 1
    src, dest = portals.pop("AA")[0].location, portals.pop("ZZ")[0].location
    pm = {}
    for label, (p1, p2) in portals.items():
        pm[p1.location] = p2.location
        pm[p2.location] = p1.location

    return find_shortest_path_length(src, dest, m, pm)


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip("\n") for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
