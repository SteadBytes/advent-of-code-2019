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


def part_1(prg: Program) -> int:
    """
    Observations obtained via experimentation with the droid program output:
    1. Jump distance = 4 tiles
    2. Surface contiains periodic holes e.g. ####.#####
    3. Surface contains some isolated tiles (islands) e.g. ###..#.####

    Insights:
    1. Register D holds the state of the *landing* tile (from observation 1) and
        therefore *must always be true for a successful jump
    2. The droid should (rather obviously) jump if the next tile is a hole.
        Therefore, it should jump if register A is false
    3. An 'island' is too large too jump over (5 tiles minimum). The droid must
        therefore jump *onto* the island and then jump according to insight 2 in
        order to traverse the island. It should therefore jump when register C
        is false as the island will be at register D (4 tiles away).

    Insight 1 (should not jump):

      @   D
    ###..#.####.####.#

    Insight 2 (should jump):

              @A  D
    ###..#.####.####.#

    Insight 3 (should jump):

     @  CD
    ###..#.####.####.#

    In terms of the droid registers, the above can be represented by the formula:

    J = (¬A ˅ ¬C) ^ D

    And can be translated into springscript as:

    NOT A T
    NOT C J
    AND D J
    OR T J
    """
    mem = prg_to_memory(prg)
    c = output_collector()
    asyncio.run(droid(mem, ["NOT A T", "NOT C J", "AND D J", "OR T J", "WALK"], out=c))
    return c.output[-1]


def part_2(prg: Program):
    """
    Observations obtained via experimentation with the droid program output:
    1. The 3 observations from part 1 remain
    2. To safely jump onto an island, the landing point of the subsequent jump
        must also be considered.
    3. Some islands may require a jump starting from one tile earlier than in part
        1.

    Insights:
    1. Insight 1 from part 1 remains
    2. Insight 2 from part 1 holds but with the additional constraint that register
        H must also be true to provide a succesful jump off the island
    3. From observation 3, a jump should also be made when register B is false

    Insight 2 (should jump):

      @  CD   H
    #####.##.##.#.###

    Insight 3 (should jump):

          @ B D
    #####.##.##.#.###

    Insight 1 (should jump, from part 1):

              @A  D
    #####.##.##.#.###


    In terms f the droid registers, the above can be represented by the formula:

    J = (¬A ˅ (¬C ^ H) ˅ ¬B) ^ D

    And can be translated into springscript as:

    NOT C J
    AND D J
    AND H J
    NOT B T
    AND D T
    OR T J
    NOT A T
    OR T J
    RUN
    """
    mem = prg_to_memory(prg)
    c = output_collector()
    asyncio.run(
        droid(
            mem,
            [
                "NOT C J",
                "AND D J",
                "AND H J",
                "NOT B T",
                "AND D T",
                "OR T J",
                "NOT A T",
                "OR T J",
                "RUN",
            ],
            out=c,
        )
    )
    return c.output[-1]


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
