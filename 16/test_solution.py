from itertools import islice

import pytest

from solution import fft, part_1


def test_fft():
    """
    4 phase example given in puzzle text.
    """
    signal = "12345678"
    g = fft(signal)
    assert list(islice(g, 4)) == ["48226158", "34040438", "03415518", "01029498"]


@pytest.mark.parametrize(
    "signal,expected",
    [
        ("80871224585914546619083218645595", "24176176"),
        ("19617804207202209144916044189917", "73745418"),
        ("69317163492948606335995924319873", "52432133"),
    ],
)
def test_part_1(signal, expected):
    assert part_1(signal) == expected
