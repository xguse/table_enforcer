"""Provide builtin recoder functions for common use cases.

Like validators, recoders take a single `pandas.Series` object as input and return
a `pandas.Series` of the same shape and indexes as the original series object. However,
instead of returning a series of `True`/`False` values, it performs some operation on
the data that gets the column data closer to being how you want it to look during
analysis operations.
"""


def upper(series):
    """Transform all text to uppercase."""
    return series.str.upper()


def lower(series):
    """Transform all text to lowercase."""
    return series.str.lower()
