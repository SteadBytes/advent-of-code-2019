from functools import partial
from operator import eq, ge


def monotonic_inc(s: str):
    return list(s) == sorted(s)


def n_same(s: str, n: int, cmp):
    return any(cmp(c, n) for c in map(s.count, s))


def is_valid(pw, cmp=ge):
    return monotonic_inc(pw) and n_same(pw, 2, cmp)


is_valid_p2 = partial(is_valid, cmp=eq)


def count_valid(low, high, pred):
    return sum(1 for i in range(low, high) if pred(str(i)))


def part_1(low, high):
    return count_valid(low, high, is_valid)


def part_2(low, high):
    return count_valid(low, high, is_valid_p2)


def main(puzzle_input_f):
    low, high = [int(x) for x in puzzle_input_f.readline().strip().split("-")]
    print("Part 1: ", part_1(low, high))
    print("Part 2: ", part_2(low, high))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
