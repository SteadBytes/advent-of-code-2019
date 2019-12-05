import pytest

from solution import is_valid


@pytest.mark.parametrize(
    "pw,valid", [("111111", True), ("223450", False), ("123789", False)]
)
def test_is_valid(pw, valid):
    assert is_valid(pw) == valid
