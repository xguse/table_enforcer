"""Provide builtin validator functions for common use cases.

In general, validators take a single `pandas.Series` object as
input and return a `pandas.Series` of the same shape and indexes
containing `True` or `False` relative to which items passed the
validation logic.
"""
import pandas as pd
# import numpy as np

# from table_enforcer import errors as e
# from table_enforcer.validate import decorators as dec


def not_null(series: pd.Series) -> pd.Series:
    """Return Series with True/False bools based on which items pass."""
    return pd.notnull(series)


def positive(series: pd.Series) -> pd.Series:
    """Test that the data items are positive."""
    return series > 0


def negative(series: pd.Series) -> pd.Series:
    """Test that the data items are negative."""
    return series < 0


def unique(series: pd.Series) -> pd.Series:
    """Test that the data items do not repeat."""
    return ~series.duplicated(keep=False)


def upper(series):
    """Test that the data items are all uppercase."""
    return series.str.isupper()


def lower(series):
    """Test that the data items are all lowercase."""
    return series.str.islower()

