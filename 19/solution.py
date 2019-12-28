import asyncio
from itertools import count, product, tee
from typing import Tuple

from intcode import Memory, Program, execute, prg_to_memory


async def scanner(mem: Memory, size: int = 50):
    inqueue = asyncio.Queue()
    outqueue = asyncio.Queue()
    for x, y in product(*tee(range(size))):
        await inqueue.put(x)
        await inqueue.put(y)
        await asyncio.create_task(execute(mem.copy(), inqueue.get, outqueue.put))
        yield x, y, await outqueue.get()


async def affected_points(scanner):
    return sum([val async for x, y, val in scanner])


def part_1(prg: Program):
    mem = prg_to_memory(prg)
    scan = scanner(mem)
    return asyncio.run(affected_points(scan))


# TODO: Document part 2 solution from notes made on paper!
async def find_gradients(mem: Memory, y=10000) -> Tuple[int, int]:
    inqueue = asyncio.Queue()
    outqueue = asyncio.Queue()
    enter_beam_x = None
    for x in count():
        await inqueue.put(x)
        await inqueue.put(y)
        await asyncio.create_task(execute(mem.copy(), inqueue.get, outqueue.put))
        val = await outqueue.get()
        if enter_beam_x is None and val == 1:
            enter_beam_x = x
        elif enter_beam_x is not None and val == 0:
            exit_beam_x = x - 1
            return y / enter_beam_x, y / exit_beam_x


def part_2(prg: Program):
    mem = prg_to_memory(prg)
    m1, m2 = asyncio.run(find_gradients(mem))
    w = 99
    x1 = round(((m2 * w) + w) / (m1 - m2))
    y2 = round((m1 * x1) - w)
    return (x1 * 10000) + y2


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
