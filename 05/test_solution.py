import pytest

from solution import parse_instruction


@pytest.mark.parametrize("inst,expected", [(1002, (2, [0, 1, 0])), (3, (3, [0, 0, 0]))])
def test_parse_instruction(inst, expected):
    assert parse_instruction(inst) == expected
