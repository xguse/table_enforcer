"""Test the unit: Enforcer."""

from .conftest import col4  # noqa: F401


def test_init(col4):
    assert col4.name == 'col4'
    assert col4.dtype == str
    assert col4.unique == False  # noqa: E712
