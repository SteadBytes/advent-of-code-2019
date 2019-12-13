from collections import defaultdict, deque
from enum import IntEnum
from itertools import zip_longest
from typing import DefaultDict, NamedTuple

from intcode import prg_to_memory, run


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


class PanelColour(IntEnum):
    BLACK = 0
    WHITE = 1


class Rotation(IntEnum):
    LEFT = 0
    RIGHT = 1


# UP, RIGHT, DOWN, LEFT
MOVE_DIRECTIONS = [Coord(0, -1), Coord(1, 0), Coord(0, 1), Coord(-1, 0)]


def run_robot(
    prg: str, start_colour: PanelColour = PanelColour.WHITE
) -> DefaultDict[Coord, PanelColour]:
    mem = prg_to_memory(prg)
    panels = defaultdict(int)
    pos = Coord(0, 0)
    panels[pos] = start_colour
    dir_idx = 0
    inqueue = deque([start_colour])
    idx_change = {Rotation.LEFT: -1, Rotation.RIGHT: 1}
    pc = run(mem, inqueue)
    for colour, rotation in zip(pc, pc):
        panels[pos] = colour
        dir_idx = (dir_idx + idx_change[rotation]) % len(MOVE_DIRECTIONS)
        pos += MOVE_DIRECTIONS[dir_idx]
        inqueue.append(panels[pos])
    return panels


def part_1(prg: str) -> int:
    panels = run_robot(prg)
    return len(panels)


# map 0/1 to unicode black/white squares for more easily readable output
PIXEL_MAP = {0: "\u2591", 1: "\u2588"}


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def part_2(prg: str):
    panels = run_robot(prg, start_colour=1)
    width = max(panels, key=lambda c: c.x).x + 1  # account for 0 based index
    height = max(panels, key=lambda c: c.y).y + 1
    image = ((panels[(x, y)] for x in range(width)) for y in range(height))
    return "\n".join("".join(PIXEL_MAP[p] for p in row) for row in image)


def main(puzzle_input_f):
    line = puzzle_input_f.read().strip()
    prg = [int(x) for x in line.split(",")]
    print("Part 1: ", part_1(prg[:]))
    print(f"Part 2: \n{part_2(prg)}")


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
