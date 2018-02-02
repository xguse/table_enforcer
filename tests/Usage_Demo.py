"""Provide functions and objects to test the overall systems level usage."""
import pandas as pd
import numpy as np

from table_enforcer import Enforcer, Column
from table_enforcer import validate as v
from table_enforcer import recode as r


def gte2(series):
    return series >= 2


def lte10(series):
    return series <= 10


def length_is_one(series):
    return series.str.len() == 1


def valid_sex(series):
    sex = set(['M', 'F'])
    return series.isin(sex)


@v.decorators.minmax(low=2, high=10)
def bt_2_and_10(series):
    """Test that the data items fall within range: 2 <= x <= 10."""
    return series


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


def standardize_sex2(series):
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
        "FEEMALE": "F",
    }
    if series.str.islower().any():
        raise ValueError("standardize_sex expects input series to contain only UPPERCASE letters.")
    else:
        return series.apply(lambda x: mapper[x])


def load_csv(path, enforcer):
    df = pd.read_csv(path)
    return enforcer.recode(df, validate=True)


def handle_values_below_detection_limit(series):
    series[series < 2] = 2
    return series


## Column defintions ##
col1 = Column(
    name='col1',
    dtype=np.int,
    unique=False,
    validators=[v.funcs.not_null, v.funcs.positive, bt_2_and_10],
    recoders=None
)

col3 = Column(
    name='col3', dtype=np.int, unique=True, validators=[v.funcs.not_null, v.funcs.positive, bt_2_and_10], recoders=None
)

col4 = Column(
    name='col4',
    dtype=str,
    unique=False,
    validators=[v.funcs.upper, length_is_one, valid_sex],
    recoders=[r.funcs.upper, standardize_sex]
)

col1_new = Column(
    name='col1',
    dtype=np.int,
    unique=False,
    validators=[v.funcs.not_null, v.funcs.positive, bt_2_and_10],
    recoders=[handle_values_below_detection_limit]
)

col4_new = Column(
    name='col4',
    dtype=str,
    unique=False,
    validators=[v.funcs.upper, length_is_one, valid_sex],
    recoders=[r.funcs.upper, standardize_sex2]
)

## Enforcer Definitions ##
demo = Enforcer(columns=[col1, col3, col4])
demo2 = Enforcer(columns=[col1_new, col3, col4])
demo3 = Enforcer(columns=[col1_new, col3, col4_new])
