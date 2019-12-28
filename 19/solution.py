import asyncio
from itertools import count, product, tee
from typing import Tuple

from intcode import Memory, Program, execute, prg_to_memory


async def scanner(mem: Memory, size: int = 50):
    inqueue: asyncio.Queue[int] = asyncio.Queue()
    outqueue: asyncio.Queue[int] = asyncio.Queue()
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


async def find_gradients(mem: Memory, y=10000) -> Tuple[int, int]:
    """Approximate the gradients of the two enclosing lines of the tractor beam.

    Scans through x coordinates, running the drone program to determine whether
    that location is enclosed within the tractor beam. The x coordinates used
    to calculate gradients for the lower and upper lines are the x coordinate of
    the first and last locations within the beam respectively.

    Args:
        mem: Memory loaded with drone system Intcode program.
        y: Y coordinate to approximate gradients at
    Returns:
        Tuple of gradients m1, m2 of the lower and upper lines respectively.
    """
    inqueue: asyncio.Queue[int] = asyncio.Queue()
    outqueue: asyncio.Queue[int] = asyncio.Queue()
    enter_beam_x = None
    for x in count():
        # Run drone program to test whether this location is within the beam
        await inqueue.put(x)
        await inqueue.put(y)
        await asyncio.create_task(execute(mem.copy(), inqueue.get, outqueue.put))
        val = await outqueue.get()
        if enter_beam_x is None and val == 1:
            enter_beam_x = x
        elif enter_beam_x is not None and val == 0:
            # Previous location was the last in the beam at this y level
            exit_beam_x = x - 1
            # Calculate gradients
            return y / enter_beam_x, y / exit_beam_x
    # Given the known behaviour of the drone program, the above for loop *will*
    # always exit
    # This assert is to a) satisfy MyPy and b) ensure that an explicit failure
    # is triggered if these assumptions are incorrect
    assert False


def part_2(prg: Program) -> int:
    """
    Brute force iterating through the entire state space (as in part 1) will not
    work (at least within a reasonable amount of time) for part 2.

    The insight here is that *only* the corners of the target area need be known
    as within the tractor beam. More specifically, if the bottom left and top right
    corners are within the beam, then the whole are is within the beam.

    Given approximate gradients (m1, m2) of the lines enclosing the tractor beam, the
    coordinates of these points can be calculated *without* an exhaustive search
    and used to find the coordinates of the *top left* corner - thus leading to
    the answer.

    #----------------+......................
    |#...............|......................
    |.##.............|......................
    |..###...........|......................
    |...###..........|......................
    |....####........|......................
    |.....#####.m2...|......................
    |..m1.######.....|......................
    |......##OOB#....|.....................
    |.......#OOO###..|.....................
    |........AOO#####|.....................
    +---------#########.....................

    Here, the 3x3 square marked using A, B (for the two corners) and O's represent
    the ship area.

    Points A and B have coordinates (x1, x2) and (x2, y2) respectively.

    The lower enclosing line (closer to A) has gradient m1 and the upper enclosing
    line has gradient m2.

    Using good old y = mx + c:

    y1 = m1 * x1 [a]
    y2 = m2 * x2 [b]

    Given a square of width w:

    x1 = x2 - w [c]
    y1 = y2 + w [d]

    Rearrange [c] to isolate x2:

    x2 = x1 + w [e]

    Substituting [e] into [b]:

    y2 = m2 * (x1 + w) [f]

    Rearrange [b] to isolate x2:

    x2 = y2 / m2 [g]

    Rearrange [d] to isolate y2:
    y2 = y1 - w [h]

    Substitute [a] in [h]:

    y2 = m1 * x1 - w [i]

    Equate [i] and [f]:

    m1 * x1 - w = m2 * (x1 + w)
    m1 * x1 - w = m2 * x1 + m2 * w
    m1 * x1 = m2 * x1 + m2 * w + w
    m1 * x1 - m2 * x1 = m2 * w + w
    (m1 - m2) * x1 = m2 * w + w
    x1 = ((m2 * w) + w) / (m1 - m2) [j]

    Use [j] and [i] to calculate the x and y coordinates of the top left corner,
    then finish off as specified in the puzzle by multiplying the x coordinate
    by 10000 and adding the y coordinate.
    """
    mem = prg_to_memory(prg)
    m1, m2 = asyncio.run(find_gradients(mem))
    w = 99  # Square is 100 wide *including* the starting location
    x1 = round(((m2 * w) + w) / (m1 - m2))  # [j]
    y2 = round((m1 * x1) - w)  # [i]
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
