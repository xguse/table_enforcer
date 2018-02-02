# -*- coding: utf-8 -*-
"""Main module."""
import typing as t

from collections import OrderedDict

import pandas as pd

from munch import Munch
from table_enforcer.errors import ValidationError, RecodingError
from table_enforcer import validate as v

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

    def _make_validations(self, table: pd.DataFrame) -> Munch:
        """Return a dict-like object containing dataframes of which tests passed/failed for each column."""
        results = Munch()

        for name, column in self._columns.items():
            results[name] = column.validate(table[name])

        return results

    def validate(self, table: pd.DataFrame) -> bool:
        """Return True if all validation tests pass: False otherwise."""

        validations = self._make_validations(table=table)

        results = [df.all().all() for df in validations.values()]

        return all(results)

    def recode(self, table: pd.DataFrame, validate=False) -> pd.DataFrame:
        """Return a fully recoded dataframe.

        If `validate`: raise ValidationError if validation fails.
        """
        df = pd.DataFrame(index=table.index)

        for name, column in self._columns.items():
            df[name] = column.recode(series=table[name], validate=validate)

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

    def _check_series_name(self, series):
        if series.name != self.name:
            raise ValueError(
                f"The name of provided series '{series.name}' does not match this column's name '{self.name}'.")

    def validate(self, series: pd.Series) -> pd.DataFrame:
        """Return a dataframe of validation results for the provided series vs the vector of validators."""
        self._check_series_name(series)

        validators = self.validators

        results = pd.DataFrame({validator: series for validator in validators}, index=series.index)

        for name, func in validators.items():
            results[name] = func(results[name])

        results['dtype'] = self._validate_series_dtype(series)

        if self.unique:
            results['unique'] = v.funcs.unique(series)

        return results

    def recode(self, series: pd.Series, validate=False) -> pd.Series:
        """Pass the provided series obj through each recoder function sequentially and return the final result.

        If `validate`: raise ValidationError if validation fails.
        """
        self._check_series_name(series)

        def find_failed_rows(results):
            failed_rows = results.apply(lambda vec: ~vec.all(), axis=1)
            return results.loc[failed_rows]

        col = self.name

        data = series.copy()

        for recoder in self.recoders.values():
            try:
                data = recoder(data)
            except (BaseException) as err:
                raise RecodingError(col, recoder, err)

        if validate:
            failed_rows = find_failed_rows(self.validate(data))
            if failed_rows.shape[0] > 0:
                raise ValidationError(f"Rows that failed to validate for column '{self.name}':\n{failed_rows}")

        return data
