import asyncio
from typing import List

from intcode import Memory, Program, execute, prg_to_memory


class output_collector:
    def __init__(self):
        self.output: List[int] = []

    async def __call__(self, value: int):
        self.output.append(value)


async def stdout(val: int):
    try:
        s = chr(val)
    except ValueError:
        s = val
    print(s, end="")


async def droid(mem: Memory, script: List[str], out=stdout):
    inqueue: asyncio.Queue[int] = asyncio.Queue()
    for c in "\n".join(script) + "\n":
        await inqueue.put(ord(c))
    await asyncio.create_task(execute(mem, inqueue.get, out))


# TODO: Document this from notes
def part_1(prg: Program):
    mem = prg_to_memory(prg)
    c = output_collector()
    asyncio.run(droid(mem, ["NOT A T", "NOT C J", "AND D J", "OR T J", "WALK"], out=c))
    return c.output[-1]


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
