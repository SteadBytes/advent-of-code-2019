import re
from dataclasses import dataclass
from itertools import combinations
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


@dataclass
class Moon:
    pos: Coord3d
    vel: Coord3d


# TODO: Tidy this nastiness up!
def calc_velocities(m1: Moon, m2: Moon):
    if m1.pos.x == m2.pos.x:
        vel1_x = m1.vel.x
        vel2_x = m2.vel.x
    elif m1.pos.x > m2.pos.x:
        vel1_x = m1.vel.x - 1
        vel2_x = m2.vel.x + 1
    else:
        vel1_x = m1.vel.x + 1
        vel2_x = m2.vel.x - 1

    if m1.pos.y == m2.pos.y:
        vel1_y = m1.vel.y
        vel2_y = m2.vel.y
    elif m1.pos.y > m2.pos.y:
        vel1_y = m1.vel.y - 1
        vel2_y = m2.vel.y + 1
    else:
        vel1_y = m1.vel.y + 1
        vel2_y = m2.vel.y - 1

    if m1.pos.z == m2.pos.z:
        vel1_z = m1.vel.z
        vel2_z = m2.vel.z
    elif m1.pos.z > m2.pos.z:
        vel1_z = m1.vel.z - 1
        vel2_z = m2.vel.z + 1
    else:
        vel1_z = m1.vel.z + 1
        vel2_z = m2.vel.z - 1

    return Coord3d(vel1_x, vel1_y, vel1_z), Coord3d(vel2_x, vel2_y, vel2_z)


def part_1(moons: List[Moon]):
    for _ in range(1000):
        # update velocities
        # loop over all *pairs* of moons
        for m1, m2 in combinations(moons, 2):
            # TODO: How to do this without mutating Moon's?
            # (would allow Moon to be NamedTupe instead of dataclass)
            m1.vel, m2.vel = calc_velocities(m1, m2)
        # update positions
        for m in moons:
            # add velocity to each moon position
            m.pos += m.vel

    # calculate total energy -> sum(potential(m) * kinetic(m) for m in moons)
    return sum(sum(abs(c) for c in m.pos) * sum(abs(c) for c in m.vel) for m in moons)


def part_2():
    pass


def parse_input(lines: Iterable[str]) -> List[Coord3d]:
    return [
        Coord3d(*(int(m.group(1)) for m in re.finditer(r"=(-?\d+)", l))) for l in lines
    ]


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    moon_positions = parse_input(lines)
    moons = [Moon(p, Coord3d(0, 0, 0)) for p in moon_positions]
    print("Part 1: ", part_1(moons))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
