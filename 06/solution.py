from collections import defaultdict


def build_graph(orbits):
    g = defaultdict(set)
    for obj1, obj2 in orbits:
        g[obj1].add(obj2)
    return g


def count_orbits(g, root, depth=0):
    children = g[root]
    n_orbits = depth
    for obj in children:
        n_orbits += count_orbits(g, obj, depth + 1)
    return n_orbits


def part_1(g):
    return count_orbits(g, "COM")


def build_bidirected_graph(graph):
    bg = defaultdict(set)
    for root, children in graph.items():
        bg[root].update(children)
        for child in children:
            bg[child].add(root)
    return bg


def calculate_distances(g, root):
    distances = {}

    def bfs(root, depth=0):
        if root in distances:
            return
        distances[root] = depth
        for child in g[root]:
            bfs(child, depth + 1)

    bfs(root)
    return distances


def part_2(orbit_graph):
    # object "YOU" is orbiting and object "SAN" is orbiting (order doesn't matter)
    start, end = [x for x, y in orbit_graph.items() if y & {"SAN", "YOU"}]
    # distances to all nodes from start
    distances = calculate_distances(build_bidirected_graph(orbit_graph), start)
    return distances[end]


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    orbits = [l.split(")") for l in lines]
    orbit_graph = build_graph(orbits)
    print("Part 1: ", part_1(orbit_graph))
    print("Part 2: ", part_2(orbit_graph))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
