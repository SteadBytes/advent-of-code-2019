from itertools import chain, cycle, islice, tee
from typing import Iterable


BASE_PATTERN = [0, 1, 0, -1]


def ones_digit(x):
    return x % (-10 if x < 0 else 10)


def fft(signal: str) -> Iterable[str]:
    """
    Infinite generator yielding successive phases of fft algorithm
    """
    out = []
    for out_index in range(1, len(signal) + 1):
        # repeat each value in pattern according to position in output
        pattern = chain(*([x] * out_index for x in BASE_PATTERN))
        p1, p2 = tee(pattern)
        repeated_pattern = chain(
            islice(p1, 1, None),  # skip first value *once*
            cycle(p2),  # repeat full pattern for the rest
        )
        digits = (int(c) for c in signal)
        vals = (ones_digit(digit * x) for digit, x in zip(digits, repeated_pattern))
        out.append(abs(ones_digit(sum(vals))))
    next_signal = "".join(str(x) for x in out)
    yield next_signal
    yield from fft(next_signal)


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)


def part_1(signal: str):
    return nth(fft(signal), 99)[:8]


def part_2():
    pass


def main(puzzle_input_f):
    signal = puzzle_input_f.read().strip()
    print("Part 1: ", part_1(signal))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
