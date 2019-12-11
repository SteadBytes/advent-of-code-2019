import math
from collections import defaultdict
from itertools import chain, islice, zip_longest
from math import gcd
from typing import Dict, Iterable, List, NamedTuple


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x + y for x, y in zip(self, other)))

    def __sub__(self, other):
        assert len(other) == len(self)
        return self.__class__(*(x - y for x, y in zip(self, other)))


class Vector(NamedTuple):
    dx: float
    dy: float


Asteroid = Coord

AsteroidVectorMap = Dict[Vector, List[Asteroid]]


def build_asteroid_vector_map(
    source: Asteroid, asteroids: List[Asteroid]
) -> AsteroidVectorMap:
    """
    Returns a `dict` mapping `Vector`s from `source` to `list`s of `Asteroid`s
    sorted by distance.
    """
    asteroid_distances_by_vector = defaultdict(list)
    for asteroid in filter(lambda asteroid: asteroid != source, asteroids):
        dx, dy = asteroid - source
        dist = gcd(abs(dx), abs(dy))
        vec = Vector(dx / dist, dy / dist)
        asteroid_distances_by_vector[vec].append((dist, asteroid))
    return {
        k: [asteroid for dist, asteroid in sorted(v)]
        for k, v in asteroid_distances_by_vector.items()
    }


def station_vector_map(asteroids: List[Asteroid]) -> AsteroidVectorMap:
    """
    Returns the `AsteroidVectorMap` for the asteroid at which the monitoring
    station should be placed (with the most other asteroids in line of sight)
    """
    return max(
        (build_asteroid_vector_map(candidate, asteroids) for candidate in asteroids),
        key=len,
    )


def vector_degrees(v: Vector) -> float:
    """
    Convert a `Vector` into degrees from 0-360
    """
    return (math.degrees(math.atan2(v.dy, v.dx)) + 90) % 360


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)


def target_order(station_vector_map: AsteroidVectorMap) -> Iterable[Asteroid]:
    """
    Iterable of asteroids in the order which the station will vaporise them
    with it's giant laser.
    """
    clockwise_vectors = sorted(station_vector_map.keys(), key=vector_degrees)
    # lists of targets sorted by distance for each vector
    clockwise_target_lists = (station_vector_map[v] for v in clockwise_vectors)
    # iterable of the first elements of each sorted target list
    targets = chain.from_iterable(zip_longest(*clockwise_target_lists))
    # remove None's introduced by zip_longest
    return (c for c in targets if c is not None)


def part_1(asteroids: List[Asteroid]) -> int:
    return len(station_vector_map(asteroids))


def part_2(asteroids: List[Asteroid]) -> int:
    m = station_vector_map(asteroids)
    t = nth(target_order(m), 199)
    return t.x * 100 + t.y


def parse_input(lines: Iterable[str]) -> List[Asteroid]:
    return [
        Coord(x, y)
        for y, row in enumerate(lines)
        for x, val in enumerate(row)
        if val == "#"
    ]


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    asteroids = parse_input(lines)
    print("Part 1: ", part_1(asteroids))
    print("Part 2: ", part_2(asteroids))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
