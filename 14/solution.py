from collections import defaultdict


def parse_chemical(s: str):
    n, chemical = s.split(" ")
    return int(n), chemical


def parse_reaction(s: str):
    l, r = s.split(" => ")
    output = parse_chemical(r)
    inputs = (parse_chemical(c) for c in l.split(", "))
    return tuple(inputs), output


def parse_input(lines):
    return {
        out_chemical: (out_quant, inputs)
        for inputs, (out_quant, out_chemical) in (parse_reaction(l) for l in lines)
    }


def part_1(lines):
    # build mapping from outputs to input requirements
    m = parse_input(lines)

    required = {"FUEL": 1}
    current = defaultdict(int)

    while True:
        try:
            next_chemical = next(filter(lambda c: c != "ORE", required))
        except StopIteration:
            # done when no chemicals are still required
            return required["ORE"]

        out_quant, inputs = m[next_chemical]
        n_consume, n_remaining = divmod(required[next_chemical], out_quant)

        if n_remaining != 0:
            # have enough to make this chemical
            current[next_chemical] = out_quant - n_remaining
            n_consume += 1

        # next_chemical will be 'made' by this reaction
        del required[next_chemical]

        # calculate input chemical requirements for this reaction
        for in_quant, in_chemical in inputs:
            required[in_chemical] = (
                # total required for next_chemical
                in_quant * n_consume
                # total *already* required from previous reactions
                + required.get(in_chemical, 0)
                # account for chemical already available
                - current[in_chemical]
            )
            # in_chemical 'used up' by this reaction
            del current[in_chemical]


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
