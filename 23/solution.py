from collections import deque
from typing import List, NamedTuple, Optional, Deque

from intcode import IntCodeVM, Program, Status

NETWORK_SIZE = 50
NAT_ADDRESS = 255


class Packet(NamedTuple):
    destination: int
    x: int
    y: int


# TODO: Document!


class NetworkedIntcodeVM:
    def __init__(self, prg: Program, address: int, target_address: int, network: list):
        self.packet_queue: Deque[Packet] = deque([])
        self.vm = IntCodeVM(prg)
        self.address = address
        self.vm.input_val = address
        self.target_address = target_address
        self.network = network
        self.vm.execute_until_complete_or_input()
        self.vm.input_val = -1
        self.status = Status.IDLE

    def execute_until_io(self) -> Optional[Packet]:
        self.status = Status.RUNNING
        if not self.packet_queue:
            self.vm.input_val = -1
        else:
            self.vm.input_val = self.packet_queue[0].x
        dest_address = self.vm.execute_until_complete_or_io()
        assert self.vm.status != Status.COMPLETE
        if self.vm.status != Status.HALTED_ON_INPUT:
            self.status = Status.RUNNING
            x = self.vm.execute_until_complete_or_io()
            y = self.vm.execute_until_complete_or_io()
            assert dest_address and x and y
            packet = Packet(dest_address, x, y)
            if packet.destination == self.target_address:
                return packet
            self.network[dest_address].packet_queue.append(packet)
        else:
            if self.packet_queue:
                self.vm.input_val = self.packet_queue.popleft().y
                self.vm.execute_until_complete_or_input()
            else:
                self.status = Status.IDLE
        return None


Network = List[NetworkedIntcodeVM]


def init_network(prg: Program, n: int, nat_address: int) -> Network:
    network: List[NetworkedIntcodeVM] = []
    for address in range(n):
        network.append(NetworkedIntcodeVM(prg, address, nat_address, network))
    return network


def part_1(prg: Program):
    network = init_network(prg, NETWORK_SIZE, NAT_ADDRESS)
    while True:
        for pc in network:
            packet = pc.execute_until_io()
            if packet is not None and packet.destination == NAT_ADDRESS:
                return packet.y


class NAT:
    def __init__(self, network: Network):
        self.network = network

        self.current_packet: Optional[Packet] = None
        self.prev_packet: Optional[Packet] = None

    def recv(self, packet: Packet):
        self.current_packet = packet

    def poll(self) -> Optional[Packet]:
        if self.current_packet is not None and self._is_network_idle():
            if self._repeated_y():
                return self.current_packet
            else:
                self.prev_packet = None
            self.prev_packet = self.current_packet
            self.network[0].packet_queue.append((self.current_packet))
            self.current_packet = None
        return None

    def _repeated_y(self) -> bool:
        if self.current_packet is None or self.prev_packet is None:
            return False
        return self.current_packet.y == self.prev_packet.y

    def _is_network_idle(self) -> bool:
        return all(pc.status == Status.IDLE for pc in self.network)


def part_2(prg: Program):
    network = init_network(prg, NETWORK_SIZE, NAT_ADDRESS)
    nat = NAT(network)

    while True:
        for pc in network:
            packet = pc.execute_until_io()
            if packet is not None and packet.destination == NAT_ADDRESS:
                nat.recv(packet)
        p = nat.poll()
        if p is not None:
            return p.y


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
