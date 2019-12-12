import math
import re
from itertools import combinations, count, islice
from typing import Iterable, List, NamedTuple


class Coord3d(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


class Moon(NamedTuple):
    pos: Coord3d
    vel: Coord3d


def velocity_component_change(pos1_component, pos2_component):
    return (pos1_component > pos2_component) - (pos1_component < pos2_component)


def calc_velocities(m1: Moon, m2: Moon):
    diffs = [velocity_component_change(c1, c2) for c1, c2 in zip(m1.pos, m2.pos)]
    return (
        Coord3d(*(c - d for c, d in zip(m1.vel, diffs))),
        Coord3d(*(c + d for c, d in zip(m2.vel, diffs))),
    )


def simulate_universe(moons: List[Moon]) -> Iterable[List[Moon]]:
    d = {i: m for i, m in enumerate(moons)}
    while True:
        # update velocities
        # loop over all *pairs* of moons
        for i, j in combinations(list(d.keys()), 2):
            m1, m2 = d[i], d[j]
            m1_vel, m2_vel = calc_velocities(m1, m2)
            d[i], d[j] = Moon(m1.pos, m1_vel), Moon(m2.pos, m2_vel)
        # update positions
        for i, m in d.items():
            # add velocity to each moon position
            d[i] = Moon(m.pos + m.vel, m.vel)
        yield list(d.values())


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)


def part_1(moons: List[Moon]):
    _moons = nth(simulate_universe(moons), 999)
    # calculate total energy -> sum(potential(m) * kinetic(m) for m in moons)
    return sum(sum(abs(c) for c in m.pos) * sum(abs(c) for c in m.vel) for m in _moons)


def lowest_common_multiple(x, y, *zs):
    if not zs:
        return x * y // math.gcd(x, y)
    else:
        return lowest_common_multiple(x, lowest_common_multiple(y, *zs))


def part_2(moons: List[Moon]):
    """
    Each x, y, z component changes independently in a cycle. The number of steps
    for the moons to reach their first state again is the lowest common denominator
    of the cycle lengths of each component.


    Note: I dropped the immutable 'Moon' abstraction here and switched to simple
    (though not preferable) mutable lists as maintaining the higher level of
    abstraction was taking too long. I may return and refactor this in the future.
    """
    component_cycle_lengths = {}
    for component in range(3):  # x, y, z
        # original component values
        start_plane = [m.pos[component] for m in moons]
        start_vels = [m.vel[component] for m in moons]

        # 'current' component values
        plane = start_plane[:]
        vels = start_vels[:]

        for step in count(1):
            for i, j in combinations(range(len(plane)), 2):
                diff = velocity_component_change(plane[i], plane[j])
                vels[i] -= diff
                vels[j] += diff
            for i, (p, v) in enumerate(zip(plane, vels)):
                plane[i] = p + v
            if plane == start_plane and vels == start_vels:
                component_cycle_lengths[component] = step
                break
    return lowest_common_multiple(*component_cycle_lengths.values())


def parse_input(lines: Iterable[str]) -> List[Coord3d]:
    return [
        Coord3d(*(int(m.group(1)) for m in re.finditer(r"=(-?\d+)", l))) for l in lines
    ]


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    moon_positions = parse_input(lines)
    moons = [Moon(p, Coord3d(0, 0, 0)) for p in moon_positions]
    print("Part 1: ", part_1(moons))
    print("Part 2: ", part_2(moons))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
