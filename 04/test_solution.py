import pytest

from solution import is_valid, is_valid_p2


@pytest.mark.parametrize(
    "pw,valid", [("111111", True), ("223450", False), ("123789", False)]
)
def test_is_valid(pw, valid):
    assert is_valid(pw) == valid


@pytest.mark.parametrize(
    "pw,valid", [("112233", True), ("123444", False), ("111122", True)]
)
def test_is_valid_p2(pw, valid):
    assert is_valid_p2(pw) == valid
