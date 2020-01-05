from enum import IntEnum
from functools import partial
from itertools import chain, islice, product
from operator import ne
from typing import Iterable, Set, Tuple

SIZE = 5  # Fixed size given in puzzle specification
AREA = SIZE * SIZE  # Assuming square
CENTER = (SIZE // 2, SIZE // 2)
EMPTY_TILE = "."
INFESTED_TILE = "#"

Grid = int


def to_str(g: Grid) -> str:
    tile_map = {"0": EMPTY_TILE, "1": INFESTED_TILE}
    s = format(g, f"0{AREA}b")[::-1]
    rows = (s[i : i + SIZE] for i in range(0, AREA, SIZE))
    return "\n".join("".join(tile_map[t] for t in row) for row in rows)


def nth_bit(x: int, n: int) -> int:
    """
    Returns the bit value at position `n` in binary representation of `x`.

    Examples:
        >>> nth_bit(0, 0)
        0
        >>> nth_bit(1, 0)
        1
        >>> nth_bit(2, 1)
        1
        >>> nth_bit(256, 8)
        1
        >>> nth_bit(62, 1)
        1
    """
    return (x >> n) & 1


def coord_bit(x: int, y: int):
    """
    Returns the bit position in the binary represenation of a grid corresponding
    to the (x, y) location in the cartesian representation of a grid.

    Examples:
        >>> coord_bit(0, 0)
        0
        >>> coord_bit(4, 4)
        24
        >>> coord_bit(4, 0)
        4
        >>> coord_bit(0, 1)
        5
        >>> coord_bit(4, 1)
        9
        >>> coord_bit(2, 2)
        12
    """
    return x + SIZE * y


def bit_coord(n: int) -> Tuple[int, int]:
    """
    Returns the (x, y) location in the cartesian representation of a grid given 
    the bit position in the binary represenation of a grid.

    Examples:
        >>> bit_coord(0)
        (0, 0)
        >>> bit_coord(24)
        (4, 4)
        >>> bit_coord(4)
        (4, 0)
        >>> bit_coord(5)
        (0, 1)
        >>> bit_coord(9)
        (4, 1)
        >>> bit_coord(12)
        (2, 2)
    """
    return divmod(n, SIZE)[::-1]


def get_coord_bit(g: Grid, x: int, y: int) -> int:
    return nth_bit(g, coord_bit(x, y))


def simulate_xy(g: Grid) -> Iterable[Grid]:
    """
    Same functionality as `simulate`, but implemented by converting cartesian
    coordinates to bit positions explicitly in the code to provide another
    understanding of the approach taken to solving this problem.

    Drop-in (though slightly less efficient) replacement for `simulate`.
    """
    while True:
        next_grid = 0
        for x, y in product(range(SIZE), range(SIZE)):
            adj_bugs = 0
            # Check left if not on leftmost column
            if x != 0:
                adj_bugs += get_coord_bit(g, x - 1, y)

            # Check right if not on rightmost column
            if x != SIZE - 1:
                adj_bugs += get_coord_bit(g, x + 1, y)

            # Check up if not on top row
            if y != 0:
                adj_bugs += get_coord_bit(g, x, y - 1)

            # Check down if not on bottom row
            if y != SIZE - 1:
                adj_bugs += get_coord_bit(g, x, y + 1)

            current_bug = get_coord_bit(g, x, y)
            # Any tile (infested or not) w/exactly 1 adjacent bug will be infested
            # in the next grid. Else, empty tiles woll be infested if they have
            # exactly 2 adjacent bugs
            should_infest = adj_bugs == 1 or (not current_bug and adj_bugs == 2)
            if should_infest:
                # Set current tile as infested and 'fill in' empty tiles in
                # between this and the previously set tile
                next_grid |= 1 << coord_bit(x, y)
        g = next_grid
        yield g


def simulate(g: Grid) -> Iterable[Grid]:
    """
    Simulate the bug cellular automata, yielding layouts after each time step
    starting from initial state `g`.
    """
    while True:
        next_grid = 0
        for i in range(AREA):
            adj_bugs = 0

            # Check left if not on leftmost column
            if i % SIZE:
                adj_bugs += nth_bit(g, i - 1)

            # Check right if not on rightmost column
            if i % SIZE != SIZE - 1:
                adj_bugs += nth_bit(g, i + 1)

            # Check up if not on top row
            if i >= SIZE:
                adj_bugs += nth_bit(g, i - 5)

            # Check down if not on bottom row
            if i < AREA - SIZE:
                adj_bugs += nth_bit(g, i + 5)

            current_bug = nth_bit(g, i)
            # Any tile (infested or not) w/exactly 1 adjacent bug will be infested
            # in the next grid. Else, empty tiles woll be infested if they have
            # exactly 2 adjacent bugs
            should_infest = adj_bugs == 1 or (not current_bug and adj_bugs == 2)
            if should_infest:
                # Set current tile as infested and 'fill in' empty tiles in
                # between this and the previously set tile
                next_grid |= 1 << i
        g = next_grid
        yield g


def part_1(g: Grid) -> int:
    print(f"Start grid:\n{to_str(g)}")
    seen: Set[Grid] = set()
    for next_grid in simulate(g):
        if next_grid in seen:
            print(f"Repeated grid:\n{to_str(next_grid)}")
            return next_grid
        seen.add(next_grid)
    raise RuntimeError("No repeated grid layout found")


# TODO: Does this need IntEnum?
class GridRelation(IntEnum):
    """
    Values correspond to index offsets used in `simulate_recursive_grids_xy` to
    access the corresponding grid given the current grid index.
    """

    OUTER = 0
    CURRENT = 1
    INNER = 2


def adjacent_coords(x: int, y: int) -> Iterable[Tuple[GridRelation, int, int]]:
    neighbours = ((x + dx, y + dy) for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)))
    for x_, y_ in neighbours:
        if x_ < 0:
            # Outer left edge
            yield (GridRelation.OUTER, 1, 2)
        elif x_ >= SIZE:
            # Outer right edge
            yield (GridRelation.OUTER, 3, 2)
        elif y_ < 0:
            # Outer top edge
            yield (GridRelation.OUTER, 2, 1)
        elif y_ >= SIZE:
            # Outer bottom edge
            yield (GridRelation.OUTER, 2, 3)
        elif (x_, y_) == CENTER:
            c_x, c_y = CENTER
            if x == c_x and y == c_y - 1:
                # Top center adjacent
                yield from ((GridRelation.INNER, ix, 0) for ix in range(SIZE))
            elif x == c_x and y == c_y + 1:
                # Bottom center adjacent
                yield from ((GridRelation.INNER, ix, 4) for ix in range(SIZE))
            elif x == c_x - 1 and y == c_y:
                # Left center adjacent
                yield from ((GridRelation.INNER, 0, iy) for iy in range(SIZE))
            elif x == c_x + 1 and y == c_y:
                # Right center adjacent
                yield from ((GridRelation.INNER, 4, iy) for iy in range(SIZE))
        else:
            yield (GridRelation.CURRENT, x_, y_)


not_center = partial(ne, CENTER)


# TODO: Pure bit manipulation version (same as `simulate`)
def simulate_recursive_grids_xy(g: Grid):
    levels = [0, 0, g, 0, 0]
    while True:
        next_levels = [0, 0]
        # Iterate over previously seen levels + 1 new above & 1 new below
        for i, grid in enumerate(levels[1:-1]):
            next_grid = 0
            # Centre leads into next level
            for x, y in filter(not_center, product(range(SIZE), range(SIZE))):
                adj_bugs = sum(
                    get_coord_bit(levels[i + g_type], x_, y_)
                    for g_type, x_, y_ in adjacent_coords(x, y)
                )
                current_bug = get_coord_bit(grid, x, y)
                # Any tile (infested or not) w/exactly 1 adjacent bug will be infested
                # in the next grid. Else, empty tiles woll be infested if they have
                # exactly 2 adjacent bugs
                should_infest = adj_bugs == 1 or (not current_bug and adj_bugs == 2)
                if should_infest:
                    # Set current tile as infested and 'fill in' empty tiles in
                    # between this and the previously set tile
                    next_grid |= 1 << coord_bit(x, y)
            next_levels.append(next_grid)
        next_levels += [0, 0]
        yield next_levels
        levels = next_levels


def part_2(g: Grid) -> int:
    """
    See part-2-notes.pdf for (not quite) beautiful hand written notes.
    """
    sim = simulate_recursive_grids_xy(g)
    return sum(bin(g).count("1") for g in next(islice(sim, 199, None)))


def parse_input(lines: Iterable[str]) -> Grid:
    """
    Parse grid input into an integer representation - directly corresponding to
    the *biodiversity rating*.

    0
    v
    ##.#.    24                      0
    ##.#.    v                       v
    ##.## -> 0001011110110110101101011
    .####
    .#...
        ^
        24
    """
    grid = 0
    for i, tile in enumerate(chain.from_iterable(lines)):
        if tile == INFESTED_TILE:
            grid += 1 << i
    return grid


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    grid = parse_input(lines)
    print("Part 1: ", part_1(grid))
    print("Part 2: ", part_2(grid))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
