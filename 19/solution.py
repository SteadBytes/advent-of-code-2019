import asyncio
from itertools import product, tee

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


def part_2():
    pass


def main(puzzle_input_f):
    line = puzzle_input_f.read().strip()
    prg = [int(x) for x in line.split(",")]
    print("Part 1: ", part_1(prg[:]))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
