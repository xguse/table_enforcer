"""Test the unit: Enforcer."""
from .conftest import enforcer
from table_enforcer import Column, Enforcer


def test_init(enforcer):
    assert isinstance(enforcer, Enforcer)

    cols = [isinstance(c, Column) for c in enforcer._columns.values()]
    assert all(cols)
