from collections import defaultdict


def count_orbits(g, root, depth=0):
    children = g[root]
    n_orbits = depth
    for obj in children:
        n_orbits += count_orbits(g, obj, depth + 1)
    return n_orbits


def part_1(orbits):
    g = defaultdict(list)
    for obj1, obj2 in orbits:
        g[obj1].append(obj2)
    return count_orbits(g, "COM")


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    orbits = [l.split(")") for l in lines]
    print("Part 1: ", part_1(orbits))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
