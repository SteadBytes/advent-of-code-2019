import asyncio
from collections import deque
from typing import NamedTuple

from intcode import Memory, Program, execute, prg_to_memory


class Packet(NamedTuple):
    destination: int
    x: int
    y: int


# TODO: Document and refactor this
# TODO: Can 'inqueue_failed_attempts' counting be replaced by Packet tuples?
async def run_pcs(mem: Memory, on_finish, n: int = 50):
    lock = asyncio.Lock()
    conds = tuple(asyncio.Condition(lock) for _ in range(n))
    inqueues = tuple(deque((i,)) for i in range(n))
    inqueue_failed_attempts = {}

    async def go(mem, i):
        queue, cond = inqueues[i], conds[i]

        async def input():
            print(i, "input")
            async with lock:
                while True:
                    if queue:
                        inqueue_failed_attempts[i] = 0
                        v = queue.popleft()
                        print("pop", i, v)
                        return v
                    inqueue_failed_attempts[i] += 1
                    if inqueue_failed_attempts[i] <= 1:
                        print(i, -1)
                        return -1
                    elif not queue:
                        print(i, "waiting")
                        await cond.wait()

        p_buff = deque([])

        async def output(val):
            print(i, "output")
            async with lock:
                print(i, "buff", val)
                p_buff.append(val)
                inqueue_failed_attempts[i] = 0
            if len(p_buff) == 3:
                p = Packet(*p_buff)
                p_buff.clear()
                if p.destination == 255:
                    await on_finish(p)
                else:
                    async with lock:
                        print(p)
                        inqueues[p.destination].append(p.x)
                        inqueues[p.destination].append(p.y)
                        conds[p.destination].notify()

        asyncio.create_task(execute(mem, input, output))

    return [asyncio.create_task(go(mem.copy(), i)) for i in range(n)]


def part_1(prg: Program):
    mem = prg_to_memory(prg)

    async def main():
        result = asyncio.Queue()

        async def handle_dest_255(p: Packet):
            assert p.destination == 255
            await result.put(p.y)

        tasks = await run_pcs(mem, handle_dest_255)

        try:
            return await result.get()
        finally:
            for t in tasks:
                t.cancel()

    return asyncio.run(main())


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
