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
            msg = "That bonehead {author} should really hear your rage about this disgraceful result! Feel free to tell them at {email}".format(author=__author__, email=__email__)

        self.args = (msg, *self.args)


class ValidationError(TableEnforcerError):
    """Raise when a validation/sanity check comes back with unexpected value."""
