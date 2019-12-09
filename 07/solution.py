"""
Note: Intcode computer (`run` function) mostly copied from day 05 solution
"""
import itertools
from collections import deque
from enum import IntEnum
from typing import List, NamedTuple


class Mode(IntEnum):
    position = 0
    immediate = 1


class Instruction(NamedTuple):
    op: int
    modes: List[Mode]


# Note: 3 and 4 are special cases and handled within run
OPCODES = {
    1: lambda x, y: x + y,
    2: lambda x, y: x * y,
    5: lambda test, val: val if test != 0 else None,
    6: lambda test, val: val if test == 0 else None,
    7: lambda x, y: 1 if x < y else 0,
    8: lambda x, y: 1 if x == y else 0,
}


def parse_instruction(code) -> Instruction:
    op = code % 100
    inst = Instruction(op, [code // i % 10 for i in (100, 1000, 10000)])
    assert inst.modes[-1] == Mode.position
    return inst


# TODO: Clean this up! I'm not proud of this code, it's *certainly* not clean or elegant!
def run(prg, inqueue):
    ip = 0
    while True:
        inst = parse_instruction(prg[ip])

        if inst.op == 99:
            return prg
        elif inst.op == 3:
            prg[prg[ip + 1]] = inqueue.popleft()  # 'read' from input
            ip += 2
        elif inst.op == 4:
            yield prg[prg[ip + 1]]  # 'output' a value
            ip += 2
        else:
            # get params according to modes
            params = []
            for mode, val in zip(inst.modes, prg[ip + 1 : ip + 3]):
                if mode == Mode.position:
                    params.append(prg[val])
                elif mode == Mode.immediate:
                    params.append(val)
            if inst.op in (5, 6):
                jump_pos = OPCODES[inst.op](*params)
                if jump_pos is None:
                    ip += 3
                else:
                    ip = jump_pos
            else:
                # calculate result according to op
                result = OPCODES[inst.op](*params)
                # store result according to final mode
                prg[prg[ip + 3]] = result
                ip += 4
    return prg


class Amplifier:
    def __init__(self, name, prg, phase):
        self.inqueue = deque([phase])
        self.process = run(prg[:], self.inqueue)

    def __str__(self):
        return f"Amplifier {self.name}"

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.process)


def pairwise_circle(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ... (s<last>,s0)"
    a, b = itertools.tee(itertools.cycle(iterable))
    next(b)
    return zip(a, b)


def run_amps(prg, phases, init_val=0):
    amps = [Amplifier(i, prg, p) for i, p in enumerate(phases)]
    amps[0].inqueue.append(init_val)

    for amp, next_amp in pairwise_circle(amps):
        try:
            val = next(amp)
        except StopIteration:
            return val
        next_amp.inqueue.append(val)


def part_1(prg):
    return max(run_amps(prg, phases) for phases in itertools.permutations(range(5)))


def part_2(prg):
    return max(run_amps(prg, phases) for phases in itertools.permutations(range(5, 10)))


def main(puzzle_input_f):
    line = puzzle_input_f.read().strip()
    prg = [int(x) for x in line.split(",")]
    print("Part 1: ", part_1(prg[:]))  # copy to avoid mutation
    print("Part 2: ", part_2(prg[:]))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
