"""Test the unit: test_MTOColumn."""
from collections import OrderedDict

import pytest
from .conftest import demo_good_df, sort_columns

import pandas as pd
import numpy as np

from box import Box

from table_enforcer import Column, CompoundColumn, BaseColumn
from table_enforcer import validate as v
import table_enforcer.errors as e


# helper functions
def is_subset(x, ref_set):
    if not isinstance(ref_set, set):
        valid = set(ref_set)

    if not isinstance(x, set):
        set_x = set([x])
    else:
        set_x = x

    return set_x.issubset(ref_set)


# Transformation function
def join_as_tuple(df):
    cols = Box()
    cols.col6_7_8 = df[["col6", "col7", "col8"]].apply(
        lambda row: (
            row.col6,
            row.col7,
            row.col8,), axis=1)

    new_columns = pd.DataFrame(cols)
    return new_columns


# Validators
def col6_valid_values(series):
    """Validator"""
    valid = [None, "DNASeq"]
    return series.apply(is_subset, ref_set=valid)


def col7_valid_values(series):
    """Validator"""
    valid = [None, "Protein Function"]
    return series.apply(is_subset, ref_set=valid)


def col8_valid_values(series):
    """Validator"""
    valid = [None, "RNASeq"]
    return series.apply(is_subset, ref_set=valid)


def col6_7_8_valid_values(series):
    """Validator"""
    valid = set(["DNASeq", "Protein Function", "RNASeq"])
    return series.apply(is_subset, ref_set=valid)


# Recoders
def translate_col6(series):
    """Recode 0-> None; 1-> 'DNASeq' """

    def rcode(x):
        mapping = {0: None, 1: "DNASeq"}
        return mapping[x]

    return series.apply(rcode)


def translate_col7(series):
    """Recode 0-> None; 1-> 'Protein Function' """

    def rcode(x):
        mapping = {0: None, 1: "Protein Function"}
        return mapping[x]

    return series.apply(rcode)


def translate_col8(series):
    """Recode 0-> None; 1-> 'RNASeq' """

    def rcode(x):
        mapping = {0: None, 1: "RNASeq"}
        return mapping[x]

    return series.apply(rcode)


def setify_drop_nones(series):
    """Convert to sets and drop ``None`` values."""

    def drop_nones(x):
        x.discard(None)
        return x

    return series.apply(lambda x: set(x)).apply(drop_nones)


# Defining the Input Columns
@pytest.fixture()
def col6():
    return Column(
        name='col6',
        dtype=(str, type(None)),
        unique=False,
        validators=[col6_valid_values],
        recoders=[translate_col6],
    )


@pytest.fixture()
def col7():
    return Column(
        name='col7',
        dtype=(str, type(None)),
        unique=False,
        validators=[col7_valid_values],
        recoders=[translate_col7],
    )


@pytest.fixture()
def col8():
    return Column(
        name='col8',
        dtype=(str, type(None)),
        unique=False,
        validators=[col8_valid_values],
        recoders=[translate_col8],
    )


# Defining the Output Column
@pytest.fixture()
def col6_7_8():
    return Column(
        name='col6_7_8',
        dtype=set,
        unique=False,
        validators=[v.funcs.not_null, col6_7_8_valid_values],
        recoders=[setify_drop_nones],
    )


@pytest.fixture()
def col6_7_8_join(col6, col7, col8, col6_7_8):
    return CompoundColumn(input_columns=[col6, col7, col8], output_columns=[col6_7_8], column_transform=join_as_tuple)


@pytest.mark.mtoc
def test_mto_column_init(col6_7_8_join, col6, col7, col8, col6_7_8):
    assert col6_7_8_join.input_columns == [col6, col7, col8]
    assert col6_7_8_join.output_columns == [col6_7_8]
    assert col6_7_8_join.column_transform == join_as_tuple

    assert issubclass(col6_7_8_join.__class__, BaseColumn)
    assert all([isinstance(c, Column) for c in col6_7_8_join.input_columns])
    assert all([isinstance(c, Column) for c in col6_7_8_join.output_columns])


@pytest.mark.mtoc
def test_mto_column_results(col6_7_8_join, demo_good_df, valid_values):
    df = demo_good_df
    valids = valid_values

    assert sort_columns(col6_7_8_join._validate_input(df).reset_index()).equals(sort_columns(valids["validate_input"]))
    assert sort_columns(col6_7_8_join._validate_output(df).reset_index()
                        ).equals(sort_columns(valids["validate_output"]))
    assert sort_columns(col6_7_8_join.validate(df).reset_index()).equals(sort_columns(valids["validate_all"]))


@pytest.fixture()
def valid_values():
    validate_input_json = '''{"validation_type":{"0":"input","1":"input","2":"input","3":"input","4":"input","5":"input","6":"input","7":"input","8":"input","9":"input","10":"input","11":"input"},"column_name":{"0":"col6","1":"col6","2":"col6","3":"col6","4":"col7","5":"col7","6":"col7","7":"col7","8":"col8","9":"col8","10":"col8","11":"col8"},"row":{"0":0,"1":1,"2":2,"3":3,"4":0,"5":1,"6":2,"7":3,"8":0,"9":1,"10":2,"11":3},"col6_valid_values":{"0":false,"1":false,"2":false,"3":false,"4":null,"5":null,"6":null,"7":null,"8":null,"9":null,"10":null,"11":null},"col7_valid_values":{"0":null,"1":null,"2":null,"3":null,"4":false,"5":false,"6":false,"7":false,"8":null,"9":null,"10":null,"11":null},"col8_valid_values":{"0":null,"1":null,"2":null,"3":null,"4":null,"5":null,"6":null,"7":null,"8":false,"9":false,"10":false,"11":false},"dtype":{"0":false,"1":false,"2":false,"3":false,"4":false,"5":false,"6":false,"7":false,"8":false,"9":false,"10":false,"11":false}}'''
    validate_output_json = '''{"validation_type":{"0":"output","1":"output","2":"output","3":"output"},"column_name":{"0":"col6_7_8","1":"col6_7_8","2":"col6_7_8","3":"col6_7_8"},"row":{"0":0,"1":1,"2":2,"3":3},"col6_7_8_valid_values":{"0":false,"1":false,"2":false,"3":false},"not_null":{"0":true,"1":true,"2":true,"3":true},"dtype":{"0":false,"1":false,"2":false,"3":false}}'''
    validate_all_json = '''{"validation_type":{"0":"input","1":"input","2":"input","3":"input","4":"input","5":"input","6":"input","7":"input","8":"input","9":"input","10":"input","11":"input","12":"output","13":"output","14":"output","15":"output"},"column_name":{"0":"col6","1":"col6","2":"col6","3":"col6","4":"col7","5":"col7","6":"col7","7":"col7","8":"col8","9":"col8","10":"col8","11":"col8","12":"col6_7_8","13":"col6_7_8","14":"col6_7_8","15":"col6_7_8"},"row":{"0":0,"1":1,"2":2,"3":3,"4":0,"5":1,"6":2,"7":3,"8":0,"9":1,"10":2,"11":3,"12":0,"13":1,"14":2,"15":3},"col6_7_8_valid_values":{"0":true,"1":true,"2":true,"3":true,"4":true,"5":true,"6":true,"7":true,"8":true,"9":true,"10":true,"11":true,"12":false,"13":false,"14":false,"15":false},"col6_valid_values":{"0":false,"1":false,"2":false,"3":false,"4":true,"5":true,"6":true,"7":true,"8":true,"9":true,"10":true,"11":true,"12":true,"13":true,"14":true,"15":true},"col7_valid_values":{"0":true,"1":true,"2":true,"3":true,"4":false,"5":false,"6":false,"7":false,"8":true,"9":true,"10":true,"11":true,"12":true,"13":true,"14":true,"15":true},"col8_valid_values":{"0":true,"1":true,"2":true,"3":true,"4":true,"5":true,"6":true,"7":true,"8":false,"9":false,"10":false,"11":false,"12":true,"13":true,"14":true,"15":true},"dtype":{"0":false,"1":false,"2":false,"3":false,"4":false,"5":false,"6":false,"7":false,"8":false,"9":false,"10":false,"11":false,"12":false,"13":false,"14":false,"15":false},"not_null":{"0":true,"1":true,"2":true,"3":true,"4":true,"5":true,"6":true,"7":true,"8":true,"9":true,"10":true,"11":true,"12":true,"13":true,"14":true,"15":true}}'''

    vals = {}
    vals["validate_input"] = pd.read_json(validate_input_json)
    vals["validate_output"] = pd.read_json(validate_output_json)
    vals["validate_all"] = pd.read_json(validate_all_json)
    return vals