def monotonic_inc(s: str):
    return list(s) == sorted(s)


def at_least_n_same(s: str, n: int):
    return any(c >= n for c in map(s.count, s))


def is_valid(pw):
    return monotonic_inc(pw) and at_least_n_same(pw, 2)


def part_1(low, high):
    return sum(1 for i in range(low, high) if is_valid(str(i)))


def part_2():
    pass


def main(puzzle_input_f):
    low, high = [int(x) for x in puzzle_input_f.readline().strip().split("-")]
    print("Part 1: ", part_1(low, high))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
