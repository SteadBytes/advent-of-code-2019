from intcode import group_outputs, prg_to_memory, run


def part_1(prg: str):
    mem = prg_to_memory(prg)
    inqueue = []
    pc = run(mem, inqueue)
    tiles = {}
    for x, y, tile_id in group_outputs(pc, 3):
        tiles[(x, y)] = tile_id
    return sum(1 for v in tiles.values() if v == 2)


# TODO: Simulate the game output with curses?
def part_2(prg: str):
    mem = prg_to_memory(prg)
    mem[0] = 2  # play for free!
    ball_x = paddle_x = 0

    def joystick_position():
        if ball_x == paddle_x:
            return 0
        else:
            return -1 if ball_x < paddle_x else 1

    pc = run(mem, joystick_position)
    score = 0
    for x, y, tile_id in group_outputs(pc, 3):
        if x == -1 and y == 0:
            score = tile_id
        elif tile_id == 3:
            paddle_x = x
        elif tile_id == 4:
            ball_x = x
    return score


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
