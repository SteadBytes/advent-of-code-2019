from collections import defaultdict
from enum import Enum, IntEnum
from typing import Callable, Coroutine, DefaultDict, List, NamedTuple

# TODO: Re-structure codebase to allow this to be imported properly instead of symlinked

Program = List[int]
Memory = DefaultDict[int, int]


class DebugCommands(Enum):
    IMMEDIATE_EXIT = 0


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
    inst = Instruction(op, [Mode(code // i % 10) for i in (100, 1000, 10000)])
    assert inst.modes[-1] in (Mode.POSITION, Mode.RELATIVE)
    return inst


def prg_to_memory(prg: Program) -> Memory:
    return defaultdict(int, enumerate(prg))


async def no_input():
    """
    Used as a `read_in` argument to `execute` when the caller expects the program
    to receive *no* input.

    Raises:
        RuntimeError: If awaited.
    """
    raise RuntimeError("Program was not expected to require input")


class stdin:
    def __init__(self):
        self._input_iter = self._input()

    async def __call__(self):
        return next(self._input_iter)

    def _input(self):
        while True:
            s = input()
            yield from map(ord, s + "\n")


async def stdout(val: int):
    try:
        s = chr(val)
    except ValueError:
        s = val
    print(s, end="")


async def execute(
    mem: Memory,
    read_in: Callable[[], Coroutine[None, None, int]],
    write_out: Callable[[int], Coroutine],
    ip: int = 0,
    rel_base: int = 0,
):
    """Intcode 'VM' entrypoint. Executes a program 'loaded' into memory (`mem`).

    Args:
        mem : Memory containing an Intcode program. Note: Can be combined with
              `ip` and `rel_base` args to start the VM from a 'snapshot'. These
              values are returned from the VM when `DebugCommands.IMMEDIAT_EXIT`
              is received as input.
        read_in: Callable providing a coro which returns the next instruction
            (an `int`) to the running machine when awaited
        write_out: Callable to receive program outputs (more `int`s)
        ip: Instruction pointer, provide specific value when re-starting the VM
            from a known state (default 0)
        rel_base: Relative base provide specific value when re-starting the VM
            from a known state (default 0)
    """

    def read(inst: Instruction, param: int):
        assert param >= 1
        addr = {
            Mode.POSITION: mem[ip + param],
            Mode.IMMEDIATE: ip + param,
            Mode.RELATIVE: rel_base + mem[ip + param],
        }[inst.modes[param - 1]]
        return mem[addr]

    def write(inst: Instruction, param: int, val: int):
        assert param >= 1
        addr = {
            Mode.POSITION: mem[ip + param],
            Mode.RELATIVE: rel_base + mem[ip + param],
        }[inst.modes[param - 1]]
        mem[addr] = val

    while True:
        assert ip >= 0

        inst = parse_instruction(mem[ip])

        if inst.op == OpCodes.STOP:
            return
        elif inst.op == OpCodes.ADD:
            write(inst, 3, read(inst, 1) + read(inst, 2))
            ip += 4
        elif inst.op == OpCodes.MUL:
            write(inst, 3, read(inst, 1) * read(inst, 2))
            ip += 4
        elif inst.op == OpCodes.INPUT:
            val = await read_in()
            if val is DebugCommands.IMMEDIATE_EXIT:
                # Return 'snapshot' of VM state for debugging
                return mem, ip, rel_base
            write(inst, 1, val)
            ip += 2
        elif inst.op == OpCodes.OUTPUT:
            await write_out(read(inst, 1))
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
