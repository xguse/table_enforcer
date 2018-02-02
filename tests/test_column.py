"""Test the unit: Enforcer."""
import pytest
from .conftest import col4, col4_no_recoders, source_table  # noqa: F401
import table_enforcer.errors as e


def test_init(col4):
    assert col4.name == 'col4'
    assert col4.dtype == str
    assert col4.unique == False  # noqa: E712


def test_column(col4, col4_no_recoders, source_table):
    assert sorted(["length_is_one", "upper", "valid_sex"]) == sorted(col4.validators.keys())

    col4.recode(series=source_table['col4'])
    col4.recode(series=source_table['col4'], validate=True)

    with pytest.raises(e.ValidationError):
        col4_no_recoders.recode(series=source_table['col4'], validate=True)

    assert sorted(["length_is_one", "upper", "valid_sex",
                   "dtype"]) == sorted(col4.validate(series=source_table['col4']).columns.values)
