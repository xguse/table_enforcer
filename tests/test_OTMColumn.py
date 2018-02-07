"""Test the unit: test_OTMColumn."""
from collections import OrderedDict
import re

import pytest
from .conftest import TEST_FILES

import pandas as pd
import numpy as np

from box import Box

import pytest

from table_enforcer import Column, OTMColumn, BaseColumn
from table_enforcer import validate as v
import table_enforcer.errors as e


@pytest.fixture()
def OTMColumn_df():
    return pd.read_csv(str(TEST_FILES / "test_OTMColumn.csv"))


bad_chars = re.compile(pattern="""[*(]""")


def no_bad_characters(series):
    """Validator"""

    def test(x):
        if bad_chars.search(x) is None:
            return True
        else:
            return False

    return series.astype(str).apply(test)


def fix_bad_characters(series):
    """Recoder"""

    def fix(x):
        return bad_chars.sub(repl='', string=x)

    return series.astype(str).apply(fix)


def recode_upper(series):
    return series.astype(str).str.upper()


def to_int(series):
    return series.astype(np.int)


def to_str(series):
    return series.astype(str)


col5_a = Column(
    name='col5_number',
    dtype=np.int,
    unique=False,
    validators=[
        v.funcs.not_null,
    ],
    recoders=[to_int],)

col5_b = Column(
    name='col5_word',
    dtype=str,
    unique=False,
    validators=[
        v.funcs.not_null,
        v.funcs.upper,
    ],
    recoders=[to_str, recode_upper],)


def split_on_colon(x):
    x = x.split(":")
    return {"col5_number": x[0], "col5_word": x[1]}


def sort_columns(df):
    return df.T.sort_index().T


@pytest.fixture()
def otmcolumn():
    col5 = OTMColumn(
        name='col5',
        unique=False,
        validators=[v.funcs.not_null, no_bad_characters],
        recoders=[fix_bad_characters],
        child_columns=[col5_a, col5_b],
        split_func=split_on_colon,)
    return col5


@pytest.fixture()
def enforcer(otmcolumn):
    col5 = OTMColumn(
        name='col5',
        unique=False,
        validators=[v.funcs.not_null, no_bad_characters],
        recoders=[fix_bad_characters],
        child_columns=[col5_a, col5_b],
        split_func=split_on_colon,)
    return col5


@pytest.mark.dev
def test_OTMColumn_init(otmcolumn):
    col5 = otmcolumn

    # test base class attrs
    assert col5.name == 'col5'
    assert col5.unique is False
    assert col5.dtype == str

    # test subclass attrs
    assert issubclass(col5.__class__, BaseColumn)
    assert isinstance(col5._child_columns, OrderedDict)
    assert list(col5._child_columns.keys()) == [col5_a.name, col5_b.name]
    assert col5._split_func == split_on_colon


@pytest.mark.dev
def test_OTMColumn_results(otmcolumn, OTMColumn_df, otmcolumn_valid_values):
    df = OTMColumn_df
    col5 = otmcolumn
    valids = otmcolumn_valid_values

    assert sort_columns(col5.validate(df.col5).reset_index()).equals(sort_columns(valids.validate_all))
    assert sort_columns(col5.validate_parent(df.col5)).equals(sort_columns(valids.validate_parent))


## Valid values serialized from Dev_OTMColumn.ipynb ##
validate_all_json = '''{"Validations":{"0":"col5","1":"col5","2":"col5","3":"col5_number","4":"col5_number","5":"col5_number","6":"col5_word","7":"col5_word","8":"col5_word"},"dtype":{"0":true,"1":true,"2":true,"3":false,"4":false,"5":false,"6":true,"7":true,"8":true},"no_bad_characters":{"0":false,"1":true,"2":true,"3":true,"4":true,"5":true,"6":true,"7":true,"8":true},"not_null":{"0":true,"1":true,"2":true,"3":true,"4":true,"5":true,"6":true,"7":true,"8":true},"upper":{"0":true,"1":true,"2":true,"3":true,"4":true,"5":true,"6":false,"7":false,"8":false}}'''
validate_parent_json = '''{"no_bad_characters":{"0":false,"1":true,"2":true},"not_null":{"0":true,"1":true,"2":true},"dtype":{"0":true,"1":true,"2":true}}'''


@pytest.fixture()
def otmcolumn_valid_values():
    vals = Box()
    vals.validate_all = pd.read_json(validate_all_json)
    vals.validate_parent = pd.read_json(validate_parent_json)
    return vals