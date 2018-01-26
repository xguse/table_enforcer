# -*- coding: utf-8 -*-
"""Main module."""
import typing as t

from collections import OrderedDict

import pandas as pd

from munch import Munch

__all__ = ["Enforcer", "Column"]

VALIDATOR_FUNCTION = t.Callable[[pd.Series], pd.DataFrame]
RECODER_FUNCTION = t.Callable[[pd.Series], pd.Series]


class Enforcer(object):
    """Class to define table definitions."""

    def __init__(self, columns):
        """Initialize an enforcer instance."""
        self._columns = OrderedDict()

        for column in columns:
            self._columns[column.name] = column

        self.columns = list(self._columns.keys())

    def make_validations(self, table: pd.DataFrame) -> Munch:
        """Return a dict-like object containing dataframes of which tests passed/failed for each column."""
        results = Munch()

        for name, column in self._columns.items():
            results[name] = column.validate(table)

        return results

    def validate(self, table: pd.DataFrame, recode: bool = False) -> bool:
        """Return True if all validation tests pass: False otherwise."""
        if recode:
            table = self.recode(table)

        validations = self.make_validations(table=table)

        results = [df.all().all() for df in validations.values()]

        return all(results)

    def recode(self, table: pd.DataFrame) -> pd.DataFrame:
        """Return a fully recoded dataframe."""
        df = table[self.columns].copy()

        for name, column in self._columns.items():
            df[name] = column.recode(table)

        return df


class Column(object):
    """Class representing a single table column."""

    def __init__(self, name: str, dtype: type, unique: bool, validators: t.List[VALIDATOR_FUNCTION],
                 recoders: t.List[RECODER_FUNCTION]) -> None:
        """Construct a new `Column` object."""
        if validators is None:
            validators = []
        if recoders is None:
            recoders = []
        self.name = name
        self.dtype = dtype
        self.unique = unique
        self.validators = self._dict_of_funcs(validators)
        self.recoders = self._dict_of_funcs(recoders)

    def _dict_of_funcs(self, funcs: list) -> pd.Series:
        """Return a pd.Series of functions with index derived from the function name."""
        return {func.__name__: func for func in funcs}

    def _validate_series_dtype(self, series: pd.Series) -> pd.Series:
        """Validate that the series data is the correct dtype."""
        return series.apply(lambda i: isinstance(i, self.dtype))

    def validate(self, table: pd.DataFrame, recode: bool = False) -> pd.DataFrame:
        """Return a dataframe of validation results for the correct column in table vs the vector of validators."""
        col = self.name
        validators = self.validators

        if recode:
            series = self.recode(table)
        else:
            series = table[col]

        results = pd.DataFrame({validator: series for validator in validators})

        for name, func in validators.items():
            results[name] = func(results[name])

        results['dtype'] = self._validate_series_dtype(series)
        if self.unique:
            results['unique'] = v.funcs.unique(series)

        return results

    def recode(self, table: pd.DataFrame) -> pd.Series:
        """Pass the appropriate column data in `table` through each recoder function in series and return the final result."""
        col = self.name
        series = table[col]

        data = series.copy()
        for recoder in self.recoders.values():
            data = recoder(data)

        return data
