"""Test whether the parts import correctly."""


def test_import_Column():
    from table_enforcer import Column


def test_import_Enforcer():
    from table_enforcer import Enforcer


def test_import_validate():
    from table_enforcer import validate as v


def test_import_recode():
    from table_enforcer import recode as r


def test_import_ValidationError():
    from table_enforcer.errors import ValidationError
