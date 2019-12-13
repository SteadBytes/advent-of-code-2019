from intcode import prg_to_memory, run, group_outputs


def part_1(prg: str):
    mem = prg_to_memory(prg)
    inqueue = []
    pc = run(mem, inqueue)
    tiles = {}
    for x, y, tile_id in group_outputs(pc, 3):
        tiles[(x, y)] = tile_id
    return sum(1 for v in tiles.values() if v == 2)


def part_2():
    pass


def main(puzzle_input_f):
    line = puzzle_input_f.read().strip()
    prg = [int(x) for x in line.split(",")]
    print("Part 1: ", part_1(prg[:]))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
