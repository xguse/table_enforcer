"""Test the unit: Enforcer."""
import pytest
from .conftest import enforcer, col4, col4_no_recoders, source_table
from table_enforcer.errors import ValidationError
from table_enforcer import Column, Enforcer


def test_init(enforcer):
    assert isinstance(enforcer, Enforcer)

    cols = [isinstance(c, Column) for c in enforcer._columns.values()]
    assert all(cols)
    assert all(cols)


def test_enforcer(col4, col4_no_recoders, source_table):
    enforcer_good = Enforcer(columns=[col4])
    enforcer_bad = Enforcer(columns=[col4_no_recoders])

    enforcer_good.recode(table=source_table)
    enforcer_good.recode(table=source_table, validate=True)

    with pytest.raises(ValidationError):
        enforcer_bad.recode(table=source_table, validate=True)