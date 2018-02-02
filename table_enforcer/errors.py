#!/usr/bin/env python
"""Provide error classes."""

# Imports
from table_enforcer import __author__, __email__


class TableEnforcerError(Exception):
    """Base error class."""


class NotImplementedYet(NotImplementedError, TableEnforcerError):
    """Raise when a section of code that has been left for another time is asked to execute."""

    def __init__(self, msg=None):
        """Set up the Exception."""
        if msg is None:
            msg = f"That bonehead {__author__} should really hear your rage about this disgraceful result! Feel free to tell them at {__email__}"
            self.args = (msg, *self.args)


class ValidationError(TableEnforcerError):
    """Raise when a validator function fails to generate all successes when called inside of a `recode` method."""


class RecodingError(TableEnforcerError):
    """Raise when a recoder function raises an error."""

    def __init__(self, column, recoder, exception):
        """Set up the Exception."""
        msg = f"Recoder '{recoder.__name__}' raised the following error on column '{column}': {repr(exception)}."
        self.args = (msg,)