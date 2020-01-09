import asyncio
import pickle
from itertools import combinations
from typing import Iterable, List, Set

from intcode import (
    DebugCommands,
    Memory,
    Program,
    execute,
    prg_to_memory,
    stdin,
    stdout,
)


async def interactive_droid(mem: Memory, **kwargs):
    asyncio.create_task(execute(mem, stdin(), stdout, **kwargs))


def as_intcode(instruction: str):
    assert instruction[-1] != "\n"
    return map(ord, instruction + "\n")


async def auto_droid(
    mem: Memory, instructions: List[str], stop_on_exhausted_instructions=False, **kwargs
):
    inqueue = asyncio.Queue()

    for inst in instructions:
        for x in as_intcode(inst):
            await inqueue.put(x)

    s = stdin()

    async def inp():
        if inqueue.empty():
            if stop_on_exhausted_instructions:
                return DebugCommands.IMMEDIATE_EXIT
            else:
                return await s()
        else:
            return await inqueue.get()

    return asyncio.create_task(execute(mem, inp, stdout, **kwargs))


def item_combinations(items: List[str]) -> Iterable[Set[str]]:
    for n in range(len(items)):
        yield set(combinations(items, n + 1))


def drop_cmds(items: Iterable[str]) -> List[str]:
    return [f"drop {i}" for i in items]


# TODO: Document
async def run_drop(mem: Memory, items: Iterable[str], **kwargs):
    inqueue = asyncio.Queue()

    for inst in drop_cmds(items) + ["north"]:
        for x in as_intcode(inst):
            await inqueue.put(x)

    outq = []

    async def outp(val: int):
        if inqueue.empty():
            outq.append(val)

    async def inp():
        if inqueue.empty():
            return DebugCommands.IMMEDIATE_EXIT
        else:
            return await inqueue.get()

    t = asyncio.create_task(execute(mem, inp, outp, **kwargs))
    await t

    return "".join(chr(x) for x in outq)


# TODO: Document
def part_1(prg: Program):
    mem = prg_to_memory(prg)

    # 'Manually" constructed path using `interactive_droid` to collect all 'good'
    # items, ending at the Securtity Checkpoint
    instructions = [
        "west",
        "south",
        "south",
        "south",
        "take asterisk",
        "north",
        "north",
        "north",
        "west",
        "west",
        "west",
        "take dark matter",
        "east",
        "south",
        "take fixed point",
        "west",
        "take food ration",
        "east",
        "north",
        "east",
        "south",
        "take astronaut ice cream",
        "south",
        "take polygon",
        "east",
        "take easter egg",
        "east",
        "take weather machine",
        "north",
    ]

    # Again, 'manually' constructed - the droid will hold all of these items
    # after the above instructions are executed
    items = {
        "polygon",
        "fixed point",
        "astronaut ice cream",
        "easter egg",
        "dark matter",
        "food ration",
        "asterisk",
        "weather machine",
    }

    # 'Snapshot' of VM state at the Security Checkpoint w/ all items
    # Could pickle this and save to a file for 'real' snapshots
    checkpoint_mem, ip, rel_base = asyncio.run(
        auto_droid(mem.copy(), instructions, stop_on_exhausted_instructions=True)
    ).result()
    assert checkpoint_mem != mem

    for to_keep in item_combinations(items):
        res = asyncio.run(
            run_drop(
                checkpoint_mem.copy(),
                items.difference(to_keep),
                ip=ip,
                rel_base=rel_base,
            )
        )
        if "Alert!" not in res:
            return res


def part_2(prg: Program):
    pass


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
