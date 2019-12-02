import operator
from itertools import product

OPCODES = {
    1: operator.add,
    2: operator.mul
}


def run(prg):
    ip = 0
    while True:
        op = prg[ip]
        if op == 99:
            break
        p1, p2, p3 = prg[ip+1:ip + 4]
        x, y = prg[p1], prg[p2]
        prg[p3] = OPCODES[op](x, y)
        ip += 4
    return prg


def part_1(prg):
    prg[1], prg[2] = 12, 2
    return run(prg)[0]


def part_2(prg):
    for x2, x1 in product(range(100), range(100)):
        _prg = prg[:]
        _prg[1], _prg[2] = x1, x2
        if run(_prg)[0] == 19690720:
            return 100 * x1 + x2


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
