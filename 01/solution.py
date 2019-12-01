from math import floor


def part_1(module_masses):
    return sum(floor(m / 3) - 2 for m in module_masses)


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    module_masses = [int(l) for l in lines]
    print("Part 1: ", part_1(module_masses))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
