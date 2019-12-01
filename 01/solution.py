from math import floor
from typing import Iterable, List


def calc_fuel(m: int) -> int:
    return floor(m / 3) - 2


def part_1(module_masses: List[int]) -> int:
    return sum(calc_fuel(m) for m in module_masses)


def gen_fuel(m: int) -> Iterable[int]:
    m = calc_fuel(m)
    while m > 0:
        yield m
        m = calc_fuel(m)


def part_2(module_masses: List[int]) -> int:
    return sum(sum(gen_fuel(m)) for m in module_masses)


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    module_masses = [int(l) for l in lines]
    print("Part 1: ", part_1(module_masses))
    print("Part 2: ", part_2(module_masses))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
