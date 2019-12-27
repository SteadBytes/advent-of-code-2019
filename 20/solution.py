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

START_LABEL, END_LABEL = "AA", "ZZ"

Grid = List[str]
TileMap = DefaultDict[Coord, Tile]
PortalMap = Dict[Coord, Tuple[Portal, Portal]]


class Maze(NamedTuple):
    tiles: TileMap
    portals: PortalMap
    start: Coord
    end: Coord


def neighbours(loc: Coord) -> Iterable[Coord]:
    return (loc + diff for diff in MOVE_DIRECTIONS.values())


def parse_grid(grid: Grid) -> Maze:
    m: TileMap = defaultdict(lambda: Tile.EMPTY)
    portals: DefaultDict[str, List[Portal]] = defaultdict(list)
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            loc = Coord(x, y)
            portal_or_entrance = val.isupper()
            if not portal_or_entrance:
                tile = Tile(val)
                m[loc] = tile
            else:
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

    # Start/end locations aren't actually portals, however parsing them from the
    # requries grid requires the same logic as portals
    # Remove and treat separately from now on
    assert len(portals[START_LABEL]) == 1
    assert len(portals[END_LABEL]) == 1
    start, end = (portals.pop(l)[0].location for l in (START_LABEL, END_LABEL))

    # Build PortalMap from intermediate portals dict
    pm = {}
    for label, (p1, p2) in portals.items():
        pm[p1.location] = (p1, p2)
        pm[p2.location] = (p2, p1)
    return Maze(m, pm, start, end)


def find_shortest_path_length(m: Maze) -> int:
    seen = set()
    q = [(0, m.start)]
    while q:
        dist, loc = heapq.heappop(q)
        seen.add(loc)
        if loc == m.end:
            return dist
        for next_loc in neighbours(loc):
            if next_loc in seen or m.tiles[next_loc] != Tile.OPEN:
                continue
            # Normal step
            heapq.heappush(q, (dist + 1, next_loc))
        if loc in m.portals:
            src, dest = m.portals[loc]
            if dest.location not in seen:
                # Teleport!
                heapq.heappush(q, (dist + 1, dest.location))

    raise RuntimeError(f"No path found from {m.start} -> {m.end}")


def part_1(grid: Grid) -> int:
    maze = parse_grid(grid)
    return find_shortest_path_length(maze)


def is_disabled(p: Portal, depth: int) -> bool:
    return p.outer if depth == 0 else False


def find_shortest_path_length_recursive_levels(m: Maze) -> int:
    """BFS again with the addition of tracking the *depth* at which a location has
    been visited.

    Portal behaviour:
    - Disabled portals treated as walls
    - Depth 0
        - All *outer* portals disabled
        - Inner portals increment depth (recurse into smaller maze)
    - Depth > 0
        - Outer portals decrement depth ('pop the stack' into the previous recursion)
        - Inner portals increment depth (recurse into smaller maze)
    - Terminate when depth 0 and location == ZZ
    """
    seen = set()
    q = [(0, 0, m.start)]
    while q:
        dist, depth, loc = heapq.heappop(q)
        seen.add((depth, loc))
        if depth == 0 and loc == m.end:
            return dist

        for next_loc in neighbours(loc):
            if (depth, next_loc) in seen or m.tiles[next_loc] != Tile.OPEN:
                continue
            # Normal step
            heapq.heappush(q, (dist + 1, depth, next_loc))

        if loc in m.portals:
            src, dest = m.portals[loc]
            if is_disabled(src, depth):
                continue
            # Inner portals recurse deeper
            # Outer portals 'pop' back previous level
            d = depth - 1 if dest.outer else depth + 1
            if (d, dest.location) not in seen:
                # Teleport!
                heapq.heappush(q, (dist + 1, d, dest.location))

    raise RuntimeError(f"No path found from {src} -> {dest}")


def part_2(grid: Grid) -> int:
    m = parse_grid(grid)
    return find_shortest_path_length_recursive_levels(m)


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
