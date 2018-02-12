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


def sort_columns(df):
    return df.T.sort_index().T


# Validators and Recoders
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


def split_on_colon(df):
    cols = Box()
    cols.col5_number = df.col5.apply(lambda x: x.split(":")[0])
    cols.col5_word = df.col5.apply(lambda x: x.split(":")[1])

    new_columns = pd.DataFrame(cols)[["col5_number", "col5_word"]]
    return new_columns


# Defining the Input Column
@pytest.fixture()
def col5():
    return Column(
        name='col5',
        dtype=str,
        unique=False,
        validators=[
            v.funcs.not_null,
            no_bad_characters,
        ],
        recoders=[fix_bad_characters])


# Defining the Output Columns (col5_a/col5_b)
@pytest.fixture()
def col5_a():
    return Column(
        name='col5_number',
        dtype=np.int,
        unique=False,
        validators=[
            v.funcs.not_null,
        ],
        recoders=[to_int],)


@pytest.fixture()
def col5_b():
    return Column(
        name='col5_word',
        dtype=str,
        unique=False,
        validators=[
            v.funcs.not_null,
            v.funcs.upper,
            no_bad_characters,
        ],
        recoders=[to_str, recode_upper],)


@pytest.fixture()
def OTMColumn_df():
    return pd.read_csv(str(TEST_FILES / "test_OTMColumn.csv"))


@pytest.fixture()
def col5_split(col5, col5_a, col5_b):
    return OTMColumn(input_columns=[col5], output_columns=[col5_a, col5_b], column_transform=split_on_colon)


# @pytest.fixture()
# def enforcer(otmcolumn):
#     col5 = OTMColumn(
#         name='col5',
#         unique=False,
#         validators=[v.funcs.not_null, no_bad_characters],
#         recoders=[fix_bad_characters],
#         child_columns=[col5_a, col5_b],
#         split_func=split_on_colon,)
#     return col5


@pytest.mark.otmc
def test_OTMColumn_init(col5_split, col5, col5_a, col5_b):
    assert col5_split.input_columns == [col5]
    assert col5_split.output_columns == [col5_a, col5_b]
    assert col5_split.column_transform == split_on_colon

    assert issubclass(col5_split.__class__, BaseColumn)
    assert all([isinstance(c, Column) for c in col5_split.input_columns])
    assert all([isinstance(c, Column) for c in col5_split.output_columns])


@pytest.mark.otmc
def test_OTMColumn_results(col5_split, OTMColumn_df, otmcolumn_valid_values):
    df = OTMColumn_df
    valids = otmcolumn_valid_values

    assert sort_columns(col5_split.validate(df).reset_index()).equals(sort_columns(valids.validate_all))
    assert sort_columns(col5_split._validate_input(df).reset_index()).equals(sort_columns(valids.validate_input))
    assert sort_columns(col5_split._validate_output(df).reset_index()).equals(sort_columns(valids.validate_output))


## Valid values serialized from Dev_OTMColumn.ipynb ##
validate_all_json = '''{"validation_type":{"0":"input","1":"input","2":"input","3":"output","4":"output","5":"output","6":"output","7":"output","8":"output"},"column_name":{"0":"col5","1":"col5","2":"col5","3":"col5_number","4":"col5_number","5":"col5_number","6":"col5_word","7":"col5_word","8":"col5_word"},"row":{"0":0,"1":1,"2":2,"3":0,"4":1,"5":2,"6":0,"7":1,"8":2},"dtype":{"0":true,"1":true,"2":true,"3":false,"4":false,"5":false,"6":true,"7":true,"8":true},"no_bad_characters":{"0":false,"1":true,"2":true,"3":true,"4":true,"5":true,"6":false,"7":true,"8":true},"not_null":{"0":true,"1":true,"2":true,"3":true,"4":true,"5":true,"6":true,"7":true,"8":true},"upper":{"0":true,"1":true,"2":true,"3":true,"4":true,"5":true,"6":false,"7":false,"8":false}}'''
validate_input_json = '''{"validation_type":{"0":"input","1":"input","2":"input"},"column_name":{"0":"col5","1":"col5","2":"col5"},"row":{"0":0,"1":1,"2":2},"no_bad_characters":{"0":false,"1":true,"2":true},"not_null":{"0":true,"1":true,"2":true},"dtype":{"0":true,"1":true,"2":true}}'''
validate_output_json = '''{"validation_type":{"0":"output","1":"output","2":"output","3":"output","4":"output","5":"output"},"column_name":{"0":"col5_number","1":"col5_number","2":"col5_number","3":"col5_word","4":"col5_word","5":"col5_word"},"row":{"0":0,"1":1,"2":2,"3":0,"4":1,"5":2},"dtype":{"0":false,"1":false,"2":false,"3":true,"4":true,"5":true},"no_bad_characters":{"0":null,"1":null,"2":null,"3":false,"4":true,"5":true},"not_null":{"0":true,"1":true,"2":true,"3":true,"4":true,"5":true},"upper":{"0":null,"1":null,"2":null,"3":false,"4":false,"5":false}}'''


@pytest.fixture()
def otmcolumn_valid_values():
    vals = Box()
    vals.validate_all = pd.read_json(validate_all_json)
    vals.validate_input = pd.read_json(validate_input_json)
    vals.validate_output = pd.read_json(validate_output_json)
    return vals