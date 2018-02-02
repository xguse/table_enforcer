#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `table_enforcer` package."""

import pytest
from .conftest import TABLE_PATH_1, TABLE_PATH_2
from . import Usage_Demo as ud

from table_enforcer.errors import ValidationError, RecodingError
from table_enforcer import Column, Enforcer


def test_basic():
    ud.load_csv(path=TABLE_PATH_1, enforcer=ud.demo)


def test_raise_validationerror():
    with pytest.raises(ValidationError):
        ud.load_csv(path=TABLE_PATH_2, enforcer=ud.demo)


def test_raise_recodingerror():
    with pytest.raises(RecodingError):
        ud.load_csv(path=TABLE_PATH_2, enforcer=ud.demo2)


def test_problems_solved():
    ud.load_csv(path=TABLE_PATH_2, enforcer=ud.demo3)