import re
from enum import Enum
from heapq import heappop, heappush
from typing import Iterable, List, NamedTuple, Optional, Tuple


class Technique(Enum):
    DEAL_INTO = 0
    CUT = 1
    DEAL_WITH_INC = 2


class TechniqueApplication(NamedTuple):
    technique: Technique
    n: Optional[int] = None


ShuffleProcess = Iterable[TechniqueApplication]


def deal_into_new_stack(s):
    return list(reversed(s))


def cut(n: int, s):
    assert n < len(s)
    return s[n:] + s[:n]


def deal_with_increment(n: int, s):
    # Heap sort using *destination* indexes as the key
    h: List[Tuple[int, int]] = []
    for i, val in enumerate(s):
        j = (n * i) % len(s)  # Calculate destination index
        heappush(h, (j, val))
    return [heappop(h)[1] for _ in range(len(h))]


TECHNIQUE_FUNCS = {
    Technique.DEAL_INTO: lambda t, s: deal_into_new_stack(s),
    Technique.DEAL_WITH_INC: lambda t, s: deal_with_increment(t.n, s),
    Technique.CUT: lambda t, s: cut(t.n, s),
}


def parse_input(lines: Iterable[str]) -> ShuffleProcess:
    for l in lines:
        m = re.search(r"(-?\d+)$", l)
        if m is None:
            yield TechniqueApplication(Technique.DEAL_INTO)
        else:
            n = int(m.group(1))
            t = Technique.DEAL_WITH_INC if l.startswith("deal") else Technique.CUT
            yield TechniqueApplication(t, n)


def part_1(sp: ShuffleProcess):
    cards = list(range(10007))
    for app in sp:
        cards = TECHNIQUE_FUNCS[app.technique](app, cards)
    return cards.index(2019)


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    sp = parse_input(lines)
    print("Part 1: ", part_1(sp))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
