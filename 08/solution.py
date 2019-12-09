import itertools
from collections import Counter
from typing import Iterable, List

Layers = Iterable[str]


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def parse_layers(image_data: str, width: int, height: int) -> Layers:
    layer_len = width * height
    return grouper(image_data, layer_len)


def part_1(image_data: str, width=25, height=6) -> int:
    layers = parse_layers(image_data, width, height)
    counts = (Counter(l) for l in layers)
    target = min(counts, key=lambda c: c["0"])
    return target["1"] * target["2"]


def build_image_matrix(layers: Layers, width: int) -> List[List[str]]:
    layer_rows = (grouper(l, width) for l in layers)
    d = {}
    for layer in layer_rows:
        for row, pixels in enumerate(layer):
            for col, pixel in enumerate(pixels):
                if (row, col) in d:
                    continue
                elif pixel in "01":
                    d[(row, col)] = pixel
    return [[p[1] for p in row] for row in grouper(sorted(d.items()), width)]


# map '0'/1' to unicode black/white squares for more easily readable output
PIXEL_MAP = {"0": "\u2588", "1": "\u2591"}


def part_2(image_data: str, width: int = 25, height: int = 6) -> str:
    layers = parse_layers(image_data, width, height)
    image = build_image_matrix(layers, width)
    return "\n".join("".join(PIXEL_MAP[p] for p in r) for r in image)


def main(puzzle_input_f):
    image_data = puzzle_input_f.read().strip()
    print("Part 1: ", part_1(image_data))
    print(f"Part 2: \n{part_2(image_data)}")


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
