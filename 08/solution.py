import itertools
from collections import Counter


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def parse_layers(image_data, width=25, height=6):
    layer_len = width * height
    return grouper(image_data, layer_len)


def part_1(layers):
    counts = (Counter(l) for l in layers)
    target = min(counts, key=lambda c: c["0"])
    return target["1"] * target["2"]


def part_2():
    pass


def main(puzzle_input_f):
    image_data = puzzle_input_f.read().strip()
    layers = list(parse_layers(image_data))
    print("Part 1: ", part_1(layers))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
