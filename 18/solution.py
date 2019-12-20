"""
There is a *unique* path from any pair of keys and starting point in the grid.
This solution uses a BFS to build a graph where nodes are entrances or keys
(referred to as Points of Interest) and edges represent the distance between nodes
and the keys required to traverse that path.

Then, perform Dijkstras shortest path algorithm over the graph where nodes (POIs)
are represented by (distance, starting point, keys gathered). The search halts
when keys gathered == number of keys on the grid.
"""
from collections import defaultdict
from heapq import heappop, heappush
from itertools import count
from typing import DefaultDict, Dict, FrozenSet, List, NamedTuple, Tuple


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


ENTRANCE = "@"
WALL = "#"

# Cannot move diagonally
MOVE_DIRS = [Coord(x=0, y=-1), Coord(x=1, y=0), Coord(x=0, y=1), Coord(x=-1, y=0)]

Grid = List[List[str]]
POIMap = Dict[str, Coord]
POIGraph = DefaultDict[str, Dict[str, Tuple[int, FrozenSet[str]]]]


def map_points_of_interest(grid: Grid) -> Tuple[POIMap, List[str]]:
    """
    Returns a map from points of interest (POIs) to coordinates and a
    list of entrance names.

    Where POIs are:
        - Entrances
        - Keys

    Entrances are named sequentially from 1 in the order they are found. For a
    grid containing a single entrance, the map will contain an entry for an
    entrance `"0"` and the list of entrance names will be `["0"]`

    """
    entrance_names = map(str, count())
    d, entrances = dict(), []
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val.isupper() or val in ".#":
                continue
            if val == ENTRANCE:
                entrance = next(entrance_names)
                entrances.append(entrance)
                d[entrance] = Coord(x, y)
            else:
                d[val] = Coord(x, y)
    return d, entrances


def build_graph(grid: Grid, poi_map: POIMap, entrances: List[str]) -> POIGraph:
    """
    Returns a graph where nodes are starting POIs and edges are the associated
    distance and *keys* crossed on the path to another key.

    i.e. `{"0": {"a": (10, frozenset({'b', 'd'}))}...}` shows that the path from
    the entrance `"0"` to the key `"a"` has a distance of `10` and crosses the
    locations of keys `b` and `d`.
    """

    def bfs(pos: Coord):
        q = [(pos, 0, ())]
        seen, paths = set(), dict()
        while q:
            p, dist, required_keys = q.pop(0)
            if p in seen:
                continue
            seen.add(p)
            pos_id = grid[p.y][p.x]
            # An unseen key or door
            if p != pos and pos_id in poi_map and pos_id not in entrances:
                paths[pos_id] = (dist, frozenset(required_keys))

            for diff in MOVE_DIRS:
                next_p = p + diff
                pos_id = grid[next_p.y][next_p.x]
                if pos_id != WALL:
                    q.append(
                        (
                            next_p,
                            dist + 1,
                            required_keys + (pos_id.lower(),)
                            if pos_id.isupper()  # Position is a door -> key is required
                            else required_keys,
                        )
                    )
        return paths

    g = defaultdict(dict)
    for pos_id, pos in poi_map.items():
        for k, v in bfs(pos).items():
            g[pos_id][k] = v

    return g


def find_shortest_path_distance(g: POIGraph, entrances: List[str], n_keys: int) -> int:
    """
    Perform Dijkstra's search algorithm to find the shorted path from the entrance(s)
    to collect all the keys on the grid.

    Search nodes are represented as tuples of distance, robot positions and keys
    gathered so far i.e. `(10, ("0", "1", "2", "t"), frozenset("t"))` means the
    current path has a distance of `10`, 4 robots (3 of which are at entrances
    and one is at key `"t"`) and the path has so far collected only key `"t"`.

    The search halts when the number of keys gathered so far is equal to the total
    number of keys on the grid.
    """
    # (distance, (robot positions, keys gathered so far))
    q = [(0, (tuple(entrances), frozenset()))]
    distances = dict()

    while q:
        dist, n = heappop(q)
        if n in distances:
            continue
        distances[n] = dist
        nodes, keys = n
        if len(keys) == n_keys:
            return dist  # Found all keys -> done!
        for i, start in enumerate(nodes):
            for pos_id, (dist_, keys_) in g[start].items():
                # next node has the same number of keys in the path (i.e. it's)
                # not a *worse* path and is not already on the current path
                if len(keys_ - keys) == 0 and pos_id not in keys:
                    heappush(
                        q,
                        (
                            dist + dist_,
                            (
                                nodes[:i] + (pos_id,) + nodes[i + 1 :],
                                keys | frozenset(pos_id),
                            ),
                        ),
                    )


def part_1(lines: List[str]):
    grid = [list(l) for l in lines]
    poi_map, entrances = map_points_of_interest(grid)
    assert len(entrances) == 1
    n_keys = len(poi_map.keys()) - 1  # account for entrance
    g = build_graph(grid, poi_map, entrances)
    return find_shortest_path_distance(g, entrances, n_keys)


def correct_grid_entrances(
    grid: Grid, entrance_location: Coord = Coord(40, 40)
) -> Grid:
    """
    Adjust the center entrance location of the grid according the 4 entrance
    specification in part two of the puzzle.
    """
    # ...    @.@
    # .@. -> .@.
    # ...    @.@

    diffs = (Coord(-1, -1), Coord(1, -1), Coord(-1, 1), Coord(1, 1))
    new_entrance_locations = [entrance_location + d for d in diffs]
    for p in new_entrance_locations:
        grid[p.y][p.x] = ENTRANCE

    # @.@    @#@
    # .@. -> ###
    # @.@    @#@

    diffs = (Coord(0, -1), Coord(-1, 0), Coord(1, 0), Coord(0, 1))
    new_walls = [entrance_location + d for d in diffs] + [entrance_location]
    for p in new_walls:
        grid[p.y][p.x] = WALL
    return grid


def part_2(lines: List[str]):
    grid = correct_grid_entrances([list(l) for l in lines])
    poi_map, entrances = map_points_of_interest(grid)
    assert len(entrances) == 4  # 0, 1, 2, 3
    n_keys = len(poi_map.keys()) - len(entrances)  # account for entrances
    g = build_graph(grid, poi_map, entrances)
    return find_shortest_path_distance(g, entrances, n_keys)


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2(lines))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
