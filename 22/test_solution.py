import pytest

from solution import (
    Technique,
    TechniqueApplication,
    cut,
    deal_into_new_stack,
    deal_with_increment,
    parse_input,
)


def test_parse_input():
    lines = [
        "deal with increment 7",
        "deal into new stack",
        "cut -2",
        "cut 5",
        "deal with increment 57",
    ]
    assert list(parse_input(lines)) == [
        TechniqueApplication(Technique.DEAL_WITH_INC, 7),
        TechniqueApplication(Technique.DEAL_INTO),
        TechniqueApplication(Technique.CUT, -2),
        TechniqueApplication(Technique.CUT, 5),
        TechniqueApplication(Technique.DEAL_WITH_INC, 57),
    ]


def test_deal_into_new_stack():
    assert deal_into_new_stack(list(range(10))) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


@pytest.mark.parametrize(
    "n,expected",
    [(3, [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]), (-4, [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])],
)
def test_cut(n, expected):
    assert cut(n, list(range(10))) == expected


def test_deal_with_increment():
    assert deal_with_increment(3, list(range(10))) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
