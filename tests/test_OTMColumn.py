"""Test the unit: test_OTMColumn."""
from collections import OrderedDict

import pytest
from .conftest import TEST_FILES

import pandas as pd
import numpy as np

import pytest

from table_enforcer import Column, OTMColumn, BaseColumn
from table_enforcer import validate as v
import table_enforcer.errors as e


@pytest.fixture()
def rcdrs_col5():
    return []


@pytest.fixture()
def vldrs_col5():
    return []


@pytest.fixture()
def rcdrs_col5_a():
    return []


@pytest.fixture()
def vldrs_col5_a():
    return []


@pytest.fixture()
def rcdrs_col5_b():
    return []


@pytest.fixture()
def vldrs_col5_b():
    return []


@pytest.fixture()
def OTMColumn_df():
    return pd.read_csv(str(TEST_FILES / "test_OTMColumn.csv"))


col5_a = Column(
    name='col5_number',
    dtype=np.int,
    unique=False,
    validators=[
        v.funcs.not_null,
    ],
    recoders=None,
)

col5_b = Column(
    name='col5_word',
    dtype=str,
    unique=False,
    validators=[
        v.funcs.not_null,
    ],
    recoders=None,
)


def split_on_colon(x):
    return x.split(":")


@pytest.mark.dev
def test_OTMColumn_init(OTMColumn_df):

    col5 = OTMColumn(
        name='col5',
        unique=False,
        validators=[v.funcs.not_null],
        recoders=None,
        child_columns=[col5_a, col5_b],
        split_func=split_on_colon,
    )

    # test base class attrs
    assert col5.name == 'col5'
    assert col5.unique is False
    assert col5.dtype == str

    # test subclass attrs
    assert issubclass(col5.__class__, BaseColumn)
    assert isinstance(col5._child_columns, OrderedDict)
    assert list(col5._child_columns.keys()) == [col5_a.name, col5_b.name]
    assert col5._split_func == split_on_colon
