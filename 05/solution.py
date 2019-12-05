import operator
from enum import IntEnum
from functools import reduce
from typing import List, NamedTuple


class Mode(IntEnum):
    position = 0
    immediate = 1


class Instruction(NamedTuple):
    op: int
    modes: List[Mode]


# Note: 3 and 4 are special cases and handled within run
OPCODES = {
    1: lambda xs: reduce(operator.add, xs),
    2: lambda xs: reduce(operator.mul, xs),
}


def parse_instruction(code) -> Instruction:
    op = code % 100
    inst = Instruction(op, [code // i % 10 for i in (100, 1000, 10000)])
    assert inst.modes[-1] == Mode.position
    return inst


def run(prg):
    ip = 0
    while True:
        inst = parse_instruction(prg[ip])

        if inst.op == 99:
            return prg
        elif inst.op == 3:
            prg[prg[ip + 1]] = 1  # Always input 1 as specified in puzzle
            ip += 2
        elif inst.op == 4:
            print(prg[prg[ip + 1]])
            ip += 2
        else:
            # get params according to modes
            params = []
            for mode, val in zip(inst.modes, prg[ip + 1 : ip + 3]):
                if mode == Mode.position:
                    params.append(prg[val])
                elif mode == Mode.immediate:
                    params.append(val)
            # calculate result according to op
            result = OPCODES[inst.op](params)
            # store result according to final mode
            prg[prg[ip + 3]] = result
            ip += 4
    return prg


def part_1(prg):
    run(prg)


def part_2(prg):
    pass


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
