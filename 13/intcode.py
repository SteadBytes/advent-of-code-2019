"""
Intcode computer copied from day 09
"""
from collections import defaultdict, deque
from enum import IntEnum
from typing import DefaultDict, List, NamedTuple

Memory = DefaultDict[int, int]


class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Instruction(NamedTuple):
    op: int
    modes: List[Mode]


class OpCodes(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LT = 7
    EQ = 8
    SET_REL_BASE = 9
    STOP = 99


def parse_instruction(code: int) -> Instruction:
    op = code % 100
    inst = Instruction(op, [code // i % 10 for i in (100, 1000, 10000)])
    assert inst.modes[-1] in (Mode.POSITION, Mode.RELATIVE)
    return inst


# TODO: Are do_read/do_write worth extracting like this? i.e. am I writing isolated\
# unit tests for them :P


def do_read(mem: dict, ip: int, rel_base: int, inst: Instruction, param: int):
    assert param >= 1
    addr = {
        Mode.POSITION: mem[ip + param],
        Mode.IMMEDIATE: ip + param,
        Mode.RELATIVE: rel_base + mem[ip + param],
    }[inst.modes[param - 1]]
    return mem[addr]


def do_write(
    mem: dict, ip: int, rel_base: int, inst: Instruction, param: int, val: int
):
    assert param >= 1
    addr = {Mode.POSITION: mem[ip + param], Mode.RELATIVE: rel_base + mem[ip + param]}[
        inst.modes[param - 1]
    ]
    mem[addr] = val


def prg_to_memory(prg: List[int]) -> Memory:
    return defaultdict(int, enumerate(prg))


def run(mem: Memory, inqueue: deque):
    ip = rel_base = 0

    def read(inst: Instruction, param: int):
        return do_read(mem, ip, rel_base, inst, param)

    def write(inst: Instruction, param: int, val: int):
        return do_write(mem, ip, rel_base, inst, param, val)

    while True:
        assert ip >= 0

        inst = parse_instruction(mem[ip])

        if inst.op == OpCodes.STOP:
            return mem
        elif inst.op == OpCodes.ADD:
            write(inst, 3, read(inst, 1) + read(inst, 2))
            ip += 4
        elif inst.op == OpCodes.MUL:
            write(inst, 3, read(inst, 1) * read(inst, 2))
            ip += 4
        elif inst.op == OpCodes.INPUT:
            write(inst, 1, inqueue.popleft())
            ip += 2
        elif inst.op == OpCodes.OUTPUT:
            yield read(inst, 1)
            ip += 2
        elif inst.op == OpCodes.JUMP_IF_TRUE:
            if read(inst, 1):
                ip = read(inst, 2)
            else:
                ip += 3
        elif inst.op == OpCodes.JUMP_IF_FALSE:
            if not read(inst, 1):
                ip = read(inst, 2)
            else:
                ip += 3
        elif inst.op == OpCodes.LT:
            write(inst, 3, 1 if read(inst, 1) < read(inst, 2) else 0)
            ip += 4
        elif inst.op == OpCodes.EQ:
            write(inst, 3, 1 if read(inst, 1) == read(inst, 2) else 0)
            ip += 4
        elif inst.op == OpCodes.SET_REL_BASE:
            rel_base += read(inst, 1)
            ip += 2
        else:
            raise RuntimeError(f"Invalid opcode {inst.op}")


def group_outputs(pc, n):
    return zip(*(pc for _ in range(n)))
