"""
Simpler re-implementation of the Intcode VM *without asyncio* as using asyncio
made solving today's puzzle overly complex. I may refactor previous solutions to
use this (or similar) implementation as in hindsight the asyncio VM is not a
great implementation.
"""
from collections import defaultdict
from enum import Enum, IntEnum
from typing import DefaultDict, List, NamedTuple, Optional

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


class Status(Enum):
    NOT_STARTED = 0
    COMPLETE = 1
    RUNNING = 2
    HALTED_ON_INPUT = 3
    HALTED_ON_OUTPUT = 4
    IDLE = 5
    INTERRUPTED = 6


class VMSnapshot(NamedTuple):
    mem: Memory
    ip: int
    rel_base: int


class IntCodeVM:
    def __init__(self, prg: Program, input_val: int = 0):
        self.mem: Memory = prg_to_memory(prg)
        self.input_val: int = input_val
        self.output: Optional[int] = None
        self.status: Status = Status.NOT_STARTED

        self._ip: int = 0
        self._rel_base: int = 0

    @staticmethod
    def from_snapshot(snapshot: VMSnapshot) -> "IntCodeVM":
        vm = IntCodeVM([0])  # Dummy program
        vm.mem = snapshot.mem
        vm._ip = snapshot.ip
        vm._rel_base = snapshot.rel_base
        return vm

    def to_snapshot(self) -> VMSnapshot:
        return VMSnapshot(self.mem.copy(), self._ip, self._rel_base)

    def execute_until_complete_or_input(self) -> Optional[int]:
        return self.execute(halt_on_input=True, halt_on_output=False)

    def execute_until_complete_or_io(self) -> Optional[int]:
        return self.execute(halt_on_input=True, halt_on_output=True)

    def execute(
        self, halt_on_input: bool = False, halt_on_output: bool = False
    ) -> Optional[int]:
        self.status = Status.RUNNING
        while True:
            assert self._ip >= 0

            inst = parse_instruction(self.mem[self._ip])

            if inst.op == OpCodes.STOP:
                self.status = Status.COMPLETE
                return None
            elif inst.op == OpCodes.ADD:
                self._write(inst, 3, self._read(inst, 1) + self._read(inst, 2))
                self._ip += 4
            elif inst.op == OpCodes.MUL:
                self._write(inst, 3, self._read(inst, 1) * self._read(inst, 2))
                self._ip += 4
            elif inst.op == OpCodes.INPUT:
                assert self.input_val is not None
                if self.input_val == DebugCommands.IMMEDIATE_EXIT:
                    # TODO: Should this prevent execute from being run again?
                    self.status = Status.INTERRUPTED
                    return None
                self._write(inst, 1, self.input_val)
                self._ip += 2
                if halt_on_input:
                    self.status = Status.HALTED_ON_INPUT
                    break
            elif inst.op == OpCodes.OUTPUT:
                self.output = self._read(inst, 1)
                self._ip += 2
                if halt_on_output:
                    self.status = Status.HALTED_ON_OUTPUT
                    break
            elif inst.op == OpCodes.JUMP_IF_TRUE:
                if self._read(inst, 1):
                    self._ip = self._read(inst, 2)
                else:
                    self._ip += 3
            elif inst.op == OpCodes.JUMP_IF_FALSE:
                if not self._read(inst, 1):
                    self._ip = self._read(inst, 2)
                else:
                    self._ip += 3
            elif inst.op == OpCodes.LT:
                self._write(
                    inst, 3, 1 if self._read(inst, 1) < self._read(inst, 2) else 0
                )
                self._ip += 4
            elif inst.op == OpCodes.EQ:
                self._write(
                    inst, 3, 1 if self._read(inst, 1) == self._read(inst, 2) else 0
                )
                self._ip += 4
            elif inst.op == OpCodes.SET_REL_BASE:
                self._rel_base += self._read(inst, 1)
                self._ip += 2
            else:
                raise RuntimeError(f"Invalid opcode {inst.op}")
        return self.output

    def _read(self, inst: Instruction, param: int) -> int:
        assert param >= 1
        addr = {
            Mode.POSITION: self.mem[self._ip + param],
            Mode.IMMEDIATE: self._ip + param,
            Mode.RELATIVE: self._rel_base + self.mem[self._ip + param],
        }[inst.modes[param - 1]]
        return self.mem[addr]

    def _write(self, inst: Instruction, param: int, val: int):
        assert param >= 1
        addr = {
            Mode.POSITION: self.mem[self._ip + param],
            Mode.RELATIVE: self._rel_base + self.mem[self._ip + param],
        }[inst.modes[param - 1]]
        self.mem[addr] = val
