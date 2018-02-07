# -*- coding: utf-8 -*-
"""Main module."""
import typing as t

from collections import OrderedDict

import pandas as pd

from box import Box
from table_enforcer.errors import ValidationError, RecodingError
from table_enforcer import validate as v

__all__ = [
    "Enforcer",
    "BaseColumn",
    "Column",
    "OTMColumn",
]

VALIDATOR_FUNCTION = t.Callable[[pd.Series], pd.DataFrame]
RECODER_FUNCTION = t.Callable[[pd.Series], pd.Series]
SPLIT_FUNCTION = t.Callable[[str], list]


def set_from_kwargs(kwargs, key, default):
    if key in kwargs.keys():
        value = kwargs[key]
    else:
        value = default
    return value


class Enforcer(object):
    """Class to define table definitions."""

    def __init__(self, columns):
        """Initialize an enforcer instance."""
        self._columns = OrderedDict()

        for column in columns:
            self._columns[column.name] = column

        self.columns = list(self._columns.keys())

    def _make_validations(self, table: pd.DataFrame) -> Box:
        """Return a dict-like object containing dataframes of which tests passed/failed for each column."""
        results = Box()

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
            df = column.update_dataframe(df, series=table[name])

        return df


class BaseColumn(object):
    """Base class representing a single table column."""

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

    def _check_series_name(self, series, override_name=None):
        if override_name is None:
            name = self.name
        else:
            name = override_name

        if series.name != name:
            raise ValueError(f"The name of provided series '{series.name}' does not match this column's name '{name}'.")

    def update_dataframe(self, df, series):
        """Perform ``self.recode(series, validate=True)`` and add resulting column(s) to ``df`` and return ``df``."""
        raise NotImplementedError('This method should be overridden by subclass.')

    def validate(self, series: pd.Series, **kwargs) -> pd.DataFrame:
        """Return a dataframe of validation results for the provided series vs the vector of validators."""
        override_name = set_from_kwargs(kwargs, key="override_name", default=None)
        self._check_series_name(series, override_name=override_name)

        validators = self.validators

        results = pd.DataFrame({validator: series for validator in validators}, index=series.index)

        for name, func in validators.items():
            results[name] = func(results[name])

        results['dtype'] = self._validate_series_dtype(series)

        if self.unique:
            results['unique'] = v.funcs.unique(series)

        return results

    def recode(self, series: pd.Series, validate=False, **kwargs) -> pd.Series:
        """Pass the provided series obj through each recoder function sequentially and return the final result.

        If `validate`: raise ValidationError if validation fails.
        """
        override_name = set_from_kwargs(kwargs, key="override_name", default=None)
        self._check_series_name(series, override_name=override_name)

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
            failed_rows = find_failed_rows(self.validate(data, override_name=override_name))
            if failed_rows.shape[0] > 0:
                raise ValidationError(f"Rows that failed to validate for column '{self.name}':\n{failed_rows}")

        return data


class Column(BaseColumn):
    """Class representing a single table column."""

    def __init__(self, name: str, dtype: type, unique: bool, validators: t.List[VALIDATOR_FUNCTION],
                 recoders: t.List[RECODER_FUNCTION]) -> None:
        """Construct a new `Column` object."""
        super().__init__(name=name, dtype=dtype, unique=unique, validators=validators, recoders=recoders)

    def update_dataframe(self, df, series):
        """Perform ``self.recode(series, validate=True)``, and add resulting column to ``df`` and return ``df``."""
        df = df.copy()
        df[self.name] = self.recode(series=series, validate=True)
        return df


class OTMColumn(BaseColumn):
    """Class representing a set of table columns derived from spliting up a single parent column."""

    def __init__(
            self,
            name: str,
            unique: bool,
            validators: t.List[VALIDATOR_FUNCTION],
            recoders: t.List[RECODER_FUNCTION],
            child_columns: t.List[Column],
            split_func: SPLIT_FUNCTION,) -> None:
        """Construct a new ``OTMColumn`` object.

        This class allows the splitting of a single column's data into multiple
        child columns based on logic defined in the provided ``split_func``. The resulting
        child columns are ``Column`` objects defined in their own right along with accompanying
        validators and recoders. These are provided through the ``child_columns`` attr and
        are responsible for dealing with the `pd.Series` objects created after applying the
        ``split_func`` as normal.


        ``OTMColumn.dtype == str`` and is set automatically because only ``str`` splitting is
        supported at the moment.

        Args:
            name (str): Name of the target column in the dataframe.
            unique (bool): If ``True``, column values may not repeat.
            validators (list): List of validators for PRE-SPLIT column.
            recoders (list): List of recoders for PRE-SPLIT column.
            child_columns (list): List of fully defined ``Column`` objects
                                  that will represent the new columns generated
                                  from the splitting. The order of these are
                                  preserved in the final dataframe.
            split_func (Callable): A function to split the original column value. Must
                                   return dict-like object with keys matching the names
                                   of ``child_columns``.

        """
        super().__init__(name=name, dtype=str, unique=unique, validators=validators, recoders=recoders)

        self._child_columns = OrderedDict({col.name: col for col in child_columns})
        self._split_func = split_func

    def update_dataframe(self, df, series):
        """Perform ``self.recode(series, validate=True)``, and add resulting columns to ``df`` and return ``df``."""
        df = df.copy()

        split_series = self.split_parent(series=series, recode=True)

        for column in self._child_columns.values():
            df = column.update_dataframe(df=df, series=split_series[column.name])

        return df

    def split_parent(self, series, recode=False):
        """Split the original series into multiple series and return the dict.

        Each new series will be named in accordance with self._child_columns.
        """
        if recode:
            parent_series = self.recode_parent(series, validate=False)
        else:
            parent_series = series

        series_of_dicts = parent_series.apply(self._split_func)

        split_series = {}

        for name in self._child_columns:
            new_series = series_of_dicts.apply(lambda i: i[name])
            new_series.name = name
            split_series[name] = new_series

        return split_series

    def validate_parent(self, series: pd.Series) -> pd.DataFrame:
        """Return a dataframe of validation results for the original data vs the parent column's vector of validators."""
        return super().validate(series=series)

    def recode_parent(self, series: pd.Series, validate=False) -> pd.Series:
        """Pass the provided series obj through each of the original column's recoder functions sequentially and return the final result.

        If `validate`: raise ValidationError if validation fails.
        """
        return super().recode(series=series, validate=validate)

    def validate(self, series: pd.Series, **kwargs) -> pd.DataFrame:
        """Return a dataframe of validation results for the parent and split series series vs each's vector of validators."""
        validations = {}
        validations[self.name] = self.validate_parent(series)
        validations[self.name]["Validations"] = self.name

        split_series = self.split_parent(series=series, recode=False)

        for name, col in self._child_columns.items():
            validations[name] = col.validate(split_series[name], override_name=name)
            validations[name]["Validations"] = name

        return pd.concat(validations.values()).set_index("Validations").fillna(True)

    def recode(self, series: pd.Series, validate=False, **kwargs) -> pd.Series:
        """Pass the provided series obj through each recoder function sequentially and return the final result.

        If `validate`: raise ValidationError if validation fails.
        """
        split_series = self.split_parent(series=series, recode=True)

        recoded_children = []

        for name, col in self._child_columns.items():
            recoded_children.append(col.recode(series=split_series[name], validate=validate, override_name=name))

        return recoded_children
