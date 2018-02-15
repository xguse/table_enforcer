# -*- coding: utf-8 -*-
"""Main module."""
import typing as t

import pandas as pd

from box import Box
from table_enforcer.errors import ValidationError, RecodingError
from .utils import validate as v

__all__ = [
    "Enforcer",
    "BaseColumn",
    "Column",
    "CompoundColumn",
]

VALIDATOR_FUNCTION = t.Callable[[pd.Series], pd.DataFrame]
RECODER_FUNCTION = t.Callable[[pd.Series], pd.Series]


def find_failed_rows(results):
    failed_rows = results.apply(lambda vec: ~vec.all(), axis=1)
    return results.loc[failed_rows]


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
        self.columns = columns

    def _make_validations(self, table: pd.DataFrame) -> Box:
        """Return a dict-like object containing dataframes of which tests passed/failed for each column."""
        results = []

        for column in self.columns:
            results.append(column.validate(table))

        return results

    def validate(self, table: pd.DataFrame) -> bool:
        """Return True if all validation tests pass: False otherwise."""
        validations = self._make_validations(table=table)

        results = [df.all().all() for df in validations]

        return all(results)

    def recode(self, table: pd.DataFrame, validate=False) -> pd.DataFrame:
        """Return a fully recoded dataframe.

        Args:
            table (pd.DataFrame): A dataframe on which to apply recoding logic.
            validate (bool): If ``True``, recoded table must pass validation tests.
        """
        df = pd.DataFrame(index=table.index)

        for column in self.columns:
            df = column.update_dataframe(df, table=table, validate=validate)

        return df


class BaseColumn(object):
    """Base Class for Columns.

    Lays out essential methods api.
    """

    def update_dataframe(self, df, table, validate=False):
        """Perform ``self.recode`` and add resulting column(s) to ``df`` and return ``df``."""
        df = df.copy()
        recoded_columns = self.recode(table=table, validate=validate)
        return pd.concat([df, recoded_columns], axis=1)

    def validate(self, table: pd.DataFrame, failed_only=False) -> pd.DataFrame:
        """Return a dataframe of validation results for the appropriate series vs the vector of validators.

        Args:
            table (pd.DataFrame): A dataframe on which to apply validation logic.
            failed_only (bool): If ``True``: return only the indexes that failed to validate.
        """
        raise NotImplementedError("This method must be defined for each subclass.")

    def recode(self, table: pd.DataFrame, validate=False) -> pd.DataFrame:
        """Pass the appropriate columns through each recoder function sequentially and return the final result.

        Args:
            table (pd.DataFrame): A dataframe on which to apply recoding logic.
            validate (bool): If ``True``, recoded table must pass validation tests.
        """
        raise NotImplementedError("This method must be defined for each subclass.")


class Column(BaseColumn):
    """Class representing a single table column."""

    def __init__(
            self,
            name: str,
            dtype: type,
            unique: bool,
            validators: t.List[VALIDATOR_FUNCTION],
            recoders: t.List[RECODER_FUNCTION],) -> None:
        """Construct a new `Column` object.

        Args:
            name (str): The exact name of the column in a ``pd.DataFrame``.
            dtype (type): The type that each member of the recoded column must belong to.
            unique (bool): Whether values are allowed to recur in this column.
            validators (list): A list of validator functions.
            recoders (list): A list of recoder functions.
        """
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

    def validate(self, table: pd.DataFrame, failed_only=False) -> pd.DataFrame:
        """Return a dataframe of validation results for the appropriate series vs the vector of validators.

        Args:
            table (pd.DataFrame): A dataframe on which to apply validation logic.
            failed_only (bool): If ``True``: return only the indexes that failed to validate.
        """
        series = table[self.name]

        self._check_series_name(series)

        validators = self.validators

        results = pd.DataFrame({validator: series for validator in validators}, index=series.index)

        for name, func in validators.items():
            results[name] = func(results[name])

        results['dtype'] = self._validate_series_dtype(series)

        if self.unique:
            results['unique'] = v.funcs.unique(series)

        if failed_only:
            results = find_failed_rows(results)

        return results

    def recode(self, table: pd.DataFrame, validate=False) -> pd.DataFrame:
        """Pass the provided series obj through each recoder function sequentially and return the final result.

        Args:
            table (pd.DataFrame): A dataframe on which to apply recoding logic.
            validate (bool): If ``True``, recoded table must pass validation tests.
        """
        series = table[self.name]

        self._check_series_name(series)

        col = self.name

        data = series.copy()

        for recoder in self.recoders.values():
            try:
                data = recoder(data)
            except (BaseException) as err:
                raise RecodingError(col, recoder, err)

        if validate:
            failed_rows = find_failed_rows(self.validate(data.to_frame()))
            if failed_rows.shape[0] > 0:
                raise ValidationError(f"Rows that failed to validate for column '{self.name}':\n{failed_rows}")

        return data.to_frame()


class CompoundColumn(BaseColumn):
    """Class representing multiple columns and the logic governing their transformation from source table to recoded table."""

    def __init__(
            self,
            input_columns: t.List[Column],
            output_columns: t.List[Column],
            column_transform,) -> None:
        """Construct a new ``CompoundColumn`` object.

        Args:
            input_columns (list, Column): A list of ``Column`` objects representing column(s) from the SOURCE table.
            output_columns (list, Column): A list of ``Column`` objects representing column(s) from the FINAL table.
            column_transform (Callable): Function accepting the table object, performing transformations to it and returning a DataFrame containing the NEW columns only.
        """
        self.input_columns = input_columns
        self.output_columns = output_columns
        self.column_transform = column_transform

    def _do_validation_set(self, table: pd.DataFrame, columns, validation_type, failed_only=False) -> pd.DataFrame:
        """Return a dataframe of validation results for the appropriate series vs the vector of validators."""
        validations = []

        for column in columns:
            validation = column.validate(table=table, failed_only=failed_only)
            validation["column_name"] = column.name
            validation["validation_type"] = validation_type
            validations.append(validation)

        validation_table = pd.concat(validations)
        validation_table.index.name = 'row'

        return validation_table.reset_index().set_index(["validation_type", "column_name", "row"])

    def _validate_input(self, table: pd.DataFrame, failed_only=False) -> pd.DataFrame:
        """Return a dataframe of validation results for the appropriate series vs the vector of validators."""
        return self._do_validation_set(
            table=table,
            columns=self.input_columns,
            validation_type="input",
            failed_only=failed_only,)

    def _recode_set(self, table: pd.DataFrame, columns, validate=False) -> pd.DataFrame:
        recoded_columns = []

        for column in columns:
            recoded = column.recode(table=table, validate=validate)
            recoded_columns.append(recoded)

        return pd.concat(recoded_columns, axis=1)

    def _recode_input(self, table: pd.DataFrame, validate=False) -> pd.DataFrame:
        return self._recode_set(table=table, columns=self.input_columns, validate=validate)

    def _validate_output(self, table: pd.DataFrame, failed_only=False) -> pd.DataFrame:
        transformed_columns = self.column_transform(table)
        return self._do_validation_set(
            table=transformed_columns,
            columns=self.output_columns,
            validation_type="output",
            failed_only=failed_only,)

    def _recode_output(self, table: pd.DataFrame, validate=False) -> pd.DataFrame:
        transformed_columns = self.column_transform(table)
        return self._recode_set(table=transformed_columns, columns=self.output_columns, validate=validate)

    def validate(self, table: pd.DataFrame, failed_only=False) -> pd.DataFrame:
        """Return a dataframe of validation results for the appropriate series vs the vector of validators.

        Args:
            table (pd.DataFrame): A dataframe on which to apply validation logic.
            failed_only (bool): If ``True``: return only the indexes that failed to validate.
        """
        return pd.concat([
            self._validate_input(table, failed_only=failed_only),
            self._validate_output(table, failed_only=failed_only),
        ]).fillna(True)

    def recode(self, table: pd.DataFrame, validate=False) -> pd.DataFrame:
        """Pass the appropriate columns through each recoder function sequentially and return the final result.

        Args:
            table (pd.DataFrame): A dataframe on which to apply recoding logic.
            validate (bool): If ``True``, recoded table must pass validation tests.
        """
        return self._recode_output(self._recode_input(table, validate=validate), validate=validate)
