import asyncio
from collections import defaultdict, deque
from enum import IntEnum
from typing import Deque, Iterable, NamedTuple

import intcode


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


class TileId(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class JoystickPosition(IntEnum):
    LEFT = -1
    NEUTRAL = 0
    RIGHT = 1


OutputBuffer = Deque[int]


def drain_buffer(buffer: OutputBuffer) -> Iterable[int]:
    while buffer:
        yield buffer.popleft()


def part_1(prg: intcode.Program):
    class TileMapper:
        def __init__(self):
            self.tiles = defaultdict(lambda: TileId.EMPTY)
            self.buffer = deque([])

        async def __call__(self, value):
            self.buffer.append(value)
            if len(self.buffer) == 3:
                self.process(*drain_buffer(self.buffer))
                assert not self.buffer

        def process(self, x: int, y: int, tile_id: int):
            self.tiles[Coord(x, y)] = tile_id

    mem = intcode.prg_to_memory(prg)
    s = TileMapper()
    asyncio.run(intcode.execute(mem, intcode.no_input, s))
    return sum(1 for v in s.tiles.values() if v == 2)


# TODO: Simulate the game output with curses?
def part_2(prg: intcode.Program):
    class Game:
        def __init__(self):
            self.tiles = defaultdict(lambda: TileId.EMPTY)
            self.score = 0
            self.paddle_pos: Coord = None
            self.ball_pos: Coord = None
            self.buffer: OutputBuffer = deque([])

        async def handle_output(self, value: int):
            self.buffer.append(value)
            if len(self.buffer) == 3:
                self.process(*drain_buffer(self.buffer))
                assert not self.buffer

        async def handle_input(self) -> JoystickPosition:
            if self.ball_pos is None or self.paddle_pos is None:
                return JoystickPosition.NEUTRAL

            if self.ball_pos.x == self.paddle_pos.x:
                return JoystickPosition.NEUTRAL

            return (
                JoystickPosition.LEFT
                if self.ball_pos.x < self.paddle_pos.x
                else JoystickPosition.RIGHT
            )

        def process(self, x: int, y: int, tile_id_or_score: int):
            if x == -1 and y == 0:
                self.score = tile_id_or_score
                return
            c = Coord(x, y)
            if tile_id_or_score == TileId.PADDLE:
                self.paddle_pos = c
            elif tile_id_or_score == TileId.BALL:
                self.ball_pos = c
            self.tiles[c] = tile_id_or_score

    mem = intcode.prg_to_memory(prg)
    mem[0] = 2  # play for free!

    g = Game()
    asyncio.run(intcode.execute(mem, g.handle_input, g.handle_output))
    return g.score


def main(puzzle_input_f):
    line = puzzle_input_f.read().strip()
    prg = [int(x) for x in line.split(",")]
    print("Part 1: ", part_1(prg[:]))
    print("Part 2: ", part_2(prg))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
