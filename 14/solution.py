import math
from collections import defaultdict
from typing import Iterable, Dict, Tuple

# TODO: Try this in clojure core.logic


ChemicalQuant = Tuple[int, str]
ReactionResult = ChemicalQuant
ReactionRequirement = Tuple[ChemicalQuant, ...]
Reaction = Tuple[ReactionResult, ReactionRequirement]
ReactionsGraph = Dict[str, Reaction]


def parse_chemical(s: str) -> ChemicalQuant:
    n, chemical = s.split(" ")
    return int(n), chemical


def parse_reaction(s: str) -> Reaction:
    l, s = s.split(" => ")
    output = parse_chemical(s)
    inputs = (parse_chemical(c) for c in l.split(", "))
    return tuple(inputs), output


def parse_input(lines: Iterable[str]) -> ReactionsGraph:
    return {
        out_chemical: (out_quant, inputs)
        for inputs, (out_quant, out_chemical) in (parse_reaction(l) for l in lines)
    }


def ore_required(g: ReactionsGraph, n_fuel: int) -> int:
    required = {"FUEL": n_fuel}
    current = defaultdict(int)

    while True:
        try:
            next_chemical = next(filter(lambda c: c != "ORE", required))
        except StopIteration:
            # done when no chemicals are still required
            return required["ORE"]

        out_quant, inputs = g[next_chemical]
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


def part_1(lines: Iterable[str]) -> int:
    reaction_graph = parse_input(lines)
    return ore_required(reaction_graph, 1)


def part_2(lines: Iterable[str]) -> int:
    """
    Given x ore produces y fuel, 10**12 ore produces >= (f * 10**1) / x

    `max_fuel` uses this approximation to find the maximum fuel that can be made
    from 10**12 ore:
    """
    reaction_graph = parse_input(lines)

    target = 10 ** 12

    def max_fuel(fuel=1) -> int:
        # ore for the *next* amount of fuel
        ore = ore_required(reaction_graph, fuel + 1)
        # base case: *next* amount of fuel is too much -> return previous
        if ore > target:
            return fuel
        else:
            # calculate next fuel value and recur
            return max_fuel(math.floor((fuel + 1) * target / ore))

    return max_fuel()


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2(lines))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
