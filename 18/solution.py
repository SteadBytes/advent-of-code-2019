from collections import defaultdict
from operator import add
from heapq import heappop, heappush

ENTRANCE = "@"

# cannot move diagonally
Y_DIRS = [-1, 0, 1, 0]
X_DIRS = [0, 1, 0, -1]


def map_keys_from_entrance(grid):
    d = dict()
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val.islower() or val == ENTRANCE:
                d[val] = (y, x)
    return d


def part_1(lines):
    """
    There is a *unique* path from any pair of keys and starting point in the grid.
    Use a BFS to build a graph where nodes are starting points (entrance or key)
    and edges representing distance and doors crossed along that path.

    Then, perform Dijkstras shortest path algorithm over the graph where nodes
    (entrance or key) are represented by (distance, starting point, keys gathered).
    The search halts when keys gathered == number of keys on the grid.
    """
    grid = [list(l) for l in lines]
    d = map_keys_from_entrance(grid)
    entrance_location = d[ENTRANCE]
    n_keys = len(d.keys()) - 1  # account for entrance

    def bfs(pos):
        q = [(pos, 0, ())]
        seen, paths = set(), dict()
        while q:
            p, dist, doors = q.pop(0)
            if p in seen:
                continue
            seen.add(p)

            pos_id = grid[p[0]][p[1]]
            # this is a key
            if pos_id in d and p not in (pos, entrance_location):
                paths[pos_id] = (dist, frozenset(doors))

            for diff in zip(Y_DIRS, X_DIRS):
                next_p = tuple(map(add, p, diff))
                pos_id = grid[next_p[0]][next_p[1]]
                if pos_id != "#":
                    q.append(
                        (
                            next_p,
                            dist + 1,
                            doors + (pos_id.lower(),) if pos_id.isupper() else doors,
                        )
                    )
        return paths

    g = defaultdict(dict)
    for pos_id, pos in d.items():
        for k, v in bfs(pos).items():
            g[pos_id][k] = v

    # (distance, (starting point, doors crossed so far))
    q = [(0, (ENTRANCE, frozenset()))]
    distances = dict()

    while q:
        dist, n = heappop(q)
        if n in distances:
            continue
        distances[n] = dist
        start, doors = n
        if len(doors) == n_keys:
            return dist  # done!
        for pos_id, (dist_, doors_) in g[start].items():
            # next node has the same number of keys in the path
            # and is not on the current path
            if len(doors_ - doors) == 0 and pos_id not in doors:
                heappush(q, (dist + dist_, (v, doors | frozenset(v))))


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
