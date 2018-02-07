from pathlib import Path

import pytest
import pandas as pd

from table_enforcer import Column, Enforcer
import table_enforcer.errors as e

from table_enforcer import validate as v
from table_enforcer import recode as r

TEST_FILES = Path("tests/files/")

TABLE_PATH_1 = TEST_FILES / "demo_table.csv"
TABLE_PATH_2 = TEST_FILES / "demo_table_bad.csv"


def length_is_one(series):
    return series.str.len() == 1


def valid_sex(series):
    sex = set(['M', 'F'])
    return series.isin(sex)


def standardize_sex(series):
    """Return a series where common representations of 'male'/'female' are standardized.

    Things like ['M', 'MALE', 'M', 'BOY', ...] are converted to `M`.
    Representations of female are treated similarly.
    """
    mapper = {
        "M": "M",
        "MALE": "M",
        "BOY": "M",
        "F": "F",
        "FEMALE": "F",
        "GIRL": "F",
    }
    if series.str.islower().any():
        raise ValueError("standardize_sex expects input series to contain only UPPERCASE letters.")
    else:
        return series.apply(lambda x: mapper[x])


@pytest.fixture()
def source_table():
    return pd.read_csv(TABLE_PATH_1)


@pytest.fixture()
def col4(col4_validators, col4_recoders):
    col4 = Column(name='col4', dtype=str, unique=False, validators=col4_validators, recoders=col4_recoders)

    return col4


@pytest.fixture()
def col4_validators():
    return [v.funcs.upper, length_is_one, valid_sex]


@pytest.fixture()
def col4_recoders():
    return [r.funcs.upper, standardize_sex]


@pytest.fixture()
def col4_no_recoders(col4_validators):
    col4 = Column(name='col4', dtype=str, unique=False, validators=col4_validators, recoders=[])

    return col4


@pytest.fixture()
def enforcer(col4):
    return Enforcer(columns=[col4])
