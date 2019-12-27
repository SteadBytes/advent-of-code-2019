import heapq
from collections import defaultdict
from enum import Enum
from typing import DefaultDict, Dict, Iterable, List, NamedTuple, Tuple


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
    outer: bool


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
                    p = Portal(
                        val + row[loc.x + 1], loc + Coord(-1, 0), loc.x + 2 == len(row)
                    )
                # Interior RHS inner label or exterior LHS inner label
                elif loc.x + 1 < len(row) and row[loc.x + 1] == ".":
                    p = Portal(row[loc.x - 1] + val, loc + Coord(1, 0), loc.x - 1 == 0)
                # Interior top inner label or exterior bottom innter label
                elif loc.y > 0 and grid[loc.y - 1][loc.x] == ".":
                    p = Portal(
                        val + grid[loc.y + 1][loc.x],
                        loc + Coord(0, -1),
                        loc.y + 2 == len(grid),
                    )
                # Interor bottom inner label or exterior top inner label
                elif loc.y + 1 < len(grid) and grid[loc.y + 1][loc.x] == ".":
                    p = Portal(
                        grid[loc.y - 1][loc.x] + val, loc + Coord(0, 1), loc.y - 1 == 0
                    )
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
        for next_loc in neighbours(loc):
            if next_loc in seen or m[next_loc] != Tile.OPEN:
                continue
            heapq.heappush(q, (dist + 1, next_loc))
        if loc in pm and pm[loc] not in seen:
            heapq.heappush(q, (dist + 1, pm[loc]))

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


def is_disabled(p: Portal, depth: int) -> bool:
    if depth == 0:
        return p.outer and p.label not in ("AA", "ZZ")
    else:
        return p.outer and p.label in ("AA", "ZZ")


def find_shortest_path_length_recursive_levels(
    src: Portal, dest: Portal, m: Map, pm: Dict[Coord, Portal], ps: Portals
) -> int:
    """BFS again with the addition of tracking the *depth* at which a location has
    been visited.

    Portal behaviour:
    - Disabled portals treated as walls
    - Depth 0
        - All *outer* portals disabled *except* AA and ZZ
        - Inner portals increment depth (recurse into smaller maze)
    - Depth > 0
        - AA and ZZ disabled
        - Outer portals decrement depth ('pop the stack' into the previous recursion)
        - Inner portals increment depth (recurse into smaller maze)
    - Terminate when depth 0 and location == ZZ
    """
    seen = set()
    q = [(0, 0, src.location)]
    while q:
        dist, depth, loc = heapq.heappop(q)
        seen.add((depth, loc))
        if depth == 0 and loc == dest.location:
            return dist

        if loc in pm:
            # TODO: Refactor portal data structures to avoid this double lookup
            dest_portal = pm[loc]
            src_portal = pm[dest_portal.location]
            if not is_disabled(src_portal, depth):
                d = depth - 1 if dest_portal.outer else depth + 1
                if (d, dest_portal.location) not in seen:
                    heapq.heappush(q, (dist + 1, d, dest_portal.location))

        for next_loc in neighbours(loc):
            if (depth, next_loc) in seen or m[next_loc] != Tile.OPEN:
                continue
            if next_loc in pm:
                # TODO: See above
                dest_portal = pm[next_loc]
                src_portal = pm[dest_portal.location]
                if is_disabled(src_portal, depth):
                    continue
            heapq.heappush(q, (dist + 1, depth, next_loc))
    raise RuntimeError(f"No path found from {src} -> {dest}")


def part_2(grid: Grid) -> int:
    # TODO: Refactor this repeated work from part 1
    m, portals = parse_grid(grid)
    assert len(portals["AA"]) == 1
    assert len(portals["ZZ"]) == 1
    src_portal, dest_portal = portals.pop("AA")[0], portals.pop("ZZ")[0]
    assert src_portal.outer is True
    assert dest_portal.outer is True
    pm = {}
    for label, (p1, p2) in portals.items():
        pm[p1.location] = p2
        pm[p2.location] = p1
    return find_shortest_path_length_recursive_levels(
        src_portal, dest_portal, m, pm, portals
    )


def main(puzzle_input_f):
    lines = [l.strip("\n") for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2(lines))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
