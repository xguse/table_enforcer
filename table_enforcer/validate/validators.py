"""Provide builtin validator functions for common use cases.

Validtor functions take a single argument (a column series) and
return a series containing True/False bools based on which items
pass the validation logic defined in the function.
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

